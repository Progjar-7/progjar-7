import threading
import socket
from queue import Queue
from io import StringIO
import json

class ChatPrivate(threading.Thread):
    def __init__(self, addr: tuple = ('127.0.0.1', 0)):
        self.clt = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(addr)
        self.server.listen(1)
        self.groups = {}
        self.locker = threading.Lock()
        threading.Thread.__init__(self)

    def broadcast_all(self, message, room_name):
        if room_name not in self.groups:
            return
        
        with self.locker:
            for client in self.groups[room_name]["clients"]:
                try:
                    client.sendall(message)
                except ConnectionResetError:
                    continue

    def send_single(self, username_destination, username_from, username_to, message):
        # if username_from not in self.groups:
        #     return 
        
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
                client_from = self.groups[username_destination]
                client_from.sendall(bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8"))
            except ConnectionResetError:
                pass

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
                client_from.sendall(bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8"))
            except ConnectionResetError:
                pass

            try:
                client_to = self.groups[username_to]
                client_to.sendall(bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8"))
            except ConnectionResetError:
                pass
    
    def send_file_single(self, username_destination, username_from, username_to, filename, file_content):
        msg_to_send = {
            "tipe_pesan": "PESAN_FILE_PRIVATE",
            "data": {
                "username_pengirim" : username_from,
                "username_penerima": username_to,
                "filename": filename,
                "file_content": file_content,
            },
        }

        jsonized_msg = json.dumps(msg_to_send)
        print(msg_to_send)
        
        with self.locker:
            try:
                client_from = self.groups[username_destination]
                client_from.sendall(bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8"))
            except ConnectionResetError:
                pass

    def send_file_to(self, username_from, username_to, filename, file_content):
        if username_from not in self.groups or username_to not in self.groups:
            return
        
        msg_to_send = {
            "tipe_pesan": "PESAN_FILE_PRIVATE",
            "data": {
                "username_pengirim" : username_from,
                "username_penerima": username_to,
                "filename": filename,
                "file_content": file_content,
            },
        }

        jsonized_msg = json.dumps(msg_to_send)
        print(msg_to_send)
        
        with self.locker:
            try:
                client_from = self.groups[username_from]
                client_from.sendall(bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8"))
            except ConnectionResetError:
                pass

            try:
                client_to = self.groups[username_to]
                client_to.sendall(bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8"))
            except ConnectionResetError:
                pass
            
    def open_connection_for(self, username, client):
        # if username in self.groups:
            # jsonized_msg = json.dumps(
            #     {
            #         "tipe_pesan": "OPEN_KONEKSI_FAIL",
            #         "data": {
            #             "alasan": "User sudah ada"
            #         }
            #     }
            # )

            # return bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8")
        self.groups[username] = client

        jsonized_msg = json.dumps(
            {
                "tipe_pesan": "OPEN_KONEKSI_SUCCESS",
                "data": {
                    "pesan": f"Koneksi dibuka untuk user {username}"
                }
            }
        )

        return bytes(f"{jsonized_msg}\r\n\r\n", encoding="utf-8")
    
    def process_private_client(self, client):
        def recvall(num_bytes, connection) -> str:
            buffer = StringIO()

            while True:
                data = connection.recv(num_bytes)
                if data:
                    print(data)
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

        while True:
            try:
                message = recvall(4096, client)
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

                    elif order == "FILEPRIVATE":
                        username_from = data[1].strip()
                        username_to = data[2].strip()
                        filename = data[3].strip()

                        content_file = StringIO()
                        for m in data[4]:
                            content_file.write(m)

                        content_file_string = content_file.getvalue()

                        self.send_file_to(username_from, username_to, filename, content_file_string)

                    elif order == "SENDFILESINGLE":
                        username_dest = data[1].strip()
                        username_from = data[2].strip()
                        username_to = data[3].strip()
                        filename = data[4].strip()

                        content_file = StringIO()
                        for m in data[5]:
                            content_file.write(m)

                        content_file_string = content_file.getvalue()

                        self.send_file_single(username_dest, username_from, username_to, filename, content_file_string)

            except ConnectionResetError:
                print("Disconnected from the server.")
                break
            except ConnectionAbortedError:
                print("Exit from group")
                break
            except Exception as e:
                print(f"An error occurred in received_message: {e}")
                break

    def run(self):
        print('Server Private is running and listening ...')
        while True:
            client, address = self.server.accept()
            print(f'Connection established with {str(address)}')
            
            client_thread = threading.Thread(target=self.process_private_client, args=(client,))
            client_thread.start()

if __name__ == "__main__":
    server = ChatPrivate('127.0.0.1', 59000)
    server.start()

    print("Ready...")
