from aiohttp import ClientSession

from flespi_sdk.modules.realms.realm_home import RealmHome
from flespi_sdk.modules.realms.realm_token_params import RealmTokenParams
from flespi_sdk.modules.realms.users import Users
from flespi_sdk.modules.item_with_metadata import ItemWithMetadata


class Realm(ItemWithMetadata):
    """
    Represents a realm in the Flespi system.
    """

    def __init__(self, realm_id: int, session: ClientSession, cid: int | None = None):
        item_path = f"platform/realms/{realm_id}"
        super().__init__(
            parent_id=None, id=realm_id, item_path=item_path, session=session, cid=cid
        )
        self.users = Users(
            realm_id=realm_id,
            client_session=session,
            cid=cid,
        )

        self.home = RealmHome(realm_id=realm_id, session=session, cid=cid)
        self.token_params = RealmTokenParams(
            realm_id=realm_id, session=session, cid=cid
        )
