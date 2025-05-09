from .geoaiagent import doit
import asyncio


def thisismain():
    asyncio.run(doit())
    
    
if __name__ == "__main__":

    asyncio.run(thisismain())