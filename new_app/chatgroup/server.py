import threading
import socket
import io

class ChatGroup:
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
                client.sendall(message)

    def create_group(self, room_name):
        if room_name in self.groups:
            return "Room sudah ada"

        self.groups[room_name] = {'clients': [], 'aliases': []}

        return "Room terbuat"
    
    def join_group(self, room_name, username, client):
        if room_name not in self.groups:
            return "Room tidak ditemukan"
        
        self.groups[room_name]["clients"].append(client)
        self.groups[room_name]["aliases"].append(username)

        return "Berhasil join"
    
    def process_client(self, client):
        while True:            
            message = client.recv(4096).decode('utf-8')
            if message:
                data = message.split(" ")
                order = data[0].strip()

                if order == "CREATE":
                    result = self.create_group(data[1].strip())
                    client.sendall(result.encode())

                elif order == "JOIN":
                    room_name = data[1].strip()
                    username = data[2].strip()

                    result = self.join_group(room_name, username, client)

                    self.broadcast_all(f"{username} has join {room_name}".encode(), room_name)
                    client.sendall(result.encode())

                elif order == "SENDGROUP":
                    room_name = data[1].strip()
                    username = data[2].strip()

                    message = ""
                    for w in data[3:]:
                        message = "{} {}".format(message, w)

                    if "EXIT" in message:
                        with self.locker:
                            self.groups[room_name]["aliases"].remove(username)
                            self.groups[room_name]["clients"].remove(client)
                        
                        client.close()
                        self.broadcast_all(f'{username} has left the chat room {room_name}!'.encode('utf-8'), room_name)
                        break

                    self.broadcast_all(f"{username}: {message}".encode(), room_name)
                else:
                    client.sendall(f"process_client: {message}".encode())    
            else:
                print("unknown command", message)    

    def start(self):
        print('Server is running and listening ...')
        while True:
            client, address = self.server.accept()
            print(f'Connection established with {str(address)}')
            
            client_thread = threading.Thread(target=self.process_client, args=(client,))
            client_thread.start()

if __name__ == "__main__":
    server = ChatGroup('127.0.0.1', 59000)
    server.start()
