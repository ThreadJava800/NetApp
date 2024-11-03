import socket

from common import BLOCK_SIZE, UDP_TIMEOUT, NetApp, NetAppProtocol
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
        #receiving file
        print("Receiving file")
        recv_file = open(recv_filepath, "wb")
        try:
            recv_block, client_addr = self.socket.recvfrom(BLOCK_SIZE)
            while recv_block:
                recv_file.write(recv_block)
                self.socket.settimeout(UDP_TIMEOUT)
                recv_block, client_addr = self.socket.recvfrom(BLOCK_SIZE)
        except socket.timeout:
            pass
        recv_file.close()
        print("File received!")

        # sending file
        print("Sending file...")
        send_file = open(recv_filepath, "rb")
        send_block = send_file.read(BLOCK_SIZE)
        while send_block:
            self.socket.sendto(send_block, client_addr)
            send_block = send_file.read(BLOCK_SIZE)
        send_file.close()
        print("Finished sending file!")

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
        if self.protocol.value == NetAppProtocol.TCP.value:
            self.socket.listen(5)

        while True:
            self.getFile(recv_filepath)
                
        raise Exception("Code unreachable!")
