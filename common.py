import argparse
from enum import Enum
import socket

BLOCK_SIZE = 1024

class NetAppType(Enum):
    SERVER = 1
    CLIENT = 2

class NetAppProtocol(Enum):
    TCP = 1
    UDP = 2

# 2 fields: self.type & self.protocol
class NetSettings:
    def __init__(self, args: argparse.ArgumentParser):
        parsed_args = args.parse_args()

        # check if only one parameter from two was provided
        if not(parsed_args.server ^ parsed_args.client) or not(parsed_args.tcp ^ parsed_args.udp):
            raise Exception("Incorrect arguments")
        
        if parsed_args.server:
            self.type = NetAppType.SERVER
        else:
            self.type = NetAppType.CLIENT

        if parsed_args.tcp:
            self.protocol = NetAppProtocol.TCP
        else:
            self.protocol = NetAppProtocol.UDP

class NetApp:
    def __init__(self, protocol: NetAppProtocol):
        self.hostname = socket.gethostname()
        self.protocol = protocol

        match self.protocol.value:
            case NetAppProtocol.TCP.value:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            case NetAppProtocol.UDP.value:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            case _:
                raise Exception("Protocol is not implemented!")
