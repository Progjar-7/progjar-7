import threading
import socket
from io import StringIO
from queue import Queue


class ChatClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 59000))
        self.message_queue = Queue()
        self.received_queue = Queue()
        self.locker = threading.Lock()

    def recvall(self, num_bytes) -> str:
        buffer = StringIO()

        while True:
            data = self.client.recv(num_bytes)
            if data:
                d = data.decode()
                buffer.write(d)

                if len(data) < num_bytes:
                    break
                    
                if d.endswith("\r\n\r\n"):
                    break
            else:
                break
        
        result = buffer.getvalue()
        stripped_result = result.strip("\r\n\r\n")

        return stripped_result

    def receive_messages(self):
        try:
            while True:
                message = self.recvall(4096)
                if message:
                    print(message)
                    self.received_queue.put(message)
        except ConnectionResetError:
            print("Disconnected from the server.")
        except ConnectionAbortedError as e:
            print("Exit from group |", e)
        except Exception as e:
            print(f"An error occurred in received_message: {e}")
        finally:
            self.client.close()

    def send_message(self, message):
        try:
            with self.locker:
                self.message_queue.put(f"{message}\n\n")
        except Exception as e:
            print(f"An error occurred in send_message: {e}")

    def process_messages(self):
        try:
            while True:
                with self.locker:
                    if not self.message_queue.empty():
                        message = self.message_queue.get()

                        if "EXIT" in message:
                            self.client.sendall(message.encode('utf-8'))
                            break
                        else:
                            self.client.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"An error occurred in process_messages: {e}")
        finally:
            self.client.close()

    def start_chat(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        send_thread = threading.Thread(target=self.process_messages)
        send_thread.start()

if __name__ == "__main__":
    client = ChatClient() # alias + roomname gausah diliat dulu
    client.start_chat()

    while True:
        msg = input()
        client.send_message(msg)
