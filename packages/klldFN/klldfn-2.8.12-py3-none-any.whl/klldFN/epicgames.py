"""Module for interacting with Epic Games API for user authentication and information."""
import aiohttp
import asyncio
import json
import os
import sys

# Constants
SWITCH_TOKEN = "OThmN2U0MmMyZTNhNGY4NmE3NGViNDNmYmI0MWVkMzk6MGEyNDQ5YTItMDAxYS00NTFlLWFmZWMtM2U4MTI5MDFjNGQ3"
IOS_TOKEN = "M2Y2OWU1NmM3NjQ5NDkyYzhjYzI5ZjFhZjA4YThhMTI6YjUxZWU5Y2IxMjIzNGY1MGE2OWVmYTY3ZWY1MzgxMmU="

class EpicUser:
    def __init__(self, data: dict = {}):
        self.raw = data

        self.access_token = data.get("access_token", "")
        self.expires_in = data.get("expires_in", 0)
        self.expires_at = data.get("expires_at", "")
        self.token_type = data.get("token_type", "")
        self.refresh_token = data.get("refresh_token", "")
        self.refresh_expires = data.get("refresh_expires", "")
        self.refresh_expires_at = data.get("refresh_expires_at", "")
        self.account_id = data.get("account_id", "")
        self.client_id = data.get("client_id", "")
        self.internal_client = data.get("internal_client", False)
        self.client_service = data.get("client_service", "")
        self.display_name = data.get("displayName", "")
        self.app = data.get("app", "")
        self.in_app_id = data.get("in_app_id", "")

    async def get_displayName(self) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method="GET",
                url="https://account-public-service-prod03.ol.epicgames.com/"
                f"account/api/public/account/displayName/{self.display_name}",
                headers={"Authorization": f"bearer {self.access_token}"},
            ) as request:
                data = await request.json()

        return data["displayName"]

class epicgames:
    """To Interact with Epicgames API's For User Info!"""

    async def get_access_token() -> str:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {SWITCH_TOKEN}",
                },
                data={
                    "grant_type": "client_credentials",
                },
            ) as response:
                data = await response.json()
        return data["access_token"]

    async def create_device_code() -> tuple:
        access_token = await epicgames.get_access_token()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/deviceAuthorization",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            ) as response:
                data = await response.json()

        return data["verification_uri_complete"], data["device_code"]

    async def wait_for_device_code_completion(code: str, timeout: int = 90) -> EpicUser:
        async def fetch_token():
            while True:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                        headers={
                        "Authorization": f"basic {SWITCH_TOKEN}",
                        "Content-Type": "application/x-www-form-urlencoded",
                        },
                        data={"grant_type": "device_code", "device_code": code},
                    ) as request:
                        token = await request.json()

                    if request.status == 200:
                        return token
                    else:
                        if (
                            token["errorCode"]
                            == "errors.com.epicgames.account.oauth.authorization_pending"
                        ):
                            pass
                        elif token["errorCode"] == "errors.com.epicgames.not_found":
                            pass
                        elif token["errorCode"] == "errors.com.epicgames.common.slow_down":
                            # Handle the rate limit error silently
                            pass
                        else:
                            print(json.dumps(token, sort_keys=False, indent=4))

                    await asyncio.sleep(5)
        

        try:
            token = await asyncio.wait_for(fetch_token(), timeout=timeout)
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError("Canceled Login")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange",
                headers={"Authorization": f"bearer {token['access_token']}"},
            ) as request:
                exchange = await request.json()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url="https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token",
                headers={
                    "Authorization": f"basic {IOS_TOKEN}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "exchange_code", "exchange_code": exchange["code"]},
            ) as request:
                auth_information = await request.json()

                return EpicUser(data=auth_information)