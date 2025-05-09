from .geoaiagent import doit


async def thisismain():
    await doit()

if __name__ == "__main__":
    import asyncio
    asyncio.run(thisismain())