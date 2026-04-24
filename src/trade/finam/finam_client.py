from datetime import datetime
from symtable import Symbol

from config import MOSCOW_TZ, FINAM_API_KEY, FINAM_ACCOUNT_ID
from trade.finam.base import TokenManager, HttpxClient, RequestMethod
from trade.finam.models import OrderState, ErrorModel, TimeFrame, BarsResponse, QuoteResponse, GetAccountResponse, \
    GetTradesResponse, OrderCreateRequest, FinamDecimal, Side


class FinamClient:
    def __init__(self, api_key, account_id, url: str = "https://api.finam.ru/v1"):
        self.token_manager = TokenManager(api_key)
        self.httpx_client = HttpxClient(self.token_manager, url=url)
        self.account_id = account_id

    @classmethod
    async def create(cls, api_key, account_id):
        instance = cls(api_key, account_id)
        await instance._refresh_jwt_token()
        return instance

    async def _refresh_jwt_token(self):
        """Create new JWT session and update token"""
        response, ok = await self.httpx_client._exec_request(
            RequestMethod.POST,
            "/sessions",
            payload={"secret": self.token_manager.token},
        )
        if not ok:
            raise ValueError(response.get("message", "Failed to authenticate"))

        jwt_token = response["token"]
        self.token_manager.set_jwt_token(jwt_token)

    """ Helper """

    async def _exec_request(self, method: RequestMethod, url: str, **kwargs) -> dict:
        # Ensure JWT token is valid before making request
        if self.token_manager.is_token_expired:
            await self._refresh_jwt_token()

        response, ok = await self.httpx_client._exec_request(method, url, **kwargs)

        if not ok:
            err = ErrorModel(**response)
            raise ValueError(
                f"code={err.code} | message={err.message} | details={err.details}"
            )
        return response

    """ Аккаунт """

    async def get_account(self):
        account_client = self.client.account
        return GetAccountResponse(
            **await self._exec_request(
                RequestMethod.GET, f"{account_client._url}/{self.account_id}"
            )
        )

    async def get_trades(
        self, start_time: datetime, end_time: datetime, limit: int
    ):
        return GetTradesResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/accounts/{self.account_id}/trades",
                params={
                    "limit": limit,
                    "interval.start_time": start_time.astimezone(MOSCOW_TZ).isoformat(),
                    "interval.end_time": end_time.astimezone(MOSCOW_TZ).isoformat(),
                },
            )
        )

    """ Market Data """

    async def get_bars(
            self,
            symbol: str,
            start_time: datetime,
            end_time: datetime,
            timeframe: TimeFrame,
    ):
        return BarsResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/instruments/{symbol}/bars",
                params={
                    "timeframe": timeframe.value,
                    "interval.start_time": start_time.astimezone(MOSCOW_TZ).isoformat(),
                    "interval.end_time": end_time.astimezone(MOSCOW_TZ).isoformat(),
                },
            )
        )

    async def get_last_quote(self, symbol: str):
        return QuoteResponse(
            **await self._exec_request(
                RequestMethod.GET,
                f"/instruments/{symbol}/quotes/latest",
            )
        )

    """ Orders """

    async def place_order(self, symbol: Symbol, quantity: int, side: Side):
        """Выставление биржевой заявки"""
        return OrderState(**await self._exec_request(
            RequestMethod.POST,
            f"/{self.account_id}/orders",
            payload={
                "quantity.value": quantity,
                "symbol": symbol,
                "side": side
            },
        ))


finam_client: FinamClient | None = None


async def initialize_finam_client():
    """Initialize global Finam client at service startup"""
    global finam_client

    if not FINAM_API_KEY or not FINAM_ACCOUNT_ID:
        raise ValueError(
            "Missing required env variables: FINAM_API_KEY and FINAM_ACCOUNT_ID are required"
        )

    finam_client = await FinamClient.create(
        api_key=FINAM_API_KEY,
        account_id=FINAM_ACCOUNT_ID
    )


def get_finam_client() -> FinamClient:
    return finam_client
