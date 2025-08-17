import threading
import time

import requests

from Settings.SettingsHandler import settings


class APIClientWorker:
    _instance = None  # Store the single instance of the class
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        """Override __new__ to ensure only one instance of APIClientWorker."""
        with cls._lock:
            if not cls._instance:
                cls._instance = super(APIClientWorker, cls).__new__(cls, *args, **kwargs)
                cls._instance._initialize()  # Initialize the instance only once
            return cls._instance

    def _initialize(self):
        """Initialize settings and attributes only once."""
        self.url = settings["api_endpoint"]
        self.max_retries = settings["api_max_retries"]
        self.retry_delay = settings["api_retry_delay"]
        self.debug = settings["debug"]
        self.session = requests.Session()
        self.response_data = None
        print("Created APIClientWorker\n------------")

    @classmethod
    def Instance(cls):
        """Return the Singleton instance."""
        return cls()

    def debug_log(self, message):
        if self.debug:
            print(message)

    def get_response_with_retries(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.debug_log(f"Attempting to send request to {self.url}... (Retry #{retries + 1})")
                response = self.session.get(self.url)

                if response.status_code == 200:
                    self.debug_log("Successfully received response.")
                    return response.text
                else:
                    self.debug_log(f"Failed to get a valid response (status code {response.status_code})")
                    retries += 1
                    time.sleep(self.retry_delay)
            except requests.exceptions.RequestException as e:
                self.debug_log(f"Request failed: {e}")
                retries += 1
                time.sleep(self.retry_delay)  # Time until try again
                self.debug_log(f"Trying again in: {self.retry_delay} seconds")

        self.debug_log(f"Failed to get a valid response after {self.max_retries} retries.")

    def request_api_call(self):
        self.response_data = self.get_response_with_retries()

    def get_response_data(self):
        return self.response_data

    def close_session(self):
        self.session.close()


# Example usage of APIClientWorker Singleton
if __name__ == "__main__":
    api_worker = APIClientWorker.Instance()  # Access Singleton via Instance
    api_worker.request_api_call()
    response = api_worker.get_response_data()
    if response:
        print(f"Final API response: {response}")
    else:
        print("Failed to get a response from the API.")
    api_worker.close_session()
