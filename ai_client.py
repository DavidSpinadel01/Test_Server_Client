import threading
import time
import openai
from client import Client

class AIClient(Client):
    def __init__(self, mode, interval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.interval = interval
        self.message_count = 0

    def receive_messages(self):
        while True:
            message = receive_message(self.socket)
            if message:
                print(f"Server: {message}")
                self.message_count += 1
                if self.mode == 1 and self.message_count % self.interval == 0:
                    self.respond_to_chat(message)
            else:
                print("Connection closed by the server")
                break

    def respond_to_chat(self, last_message):
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Respond to the following conversation: {last_message}",
            max_tokens=150
        )
        send_message(self.socket, response.choices[0].text.strip())

    def run(self):
        threading.Thread(target=self.receive_messages).start()
        if self.mode == 2:
            while True:
                time.sleep(self.interval)
                self.send_unrelated_message()

    def send_unrelated_message(self):
        prompt = "Say something interesting:"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=150
        )
        send_message(self.socket, response.choices[0].text.strip())

if __name__ == "__main__":
    ai_client = AIClient(mode=1, interval=5)
    ai_client.run()