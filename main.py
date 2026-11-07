
import datetime
import time
from zoneinfo import ZoneInfo

from fysiken import Fysiken

SWEDEN = ZoneInfo("Europe/Stockholm")


def wait_until_release():

    now = datetime.datetime.now(SWEDEN)

    release = now.replace(
        hour=12,
        minute=0,
        second=0,
        microsecond=0
    )

    while True:
        remaining = (
            release - datetime.datetime.now(SWEDEN)
        ).total_seconds()

        if remaining <= 0:
            break

        if remaining > 1:
            time.sleep(remaining - 0.5)
        else:
            time.sleep(0.01)


def main():

    now = datetime.datetime.now(SWEDEN)

    if not (now.hour == 11 and now.minute >= 57 and now.minute <= 59):

    fysiken = Fysiken()

    wait_until_release()

    fysiken.next_available_date = (
        datetime.datetime.now(SWEDEN).date()
        + datetime.timedelta(days=8)
    )

    fysiken.available_workouts = fysiken.get_workouts()

    fysiken.reserve_workouts()


if __name__ == "__main__":
    main()
