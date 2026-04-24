from agent.agent import run_agent
from trade.arena.arena_client import initialize_arena_client
from trade.finam.finam_client import initialize_finam_client


async def amain():
    await initialize_arena_client()
    await initialize_finam_client()
    await run_agent()



def main():
    import asyncio
    asyncio.run(amain())


if __name__ == '__main__':
    main()
