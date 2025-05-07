# your_package/cli.py
from .core import main
def run():
    import asyncio
    asyncio.run(main())
