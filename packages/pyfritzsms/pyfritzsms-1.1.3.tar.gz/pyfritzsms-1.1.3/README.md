# Python library to send SMS via AVM FRITZ!Box

## Requirements

- AVM FRITZ!Box with internal or USB cellular modem and SMS enabled SIM card.
- User account with app-based second-factor enabled and TOTP secret available.

## Example usage

```python
from fritzsms.fritzbox import FritzBox
from aiohttp import ClientSession
import asyncio


async def async_main_test():
    async with ClientSession() as session:
        box = FritzBox("fritz.box", session)
        box.set_otp("TOTP-secret")
        print(box.get_otp()) # for confirmation during setup
        await box.login("username", "password")
        uid = await box.send_sms("mobile-number", "Hello World!")
        await box.delete_sms(uid)
        print(await box.list_sms())
        await box.logout()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_main_test())
```
