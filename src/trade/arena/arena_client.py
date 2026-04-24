from datetime import datetime

from config import FINAM_ARENA_API_KEY, FINAM_ARENA_ACCOUNT_ID, FINAM_ARENA_URL
from trade.finam.base import RequestMethod
from trade.finam.finam_client import FinamClient
from trade.arena.models import AccountResponse, OrderResponse, TradesResponse
from trade.finam.models import OrderCreateRequest


class ArenaClient(FinamClient):
    def __init__(self, api_token: str, account_id: int, **kwargs):
        super().__init__(api_token, account_id, url=FINAM_ARENA_URL, **kwargs)

    async def get_account(self) -> AccountResponse:
        return AccountResponse(
            **await self._exec_request(RequestMethod.GET, f"/accounts/{self.account_id}")
        )

    async def get_trades(
        self,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        limit: int | None = None,
    ) -> TradesResponse:
        params = {}
        if start_time:
            params["interval.start_time"] = start_time.isoformat()
        if end_time:
            params["interval.end_time"] = end_time.isoformat()
        if limit is not None:
            params["limit"] = limit
        return TradesResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/accounts/{self.account_id}/trades",
                params=params,
            )
        )

    async def place_order(self, order: OrderCreateRequest) -> OrderResponse:
        return OrderResponse(
            **await self._exec_request(
                RequestMethod.POST,
                f"/accounts/{self.account_id}/orders",
                payload=order.model_dump(mode="json"),
            )
        )

arena_client: ArenaClient | None = None


async def initialize_arena_client():
    """Initialize global Finam client at service startup"""
    global arena_client

    if not FINAM_ARENA_API_KEY or not FINAM_ARENA_ACCOUNT_ID:
        raise ValueError(
            "Missing required env variables: FINAM_API_KEY and FINAM_ACCOUNT_ID are required"
        )

    arena_client = await ArenaClient.create(
        api_key=FINAM_ARENA_API_KEY,
        account_id=FINAM_ARENA_ACCOUNT_ID
    )


def get_arena_client() -> ArenaClient:
    return arena_client
