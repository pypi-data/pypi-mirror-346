# coding: utf-8

import os

from typing import Union, Optional

from protean.api_client import ApiClient
from protean.configuration import Configuration
from protean.api import ChatApi, DatasetApi, DataApi, UserApi


class Protean(ApiClient):
    chat: ChatApi
    dataset: DatasetApi
    data: DataApi
    user: UserApi

    def __init__(
            self,
            *,
            api_key: Optional[str] = None,
            base_url: Union[str, None] = None,
    ) -> None:
        if api_key is None:
            api_key = os.environ.get("PROTEAN_API_KEY")
        if api_key is None:
            raise ValueError(
                "The api_key client option must be set either by passing api_key to the client or by setting the PROTEAN_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("PROTEAN_BASE_URL")
        if base_url is None:
            raise ValueError(
                "The base_url client option must be set either by passing base_url to the client or by setting the PROTEAN_BASE_URL environment variable"
            )
        self.base_url = base_url

        self.chat = ChatApi(self)
        self.dataset = DatasetApi(self)
        self.data = DataApi(self)
        self.user = UserApi(self)

        configuration = Configuration(
            host=base_url,
            access_token=api_key
        )

        super().__init__(
            configuration=configuration
        )
