from aiohttp import ClientSession
from flespi_sdk.modules.flespi_session import FlespiSession
from flespi_sdk.modules.metadata import Metadata


class ItemWithMetadata(FlespiSession):
    def __init__(
        self,
        parent_id: int | None,
        id: int,
        item_path: str,
        session: ClientSession,
        cid: int | None = None,
    ):
        super().__init__(session, cid)
        self.parent_id = parent_id
        self.id = id
        self.item_path = item_path
        self.metadata = Metadata(item_path, session, cid)

    async def get_name(self) -> str:
        """
        Get the name of the item.
        :return: The name of the item.
        """
        async with self.session.get(
            f"/{self.item_path}",
            headers=self.get_headers(),
        ) as response:
            result = await self.get_result(response)
            return result[0]["name"]
