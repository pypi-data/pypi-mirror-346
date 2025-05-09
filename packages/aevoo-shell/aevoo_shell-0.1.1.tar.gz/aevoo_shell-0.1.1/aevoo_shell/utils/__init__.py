import asyncio


def async_run(cor):
    return asyncio.get_event_loop().run_until_complete(cor)
