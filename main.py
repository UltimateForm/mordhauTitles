import asyncio
import logger
from dotenv import load_dotenv
from persistent_titles import start_persistent_titles
from migrant_titles import start_migrant_titles
from rcon_listener import RconListener

load_dotenv()


async def main():
    login_listener = RconListener(event="login", listening=False)
    await asyncio.gather(
        login_listener.start(),
        start_migrant_titles(login_listener),
        start_persistent_titles(login_listener),
    )


if __name__ == "__main__":
    logger.use_date_time_logger()
    logger.info("INIT")
    asyncio.run(main())
    logger.info("END")
