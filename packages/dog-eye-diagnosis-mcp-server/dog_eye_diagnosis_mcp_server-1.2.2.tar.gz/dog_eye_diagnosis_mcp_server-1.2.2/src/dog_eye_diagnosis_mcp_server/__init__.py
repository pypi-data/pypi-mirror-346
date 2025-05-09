
from .server import server

def main():
    import asyncio
    asyncio.run(server())


if __name__ == "__main__":
    main()
