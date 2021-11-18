from locust import HttpUser, task, between
from datetime import date
import random
import os 


class QuickstartUser(HttpUser):
    wait_time = between(1, 4)

    @task
    def simple(self):
        colors = ["red", "green", "blue", "black", "orange", "green", "yellow", "pink", "white", "purple"]
        color = random.choice(colors)
        self.client.get("/color?=%s" %(color))
        self.client.get("/color")

        customers=["gold", "silver", "platinum"]
        customer=random.choice(customers)
        self.client.get("/customer?=%s" %(customer))
        self.client.get("/customer")