from locust import HttpUser, task, between
from datetime import date
import random
import os 


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)

    @task
    def home_page(self):
        self.client.get("/")

