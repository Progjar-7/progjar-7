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

class Gateway(threading.Thread):
    def __init__(self, addr: tuple = ('127.0.0.1', 11111)):
        print(f"Gateway diinisialisasi di {addr}")
        self.addr = addr
        self.realms: Dict = {}
        self.received_messsage = Queue()
        self.locker = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(self.addr)
        self.server_socket.listen(1)

        threading.Thread.__init__(self)
    
    def add_realm(self, realm_name: str) -> str:
        if realm_name in self.realms:
            return json.dumps({
                "tipe_pesan": "GATEWAY_ADD_REALM_FAIL",
                "alasan": "Realm sudah ada"
            })

        private_server = ServerChatPrivate()
        private_server_host, private_server_port = private_server.server.getsockname()
        private_server.start()

        group_server = ServerChatGroup()
        group_server_host, group_server_port = group_server.server.getsockname()
        group_server.start()

        self.realms[realm_name] = {
            "private": {
                "server": private_server,
                "host": private_server_host,
                "port": private_server_port,
                "clients": {}
            },

            "group": {
                "server": group_server,
                "host": group_server_host,
                "port": group_server_port,
                "clients": {}
            }
        }

        return json.dumps({
            "tipe_pesan": "GATEWAY_ADD_REALM_SUKSES",
            "pesan": f"Realm {realm_name} dibuat"
        })

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

    def open_private_connection_for(self, realm_name: str, username: str, client_gateway_connection: socket.socket) -> str:
        if realm_name not in self.realms:
            return json.dumps({
                "tipe_pesan": "GATEWAY_OPEN_PRIVATE_FAIL",
                "alasan": "Realm tidak ada"
            })
                
        host = self.realms[realm_name]["private"]["host"]
        port = self.realms[realm_name]["private"]["port"]

        private_client = ClientChatPrivate(host=host, port=port)
        private_client.start_chat()

        self.realms[realm_name]["private"]["clients"][username] = private_client

        listener_thread = threading.Thread(target=self.listen, args=(private_client.received_queue, client_gateway_connection))
        listener_thread.start()

        private_client.send_message(f"OPENPRIVATE {username}\r\n\r\n")

        return json.dumps({
            "tipe_pesan": "GATEWAY_OPEN_PRIVATE_SUKSES",
            "pesan": "User berhasil online"
        })

    def send_msg_internal_realm(self, realm_name: str, username_from: str, username_to: str, msg: str) -> str:
        if realm_name not in self.realms:
            return json.dumps({
                "tipe_pesan": "GATEWAY_SEND_PRIVATE_FAIL",
                "alasan": "Realm tidak ada"
            })
        
        if username_from not in self.realms[realm_name]["private"]["clients"]:
            return json.dumps({
                "tipe_pesan": "GATEWAY_SEND_PRIVATE_FAIL",
                "alasan": "User pengirim tidak ditemukan"
            })
        
        private_client = self.realms[realm_name]["private"]["clients"][username_from]
        private_client.send_message(f"SENDPRIVATE {username_from} {username_to} {msg}\r\n\r\n")

        return json.dumps({
            "tipe_pesan": "GATEWAY_SEND_PRIVATE_SUKSES",
            "pesan": "Pesan dikirimkan"
        })


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
                    
                    if order == "ADDREALM":
                        realm_name = data[1].strip()

                        result = self.add_realm(realm_name=realm_name)
                        print(result)
                        client.sendall(f"{result}\r\n\r\n".encode())

                    elif order == "OPENPRIVATE":
                        realm_name = data[1].strip()
                        username = data[2].strip()

                        result = self.open_private_connection_for(realm_name=realm_name, username=username, client_gateway_connection=client)
                        print(result)
                        client.sendall(f"{result}\r\n\r\n".encode())

                    elif order == "SENDPRIVATESINGLE":
                        realm_name = data[1].strip()
                        username_from = data[2].strip()
                        username_to = data[3].strip()

                        msg = ""
                        for w in data[4:]:
                            msg = "{} {}".format(msg, w)

                        result = self.send_msg_internal_realm(realm_name=realm_name, username_from=username_from, username_to=username_to, msg=msg)
                        print(result)
                        client.sendall(f"{result}\r\n\r\n".encode())

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

        while True:
            client, address = self.server_socket.accept()
            print(f'Connection established in gateway with {str(address)}')
            
            client_thread = threading.Thread(target=self.process_request, args=(client,))
            client_thread.start()

if __name__ == "__main__":
    gateway = Gateway()
    gateway.start()
    print("Gateway open...")

