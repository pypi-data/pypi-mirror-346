import aiohttp

from flespi_sdk.modules.flespi_session import FlespiSession


class Metadata(FlespiSession):
    def __init__(
        self, item_path, session: aiohttp.ClientSession, cid: int | None = None
    ):
        super().__init__(session, cid)
        self.item_path = item_path

    async def get(self) -> dict:
        """
        Get metadata for the current account.
        :return: Metadata as a dictionary.
        """
        params = {"fields": "metadata"}
        async with self.session.get(
            self.item_path, params=params, headers=self.get_headers()
        ) as response:
            result = await self.get_result(response)
            return result[0]["metadata"]

    async def set(self, metadata: dict) -> None:
        """ "
        "Set metadata for the current account.
        :param metadata: Metadata as a dictionary.
        """
        async with self.session.put(
            self.item_path,
            json={"metadata": metadata},
            headers=self.get_headers(),
        ) as response:
            await self.get_result(response)

    async def get_value(self, key_path: str):
        """
        Get a specific value from the metadata.
        :param key_path: The key path to the value in the metadata.
        :return: The value from the metadata.
        """
        metadata = await self.get()
        if not metadata:
            return None
        keys = key_path.split(".")
        value = metadata
        for key in keys:
            if key in value:
                value = value[key]
            else:
                return None
        return value

    async def set_value(self, key_path: str, value) -> None:
        """
        Set a specific value in the metadata.
        :param key_path: The key path to the value in the metadata.
        :param value: The value to set.
        """
        metadata = await self.get() or {}
        keys = key_path.split(".")
        metadata_level = metadata
        for key in keys[:-1]:
            if key not in metadata_level:
                metadata_level[key] = {}
            metadata_level = metadata_level[key]
        metadata_level[keys[-1]] = value
        await self.set(metadata)

    async def delete_value(self, key_path: str) -> None:
        """
        Delete a specific key from the metadata.
        :param key_path: The key path to the value in the metadata.
        """
        metadata = await self.get()
        if not metadata:
            return
        keys = key_path.split(".")
        metadata_level = metadata
        for key in keys[:-1]:
            if key in metadata_level:
                metadata_level = metadata_level[key]
            else:
                return None
        del metadata_level[keys[-1]]
        await self.set(metadata)
