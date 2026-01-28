import random
from locust import HttpUser, task, between

class DateCalculatorUser(HttpUser):
    # Wait time between requests (simulates a real human thinking time)
    # If testing pure API throughput (machine-to-machine), you can remove this or set to 0
    wait_time = between(0.5, 2)

    @task(3) # Weight of 3: Users do this 3x more often
    def get_weekday_cached(self):
        # This requests the SAME date. After the first hit, 
        # this tests your Caching layer speed (Redis/Memory).
        self.client.get(
            "/api/v1/dates/weekday", 
            params={"year": 2025, "month": 1, "day": 15},
            name="/weekday (cached)"
        )

    @task(1) # Weight of 1
    def get_weekday_random(self):
        # This requests RANDOM dates.
        # This bypasses cache and tests your CPU/Calculation speed.
        year = random.randint(1900, 2100)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        self.client.get(
            "/api/v1/dates/weekday", 
            params={"year": year, "month": month, "day": day},
            name="/weekday (random)"
        )

    @task(1)
    def get_mid_saturdays(self):
        # Tests the heavier loop calculation
        self.client.get(
            "/api/v1/dates/mid-saturdays",
            params={"start_date": "2020-01-01", "end_date": "2030-12-31"},
            name="/mid-saturdays"
        )