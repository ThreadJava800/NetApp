import argparse

from common import NetSettings, NetAppType
import client_side
import server_side

def createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
                    prog="NetApp emulator",
                    description="Emulate TCP/UDP client or server. \
                                 Awaits for two arguments: (-c or -s) and (--tcp or --udp).",
                )
    
    parser.add_argument("-s", "--server", action="store_true")
    parser.add_argument("-c", "--client", action="store_true")
    parser.add_argument("--tcp", action="store_true")
    parser.add_argument("--udp", action="store_true")

    return parser

def realMain() -> None:
    cmd_parser = createParser()
    net_app = NetSettings(cmd_parser)

    if net_app.type == NetAppType.SERVER:
        server = server_side.Server(net_app.protocol)
        server.run()
    else:
        client = client_side.Client(net_app.protocol)
        client.run()

if __name__ == "__main__":
    realMain()