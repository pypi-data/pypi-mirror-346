# your_package/cli.py
from .core import serve

def main():
    import asyncio
    asyncio.run(serve())
