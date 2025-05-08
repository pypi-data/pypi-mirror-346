import time

from pyrogram import Client, raw, utils
from pyrogram.storage import Storage
from tortoise import fields
from tortoise.signals import pre_save
from x_model.models import Model
from xync_schema.models import User


class Session(Model):
    name = fields.CharField(255, primary_key=True)
    dc_id = fields.IntField(null=False)
    api_id = fields.IntField(null=False)
    test_mode = fields.BooleanField(null=True)
    auth_key = fields.BinaryField()
    date = fields.IntField(null=False)
    user: fields.OneToOneRelation[User] = fields.OneToOneField("models.User", "sessions")
    user_id: int
    is_bot = fields.BooleanField(null=True)


class Peer(Model):
    session: fields.ForeignKeyRelation[Session] = fields.OneToOneField("models.Session", "peers", primary_key=True)
    id: int = fields.BigIntField(True)
    access_hash: int = fields.BigIntField()
    type = fields.CharField(255)
    phone_number = fields.CharField(255)
    last_update_on: int = fields.BigIntField()


@pre_save(Peer)
async def person(_meta, peer: Peer, _db, _updated: dict) -> None:
    if not peer.last_update_on:
        peer.last_update_on = int(time.time())


class UpdateState(Model):
    session: fields.ForeignKeyRelation[Session] = fields.OneToOneField("models.Session", "update_states", primary_key=True)
    pts = fields.IntField()
    qts = fields.IntField()
    date = fields.IntField()
    seq = fields.IntField()


class Version(Model):
    id: None
    number = fields.IntField(primary_key=True)


def get_input_peer(peer_id: int, access_hash: int, peer_type: str):
    if peer_type in ["user", "bot"]:
        return raw.types.InputPeerUser(
            user_id=peer_id,
            access_hash=access_hash
        )

    if peer_type == "group":
        return raw.types.InputPeerChat(
            chat_id=-peer_id
        )

    if peer_type in ["channel", "supergroup"]:
        return raw.types.InputPeerChannel(
            channel_id=utils.get_channel_id(peer_id),
            access_hash=access_hash
        )

    raise ValueError(f"Invalid peer type: {peer_type}")


