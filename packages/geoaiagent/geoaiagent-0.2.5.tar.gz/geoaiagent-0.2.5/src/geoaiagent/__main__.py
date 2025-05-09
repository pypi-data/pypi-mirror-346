import asyncio
from .geoaiagent import doit

async def thisismain():
    await doit()

if __name__ == "__main__":
    asyncio.run(thisismain())