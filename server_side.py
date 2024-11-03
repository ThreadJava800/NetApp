import socket

from common import BLOCK_SIZE, NetApp, NetAppProtocol
from utils import enterIp, enterPort, enterFilename

class Server(NetApp):
    def __init__(self, protocol: NetAppProtocol):
        super().__init__(protocol)

    def __getFileOverTcp(self, recv_filepath: str):
        conn, _ = self.socket.accept()

        # receiving file from client
        print("Receiving file from client...")
        server_file = open(recv_filepath, "wb")
        client_file = conn.recv(BLOCK_SIZE)
        while client_file:
            server_file.write(client_file)
            client_file = conn.recv(BLOCK_SIZE)
        server_file.close()
        print("File received: " + recv_filepath + ".")

        # sending everything back (why??? - who knows)
        print("Sending file back to client...")
        server_file = open(recv_filepath, "rb")
        send_block = server_file.read(BLOCK_SIZE)
        while send_block:
            conn.send(send_block)
            send_block = server_file.read(BLOCK_SIZE)
        server_file.close()
        self.socket.shutdown(socket.SHUT_WR)
        print("File sent!")

        conn.close()
    
    def __getFileOverUdp(self, recv_filepath: str):
        pass

    def getFile(self, filepath: str):
        match self.protocol.value:
            case NetAppProtocol.TCP.value:
                self.__getFileOverTcp(filepath)
            case NetAppProtocol.UDP.value:
                self.__getFileOverUdp(filepath)
            case _:
                raise Exception("Protocol is not implemented!")

    def run(self):
        server_ip = enterIp("Enter server ip-address: ")
        port = enterPort("Enter server port: ")
        recv_filepath = enterFilename("Enter existing filename, where to save data from client: ")

        self.socket.bind((str(server_ip), port))
        self.socket.listen(5)

        while True:
            self.getFile(recv_filepath)
                
        raise Exception("Code unreachable!")