class MultiPostgresStorage(Storage):
    VERSION = 1
    USERNAME_TTL = 8 * 60 * 60

    def __init__(self, client: Client, database: dict):
        super().__init__(client.name)
        self.cn = f"postgresql+asyncpg://{database['db_user']}:{database['db_pass']}@{database['db_host']}:{database['db_port']}/{database['db_name']}"
        self.name = client.name

    async def open(self):
        if not await Session.filter(session_name=self.name).exists():
            _ = await Session.create(
                session_name=self.name,
                dc_id=None,
                api_id=None,
                test_mode=None,
                auth_key=None,
                date=int(time.time()),
                user_id=None,
                is_bot=None
            )

    async def save(self):
        await self.date(int(time.time()))

    async def close(self):
        await self.cn.close()

    async def delete(self):
        # await UpdateState.filter(session__name=self.name).delete()
        # delete(UsernameModel).where(UsernameModel.session_name == self.name)
        # await Peer.filter(session__name=self.name).delete()  # no need if delete cascade
        await Session.filter(session__name=self.name).delete()

    async def update_peers(self, peers: list[tuple[int, int, str, str]]):
        for peer in peers:
            existing_peer = await Peer.get_or_none(session__name=self.name, id=peer[0])

            if existing_peer:
                existing_peer.access_hash = peer[1]
                existing_peer.type = peer[2]
                existing_peer.phone_number = peer[3]
            else:
                new_peer = await Peer.create(
                    session__name=self.name,  # todo: pk ?
                    id=peer[0],
                    access_hash=peer[1],
                    type=peer[2],
                    phone_number=peer[3]
                )

    async def update_usernames(self, usernames: list[tuple[int, list[str]]]):
        for telegram_id, _ in usernames:
            await session.execute(
                delete(UsernameModel).where(UsernameModel.session_name == self.name,
                                            UsernameModel.id == telegram_id)
            )

        for telegram_id, user_list in usernames:
            for username in user_list:
                User
                new_username = UsernameModel(session_name=self.name, id=telegram_id, username=username)
                session.add(new_username)

        await session.commit()

    async def get_peer_by_id(self, peer_id_or_username):
        async with self.session_maker() as session:
            if isinstance(peer_id_or_username, int):
                peer = await session.execute(
                    select(PeerModel).filter_by(session_name=self.name, id=peer_id_or_username)
                )
                peer = peer.scalar_one_or_none()
                if peer is None:
                    raise KeyError(f"ID not found: {peer_id_or_username}")
                return get_input_peer(peer.id, peer.access_hash, peer.type)
            elif isinstance(peer_id_or_username, str):
                r = await session.execute(
                    select(
                        PeerModel.id,
                        PeerModel.access_hash,
                        PeerModel.type,
                        PeerModel.last_update_on
                    )
                    .join(UsernameModel, UsernameModel.id == PeerModel.id)
                    .filter(UsernameModel.username == peer_id_or_username,
                            UsernameModel.session_name == self.name,
                            PeerModel.session_name == self.name)
                    .order_by(PeerModel.last_update_on.desc())
                )
                r = r.fetchone()
                if r is None:
                    raise KeyError(f"Username not found: {peer_id_or_username}")
                if len(r) == 4:
                    peer_id, access_hash, peer_type, last_update_on = r
                else:
                    raise ValueError(f"The result does not contain the expected tuple of values. Received: {r}")
                if last_update_on:
                    if abs(time.time() - last_update_on) > self.USERNAME_TTL:
                        raise KeyError(f"Username expired: {peer_id_or_username}")
                return get_input_peer(peer_id, access_hash, peer_type)

            else:
                raise ValueError("peer_id_or_username must be an integer (ID) or string (Username).")

    async def get_peer_by_username(self, username: str):
        async with self.session_maker() as session:
            peer_alias = aliased(PeerModel)
            username_alias = aliased(UsernameModel)
            r = await session.execute(
                select(peer_alias.id, peer_alias.access_hash, peer_alias.type, peer_alias.last_update_on)
                .join(username_alias, username_alias.id == peer_alias.id)
                .filter(username_alias.username == username, username_alias.session_name == self.name)
                .order_by(peer_alias.last_update_on.desc())
            )
            r = r.fetchone()
            if r is None:
                raise KeyError(f"Username not found: {username}")

            peer_id, access_hash, peer_type, last_update_on = r
            return get_input_peer(peer_id, access_hash, peer_type)

    async def update_state(self, value: Tuple[int, int, int, int, int] = object):
        async with self.session_maker() as session:
            if value == object:
                result = await session.execute(
                    select(UpdateStateModel).filter_by(session_name=self.name)
                )
                return result.scalars().all()
            else:
                if isinstance(value, int):
                    await session.execute(
                        delete(UpdateStateModel)
                        .where(UpdateStateModel.session_name == self.name, UpdateStateModel.id == value)
                    )
                else:
                    state = await session.execute(
                        select(UpdateStateModel).filter_by(session_name=self.name, id=value[0])
                    )
                    state_instance = state.scalar_one_or_none()

                    if state_instance:
                        state_instance.pts = value[1]
                        state_instance.qts = value[2]
                        state_instance.date = value[3]
                        state_instance.seq = value[4]
                    else:
                        state_instance = UpdateStateModel(
                            id=value[0],
                            session_name=self.name,
                            pts=value[1],
                            qts=value[2],
                            date=value[3],
                            seq=value[4]
                        )
                        session.add(state_instance)

                await session.commit()

    async def get_peer_by_phone_number(self, phone_number: str):
        if not (peer := await Peer.filter(
                session__name=self.name, phone_number=phone_number
        ).values_list("id", "access_hash", "type")):
            raise KeyError(f"Phone number not found: {phone_number}")
        return get_input_peer(*peer)

    async def _get(self, attr: str):
        return await Session.get(name=self.name).values_list(attr, flat=True)

    async def _set(self, attr: str, value: Any):
        await Session.update_or_create({attr: value}, name=self.name)

    async def _accessor(self, attr: str, value: Any = object):
        if value == object:
            return await self._get(attr)
        else:
            await self._set(attr, value)

    async def dc_id(self, value: int = object):
        return await self._accessor('dc_id', value)

    async def api_id(self, value: int = object):
        return await self._accessor('api_id', value)

    async def test_mode(self, value: bool = object):
        return await self._accessor('test_mode', value)

    async def auth_key(self, value: bytes = object):
        return await self._accessor('auth_key', value)

    async def date(self, value: int = object):
        return await self._accessor('date', value)

    async def user_id(self, value: int = object):
        return await self._accessor('user_id', value)

    async def is_bot(self, value: bool = object):
        return await self._accessor('is_bot', value)

    async def version(self, value: int = object):
        if value == object:
            ver = await Version.first()
            return ver.number
        else:
            await Version.update_or_create({"number": value})
