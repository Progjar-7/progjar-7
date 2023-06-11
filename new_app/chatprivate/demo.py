from . import client
from queue import Queue
import threading


chat = client.ChatPrivateClient()


def listen(queue: Queue):
    try:
        while True:
            if not queue.empty():
                message = queue.get()
                print(message)  # main main disini
    except ConnectionResetError:
        print("Disconnected from the server.")
    except ConnectionAbortedError as e:
        print("Exit from group")
    except Exception as e:
        print(f"An error occurred in received_message: {e}")


if __name__ == "__main__":
    receiver_thread = threading.Thread(target=listen, args=(chat.received_queue,))
    receiver_thread.start()

    while True:
        cmd = input()
        chat.send_message(cmd)
