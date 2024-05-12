import argparse
import threading
import time
from message_protocol import receive_message, send_message
from openai import OpenAI

client = OpenAI()
from client import Client

class AIClient(Client):
    def __init__(self, mode, interval, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mode = mode
        self.interval = interval
        self.messages = list()

    def receive_messages(self):
        while True:
            message = receive_message(self.socket)
            if message:
                print(f"Server: {message}")
                self.messages.append(message)
                if self.mode == 1 and len(self.messages) == self.interval == 0:
                    self.respond_to_chat()
            else:
                print("Connection closed by the server")
                break

    def respond_to_chat(self):
        if not self.messages:
            return
        
        response = client.chat.completions.create(model="gpt-4-turbo",
            messages=[{'role': 'user', 'content': m} for m in self.messages],
            max_tokens=500)
        self.messages = list()
        print(f'{response.choices[0].message.role}: {response.choices[0].message.content}')
        send_message(self.socket, f'{response.choices[0].message.role}: {response.choices[0].message.content}')

    def run(self):
        threading.Thread(target=self.receive_messages).start()
        if self.mode == 2:
            while True:
                time.sleep(self.interval)
                self.respond_to_chat()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure bot response options")
    parser.add_argument("--mode", "-m", choices=["lines", "seconds"], help="Choose response mode", default="lines")
    parser.add_argument("--interval", "-i", type=int, help="Interval (in seconds or lines) for response", default=5)
    args = parser.parse_args()
    
    ai_client = AIClient(mode=(1 if args.mode == "lines" else 2), interval=args.interval)
    ai_client.run()