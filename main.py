import datetime
import time
from zoneinfo import ZoneInfo

from fysiken import Fysiken

SWEDEN = ZoneInfo("Europe/Stockholm")

WINDOW_START = (11, 30)                       
RELEASE = (12, 0)                             
LOGIN_LEAD = datetime.timedelta(seconds=60)   
LATE_GRACE = datetime.timedelta(minutes=10)  


def today_at(hour, minute=0):
    return datetime.datetime.now(SWEDEN).replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )


def sleep_until(target):
    while True:
        remaining = (target - datetime.datetime.now(SWEDEN)).total_seconds()
        if remaining <= 0:
            return
        if remaining > 1:
            time.sleep(remaining - 0.5)
        else:
            time.sleep(0.01)


def main():
    print("Main function started")
    now = datetime.datetime.now(SWEDEN)
    print("Current Swedish time:", now)

    release = today_at(*RELEASE)
    window_start = today_at(*WINDOW_START)

    if not (window_start <= now <= release + LATE_GRACE):
        print("Outside booking window, exiting")
        return

    # Wait, then log in shortly before release so the session is fresh
    sleep_until(release - LOGIN_LEAD)

    print("Starting Fysiken bot...")
    fysiken = Fysiken()
    print("Fysiken authentication successful.")

    # Returns immediately if we're already past noon (late start)
    sleep_until(release)

    fysiken.next_available_date = (
        datetime.datetime.now(SWEDEN).date()
        + datetime.timedelta(days=8)
    )

    fysiken.available_workouts = fysiken.get_workouts()
    print("Fetched workouts:", fysiken.available_workouts)
    fysiken.reserve_workouts()


if __name__ == "__main__":
    main()