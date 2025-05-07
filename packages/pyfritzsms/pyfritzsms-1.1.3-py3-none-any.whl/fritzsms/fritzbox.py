import hashlib
import pyotp
from aiohttp import ClientSession
from xml.etree import ElementTree

DATA_URL = "http://{}/data.lua"
LOGIN_URL = "http://{}/login_sid.lua"
TWOFACTOR_URL = "http://{}/twofactor.lua"


class FritzBox:
    def __init__(self, host: str, session: ClientSession):
        self._host = host
        self._session = session
        self._sid = ""
        self._otp = None

    def set_otp(self, otp_secret: str):
        self._otp = pyotp.TOTP(otp_secret)

    def get_otp(self):
        if not self._otp:
            raise RuntimeError("TOTP secret is not set")
        return self._otp.now()

    def _check_status(self, response):
        if response.status != 200:
            raise RuntimeError(f"Unexpected response from FritzBox: {response.status}")

    async def login(self, username: str, password: str):
        async with self._session.get(LOGIN_URL.format(self._host)) as response:
            self._check_status(response)
            text = await response.text()
            tree = ElementTree.fromstring(text)
            challenge = tree.findtext("Challenge")
        md5hash = (
            hashlib.md5((challenge + "-" + password).encode("utf-16le"))
            .hexdigest()
            .lower()
        )
        response = challenge + "-" + md5hash
        async with self._session.post(
            LOGIN_URL.format(self._host),
            data={
                "username": username,
                "response": response,
            },
        ) as response:
            self._check_status(response)
            text = await response.text()
            tree = ElementTree.fromstring(text)
            self._sid = tree.findtext("SID").strip("0")
        return self._sid

    async def logout(self):
        async with self._session.get(
            LOGIN_URL.format(self._host),
            params={
                "sid": self._sid,
                "logout": "1",
            },
        ) as response:
            self._check_status(response)
            text = await response.text()
            tree = ElementTree.fromstring(text)
            self._sid = tree.findtext("SID").strip("0")
        return self._sid

    async def is_otp_configured(self):
        async with self._session.post(
            TWOFACTOR_URL.format(self._host),
            data={
                "sid": self._sid,
                "tfa_googleauth_info": "",
                "no_sidrenew": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        return data["googleauth"]["isConfigured"]

    async def list_sms(self):
        async with self._session.post(
            DATA_URL.format(self._host),
            data={
                "sid": self._sid,
                "page": "smsList",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        messages = data["data"]["smsListData"]["messages"]
        return messages

    async def delete_sms(self, id: int):
        async with self._session.post(
            DATA_URL.format(self._host),
            data={
                "sid": self._sid,
                "page": "smsList",
                "messageId": id,
                "delete": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if "sid" in data:
            self._sid = data["sid"]
        if data["data"]["delete"] != "ok":
            raise RuntimeError("SMS could not be deleted")

    async def send_sms(self, number: str, message: str):
        # initial request to send SMS
        async with self._session.post(
            DATA_URL.format(self._host),
            data={
                "sid": self._sid,
                "page": "smsSendMsg",
                "recipient": number,
                "newMessage": message,
                "apply": "true",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if "sid" in data:
            self._sid = data["sid"]
        if "new_uid" not in data["data"]:
            return True

        # second factor required via TOTP
        new_uid = data["data"]["new_uid"]
        async with self._session.post(
            DATA_URL.format(self._host),
            data={
                "sid": self._sid,
                "page": "smsSendMsg",
                "recipient": number,
                "newMessage": message,
                "new_uid": new_uid,
                "second_apply": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if "sid" in data:
            self._sid = data["sid"]
        if data["data"]["second_apply"] != "twofactor":
            raise RuntimeError("TOTP is not required")

        # check if TOTP is configured and available
        async with self._session.post(
            TWOFACTOR_URL.format(self._host),
            data={
                "sid": self._sid,
                "tfa_googleauth_info": "",
                "no_sidrenew": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if not data["googleauth"]["isConfigured"]:
            raise RuntimeError("TOTP is not configured")
        if not data["googleauth"]["isAvailable"]:
            raise RuntimeError("TOTP is not available")

        # send TOTP
        async with self._session.post(
            TWOFACTOR_URL.format(self._host),
            data={
                "sid": self._sid,
                "tfa_googleauth": self.get_otp(),
                "no_sidrenew": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if data["err"] != 0:
            raise RuntimeError("TOTP is not valid")

        # check if TOTP is active and done
        async with self._session.post(
            TWOFACTOR_URL.format(self._host),
            data={
                "sid": self._sid,
                "tfa_active": "",
                "no_sidrenew": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if not data["active"]:
            raise RuntimeError("TOTP is not active")
        if not data["done"]:
            raise RuntimeError("TOTP is not done")

        # finally send SMS again
        async with self._session.post(
            DATA_URL.format(self._host),
            data={
                "sid": self._sid,
                "page": "smsSendMsg",
                "recipient": number,
                "newMessage": message,
                "new_uid": new_uid,
                "second_apply": "",
                "confirmed": "",
                "twofactor": "",
            },
        ) as response:
            self._check_status(response)
            data = await response.json()
        if "sid" in data:
            self._sid = data["sid"]
        if data["data"]["second_apply"] != "ok":
            raise RuntimeError("TOTP is not ok")
        return new_uid
