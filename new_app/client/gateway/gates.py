import socket
import threading
import json
from io import StringIO
from typing import Dict
from server_private import ChatPrivate as ServerChatPrivate
from client_private import ChatPrivateClient as ClientChatPrivate
from server_group import ChatGroup as ServerChatGroup
from client_group import ChatGroupClient as ClientChatGroup
from queue import Queue

class Gates(threading.Thread):
    def __init__(self, addr: tuple = ('127.0.0.1', 11111)):
        print(f"Gateway diinisialisasi di {addr}")
        self.addr = addr
        self.private_users: Dict = {}
        self.local_private_chat_server = ServerChatPrivate()

        host, port = self.local_private_chat_server.server.getsockname()

        self.local_private_chat_host = host
        self.local_private_chat_port = port

        self.received_messsage = Queue()
        self.locker = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(1)

        threading.Thread.__init__(self)

    def listen(self, queue: Queue, connection: socket.socket):
        print("Listening the queue...")
        try:
            while True:
                if not queue.empty():
                    with self.locker:
                        rcv = queue.get()
                        connection.sendall(rcv.encode())
        except ConnectionResetError:
            print("Gateway listen: Disconnected from the server.")
        except ConnectionAbortedError as e:
            print("Gateway listen: Exit from group")
        except Exception as e:
            print(f"Gateway listen: An error occurred in received_message: {e}")


    def open_connection(self, username: str, client_connection: socket.socket) -> str:
        private_client = ClientChatPrivate(host=self.local_private_chat_host, port=self.local_private_chat_port)
        private_client.start_chat()

        private_client.send_message(f"OPENPRIVATE {username}")

        listener_thread = threading.Thread(target=self.listen, args=(private_client.received_queue, client_connection))
        listener_thread.start()

        self.private_users[username] = {
            "client": private_client,
            "is_diff": False
        }

        return "INTERNAL OK"
    
    def open_connection_external(self, username: str, host: str, port: int, client_connection: socket.socket) -> str:
        private_client = ClientChatPrivate(host=host, port=port)
        private_client.start_chat()

        listener_thread = threading.Thread(target=self.listen, args=(private_client.received_queue, client_connection))
        listener_thread.start()

        self.private_users[username] = {
            "server": None,
            "client": private_client,
            "is_diff": True
        }

        return "EXTERNAL OK"

    def open_connection_multi(self, username: str, host: str, port: int, client_connection: socket.socket) -> str:
        private_client = ClientChatPrivate(host=host, port=port)
        private_client.start_chat()

        private_client.send_message(f"OPENPRIVATE {username}")

        listener_thread = threading.Thread(target=self.listen, args=(private_client.received_queue, client_connection))
        listener_thread.start()

        self.private_users[username] = {
            "client": private_client,
            "is_diff": False
        }

        return "MULTI OK"

    def send_message(self, username_from: str, username_to: str, msg: str) -> str:
        user_from = self.private_users[username_from]["client"]
        user_to = self.private_users[username_to]

        user_from.send_message(f"SENDPRIVATESINGLE {username_from} {username_from} {username_to} {msg}")
        if user_to["is_diff"]:
            user_to["client"].send_message(f"CHAT_EKSTERNAL {username_from} {username_to} {msg}\r\n\r\n")
        else:
            user_to["client"].send_message(f"SENDPRIVATESINGLE {username_to} {username_from} {username_to} {msg}")
        
        return "Terkirim"
    
    def send_file(self, username_from: str, username_to: str, filename: str, content_file: str):
        user_from = self.private_users[username_from]["client"]
        user_to = self.private_users[username_to]

        user_from.send_message(f"SENDFILESINGLE {username_from} {username_from} {username_to} {filename} {content_file}")
        if user_to["is_diff"]:
            user_to["client"].send_message(f"FILE_EKSTERNAL {username_from} {username_to} {filename} {content_file}\r\n\r\n")
        else:
            user_to["client"].send_message(f"SENDFILESINGLE {username_to} {username_from} {username_to} {filename} {content_file}")
        
        return "File Terkirim"


    def process_request(self, client: socket.socket):
        def recvall(num_bytes, connection: socket.socket) -> str:
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
                        result = self.open_connection(username=username, client_connection=client)
                        print(result)
                    
                    elif order == "OPENPRIVATEEXTERNAL":
                        username = data[1].strip()
                        host = data[2].strip()
                        port = int(data[3].strip())

                        result = self.open_connection_external(username=username, host=host, port=port, client_connection=client)
                        print(result)

                    elif order == "OPENPRIVATEMULTI":
                        username = data[1].strip()
                        host = data[2].strip()
                        port = int(data[3].strip())

                        result = self.open_connection_multi(username=username, host=host, port=port, client_connection=client)
                        print(result)

                    elif order == "SENDPRIVATE":
                        username_from = data[1].strip()
                        username_to = data[2].strip()

                        msg = ""
                        for w in data[3:]:
                            msg = "{} {}".format(msg, w)

                        result = self.send_message(username_from=username_from, username_to=username_to, msg=msg)
                        print(result)

                    elif order == "FILEPRIVATE":
                        username_from = data[1].strip()
                        username_to = data[2].strip()
                        filename = data[3].strip()

                        content_file = StringIO()
                        for m in data[4]:
                            content_file.write(m)

                        content_file_string = content_file.getvalue()
                        result = self.send_file(username_from=username_from, username_to=username_to, filename=filename, content_file=content_file_string)
                        print(result)


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
        print('Server is running and listening ...')
        self.local_private_chat_server.start()

        while True:
            client, address = self.server_socket.accept()
            print(f'Connection established in gateway with {str(address)}')
            
            client_thread = threading.Thread(target=self.process_request, args=(client,))
            client_thread.start()


if __name__ == "__main__":
    gateway = Gates()
    gateway.start()
    print("Gateway open...")