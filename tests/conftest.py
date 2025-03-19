# import pytest
# import asyncio
#
# @pytest.fixture(scope="function")  # Явно указываем область видимости
# async def event_loop():
#     loop = await asyncio.get_event_loop()
#     await loop
#     loop.close()