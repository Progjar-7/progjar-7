import threading
import socket
from queue import Queue
import json

class ChatPrivate:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clt = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(1)
        self.groups = {}
        self.locker = threading.Lock()


    def broadcast_all(self, message, room_name):
        if room_name not in self.groups:
            return
        
        with self.locker:
            for client in self.groups[room_name]["clients"]:
                try:
                    client.sendall(message)
                except ConnectionResetError:
                    continue

    def send_to(self, username_from, username_to, message):
        if username_from not in self.groups or username_to not in self.groups:
            return
        
        msg_to_send = {
            "tipe_pesan": "PESAN_PRIVATE",
            "data": {
                "username_pengirim" : username_from,
                "username_penerima": username_to,
                "pesan": message,
            },
        }

        jsonized_msg = json.dumps(msg_to_send)
        print(msg_to_send)
        
        with self.locker:
            try:
                client_from = self.groups[username_from]
                client_from.sendall(bytes(jsonized_msg, encoding="utf-8"))
            except ConnectionResetError:
                pass

            try:
                client_to = self.groups[username_to]
                client_to.sendall(bytes(jsonized_msg, encoding="utf-8"))

            except ConnectionResetError:
                pass
            
    def open_connection_for(self, username, client):
        if username in self.groups:
            jsonized_msg = json.dumps(
                {
                    "tipe_pesan": "OPEN_KONEKSI_FAIL",
                    "data": {
                        "alasan": "User sudah ada"
                    }
                }
            )

            return bytes(jsonized_msg, encoding="utf-8")

        self.groups[username] = client

        jsonized_msg = json.dumps(
            {
                "tipe_pesan": "OPEN_KONEKSI_SUCCESS",
                "data": {
                    "pesan": f"Koneksi dibuka untuk user {username}"
                }
            }
        )

        return bytes(jsonized_msg, encoding="utf-8")
    
    def process_private_client(self, client):
        while True:
            try:
                message = client.recv(4096).decode()
                if message:
                    data = message.split(" ")
                    order = data[0].strip()

                    if order == "OPENPRIVATE":
                        username = data[1].strip()
                        result = self.open_connection_for(username, client)
                        client.send(result)

                    elif order == "SENDPRIVATE":
                        username_from = data[1].strip()
                        username_to = data[2].strip()

                        msg = ""
                        for w in data[3:]:
                            msg = "{} {}".format(msg, w)

                        self.send_to(username_from, username_to, msg)
            except ConnectionResetError:
                print("Disconnected from the server.")
                break
            except ConnectionAbortedError:
                print("Exit from group")
                break
            except Exception as e:
                print(f"An error occurred in received_message: {e}")
                break

    def start(self):
        print('Server is running and listening ...')
        while True:
            client, address = self.server.accept()
            print(f'Connection established with {str(address)}')
            
            client_thread = threading.Thread(target=self.process_private_client, args=(client,))
            client_thread.start()

if __name__ == "__main__":
    server = ChatPrivate('127.0.0.1', 59000)
    server.start()
