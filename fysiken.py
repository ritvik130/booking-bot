import datetime
import json
import os
import requests

session = requests.Session()
BASE_URL = "https://fysiken.zoezi.se/api"
NUM_RETRIES = 5

class Fysiken:
    def __init__(self):
        self.config_file = os.environ["CONFIG"]
        user_info = self.get_user_session()

        self.token = user_info["session"]
        self.user_id = user_info["id"]

        self.user_workouts = json.load(open(self.config_file, "r"))
        self.next_available_date = datetime.date.today() + datetime.timedelta(days=8)
        self.available_workouts = self.get_workouts()

    def get_user_session(self):
        username = os.environ["USERNAME"]
        password = os.environ["PASSWORD"]

        cookies = {"login": username, "password": password}
        session_data = session.post(os.path.join(BASE_URL, "v8.0/memberapi/login"), json=cookies)

        return session_data.json()

    def get_workouts(self):
        """Get workouts to sign up for 8 days later"""
        formatted_date = self.next_available_date.strftime("%Y-%m-%d")
        sess = session.get(os.path.join(BASE_URL, f"public/workout/get/all?fromDate={formatted_date}&toDate={formatted_date}"))
        workouts = dict()

        for workout in sess.json()["workouts"]:
            uuid = workout["id"]
            start_time = workout["startTime"]
            bookable = workout["bookableForCustomer"]
            name = workout["workoutType"]["name"]

            if bookable:
                workouts[name] = {
                    "uuid": uuid,
                    "start_time": start_time
                }

        return workouts

    def reserve_workouts(self):
        next_available_weekday = self.next_available_date.strftime("%A").lower()
        for workout in self.user_workouts:
            book = False
            for weekday in workout["weekdays"]:
                if weekday.lower() == next_available_weekday:
                    book = True
                    break

            if book and workout["class_name"] in self.available_workouts:
                for i in range(NUM_RETRIES):
                    sleep(i*2)
                    workout_booking = self.available_workouts[workout["class_name"]]
                    sess = session.post(os.path.join(BASE_URL, f"memberapi/workoutBooking/add?workout={workout_booking['uuid']}&method=trainingcard&user_id={self.user_id}"))
                    res = sess.json()

                    # verify the returned data is successful
                    booking_id = res.get("id", None)
                    booked_user_id = res.get("user_id", None)
                    booked_workout_id = res.get("workout", None)

                    if booked_workout_id == workout_booking['uuid'] and booked_user_id == self.user_id:
                        print(f"Successfully booked {workout['class_name']} on {next_available_weekday} with id {booking_id}")
                        break
                    else:
                        print(f"Failed to book, retrying... \n{res}")


fysiken = Fysiken()
fysiken.reserve_workouts()
