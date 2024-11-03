import ipaddress
import os

def enterIp(ip_hint: str) -> ipaddress.ip_address:
    while True:
        ip_str = input(ip_hint)

        try:
            ip = ipaddress.ip_address(ip_str)
            return ip
        except:
            print("Ip-address must be in format 'xxx.xxx.xxx.xxx'! Try again.")

    raise Exception("Code unreachable!")

def enterPort(port_hint: str) -> int:
    while True:
        try:
            server_port = int(input(port_hint))
        except:
            print("Port must be a number! Try again")
            continue

        if server_port < 0 or server_port > 65535:
            print("Port must be in segment [0, 65535]! Enter again.")
            continue

        return server_port
    
    raise Exception("Code unreachable!")

def enterFilename(file_hint) -> str:
    while True:
        file_path_str = input(file_hint)

        if os.path.exists(file_path_str):
            return file_path_str
        else:
            print("File " + file_path_str + " is not found. Please, try again.")

    raise Exception("Code unreachable!")