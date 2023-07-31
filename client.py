import requests
import random
import string
import time
from uuid import uuid4

BASE_URL = "http://web:8000"


class Client:
    @staticmethod
    def generate_random_string(length):
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join((random.choice(letters_and_digits) for i in range(length)))

        return random_string

    def create_entries(self):
        count = random.randint(10, 100)
        entries = []

        for i in range(count):
            uuid = str(uuid4())
            text = self.generate_random_string(16)
            entries.append({"uuid": uuid, "text": text})

        response = requests.post(f"{BASE_URL}/new", json=entries)
        response.raise_for_status()

    @staticmethod
    def get_and_delete_entries():
        response = requests.get(f"{BASE_URL}/count/10")
        response.raise_for_status()

        entries = response.json()["entries"]
        print(f"Deleted {len(entries)} entries")

        for entry in entries:
            uuid = entry["uuid"]
            response = requests.delete(f"{BASE_URL}/{uuid}")
            response.raise_for_status()

    def start_client(self):
        while True:
            self.create_entries()
            self.get_and_delete_entries()
            time.sleep(10)