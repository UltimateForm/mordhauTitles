import asyncio

from reactivex import Observable
from rcon_listener import RconListener
from os import environ
from rcon import RconContext
import parsers
import logger

DEFAULT_REX_TITLE = "REX"


# doesn't really need to be a class....
# but i had a issue and i was too lazy
class TitleCompute:
    current_rex: str = ""
    rex_tile: str = ""

    def __init__(self):
        self.rex_tile = environ.get("TITLE", DEFAULT_REX_TITLE)

    async def _execute_command(self, command: str):
        async with RconContext() as client:
            await client.execute(command)

    def _sanitize_name(self, name: str):
        return name.replace(f"[{self.rex_tile}]", "").lstrip()

    def _remove_rex(self, playfab_id: str, user_name):
        asyncio.create_task(
            self._execute_command(
                f"renameplayer {playfab_id} {self._sanitize_name(user_name)}"
            )
        )

    def _place_rex(self, playfab_id: str, user_name):
        asyncio.create_task(
            self._execute_command(
                f"renameplayer {playfab_id} [{self.rex_tile}] {self._sanitize_name(user_name)}"
            )
        )

    def _process_killfeed_event(self, event_data: dict[str, str]):
        try:
            killer = event_data.get("userName", "")
            killed = event_data.get("killedUserName", "")
            killer_playfab_id = event_data.get("killerPlayfabId", "")
            killed_playfab_id = event_data.get("killedPlayfabId", "BOT")
            if not killer_playfab_id:
                return
            if not self.current_rex:
                asyncio.create_task(
                    self._execute_command(
                        f"say {killer} has defeated {killed} and claimed the vacant {self.rex_tile} title"
                    )
                )
                self._place_rex(killer_playfab_id, killer)
                self.current_rex = killer_playfab_id
            elif self.current_rex == killed_playfab_id:
                asyncio.create_task(
                    self._execute_command(
                        f"say {killer} has defeated {killed} and claimed his {self.rex_tile} title"
                    )
                )
                self._place_rex(killer_playfab_id, killer)
                self._remove_rex(killed_playfab_id, killed)
                self.current_rex = killer_playfab_id
            elif (
                killer.rstrip().startswith(f"[{self.rex_tile}]")
                and killer_playfab_id != self.current_rex
            ):
                # this is a bug, boy has REX in his name but isn't actually current rex
                self._remove_rex(killer_playfab_id, killer)
        except Exception as e:
            logger.error(f"Failed to process REX tag compute, {str(e)}")

    def process_killfeed_raw_event(self, event: str):
        logger.debug(f"EVENT: {event}")
        (success, event_data) = parsers.parse_event(
            event, parsers.GROK_KILLFEED_EVENT
        )
        if success:
            self._process_killfeed_event(event_data)

    def process_login_raw_event(self, event: str):
        logger.debug(f"EVENT: {event}")
        (success, event_data) = parsers.parse_event(event, parsers.GROK_LOGIN_EVENT)
        if not success:
            return
        event_text = event_data.get("eventText", "").lower()
        if event_text.lower().startswith(
            "logged out"
        ) and self.current_rex == event_data.get("playfabId", None):
            self.current_rex = ""


async def start_migrant_titles(login_observable: Observable[str]):
    rex_compute = TitleCompute()

    killfeed_listener = RconListener(event="killfeed", listening=False)

    killfeed_listener.subscribe(rex_compute.process_killfeed_raw_event)
    login_observable.subscribe(rex_compute.process_login_raw_event)
    await killfeed_listener.start()


if __name__ == "__main__":
    login_listener = RconListener(event="login", listening=False)
    asyncio.run(
        asyncio.gather(login_listener.start(), start_migrant_titles(login_listener))
    )
