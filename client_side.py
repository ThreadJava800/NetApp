from enum import Enum
import ipaddress
import socket

from common import NetApp, NetAppProtocol, BLOCK_SIZE, UDP_TIMEOUT
from utils import enterIp, enterPort, enterFilename

class UserChoices(Enum):
    QUIT = 0
    CONTINUE = 1

    DEFAULT = 2

def getChoice() -> UserChoices:
    while True:
        answer = input("Quit / send one more file (q/c): ")
    
        if answer != 'q' and answer != 'c':
            print("Enter only allowed symbols!")
            continue

        if answer == 'q':
            return UserChoices.QUIT
        return UserChoices.CONTINUE
    
    raise Exception("Code unreachable!")

class Client(NetApp):
    def __init__(self, protocol: NetAppProtocol):
        super().__init__(protocol)

    def __sendFileOverTcp(self, server_ip: ipaddress.ip_address, server_port: int, recv_filepath: str, send_filepath: str):
        self.socket.connect((str(server_ip), server_port))

        # sending file
        print("Sending file...")
        send_file = open(send_filepath, "rb")
        send_block = send_file.read(BLOCK_SIZE)
        while send_block:
            self.socket.send(send_block)
            send_block = send_file.read(BLOCK_SIZE)
        send_file.close()
        self.socket.shutdown(socket.SHUT_WR)
        print("Finished sending file!")

        # receiving it back
        print("Receiving file")
        recv_file = open(recv_filepath, "wb")
        recv_block = self.socket.recv(BLOCK_SIZE)
        while recv_block:
            recv_file.write(recv_block)
            recv_block = self.socket.recv(BLOCK_SIZE)
        recv_file.close()
        print("File received!")
    
    def __sendFileOverUdp(self, server_ip: ipaddress.ip_address, server_port: int, recv_filepath: str, send_filepath: str):
        # sending file
        print("Sending file...")
        send_file = open(send_filepath, "rb")
        send_block = send_file.read(BLOCK_SIZE)
        while send_block:
            self.socket.sendto(send_block, (str(server_ip), server_port))
            send_block = send_file.read(BLOCK_SIZE)
        send_file.close()
        print("Finished sending file!")

        #receiving file
        print("Receiving file")
        recv_file = open(recv_filepath, "wb")
        try:
            recv_block, _ = self.socket.recvfrom(BLOCK_SIZE)
            while recv_block:
                recv_file.write(recv_block)
                self.socket.settimeout(UDP_TIMEOUT)
                recv_block, _ = self.socket.recvfrom(BLOCK_SIZE)
        except socket.timeout:
            pass
        recv_file.close()
        print("File received!")

    def sendFile(self, server_ip: ipaddress.ip_address, server_port: int, recv_filepath: str, send_filepath: str):
        match self.protocol.value:
            case NetAppProtocol.TCP.value:
                self.__sendFileOverTcp(server_ip, server_port, recv_filepath, send_filepath)
            case NetAppProtocol.UDP.value:
                self.__sendFileOverUdp(server_ip, server_port, recv_filepath, send_filepath)
            case _:
                raise Exception("Protocol is not implemented!")

    def run(self):
        while True:
            client_ip = enterIp("Enter server ip-address: ")
            port = enterPort("Enter server port: ")
            send_filepath = enterFilename("Enter existing filename, where to send data to server: ")
            recv_filepath = enterFilename("Enter existing filename, where to save response from server: ")

            self.sendFile(client_ip, port, recv_filepath, send_filepath)
            self.socket.close()

            answer = getChoice()
            is_quit = False
            match answer.value:
                case UserChoices.QUIT.value:
                    is_quit = True
                case UserChoices.CONTINUE.value:
                    match self.protocol.value:
                        case NetAppProtocol.TCP.value:
                            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        case NetAppProtocol.UDP.value:
                            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        case _:
                            raise Exception("Protocol is not implemented!")
                    continue
                case _:
                    raise Exception("Invalid user choice!")
            if is_quit:
                break
