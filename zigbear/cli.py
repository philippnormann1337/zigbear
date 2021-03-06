from cmd import Cmd

from zigbear.custom_protocol.coordinatorcli import CoordinatorCli
from zigbear.custom_protocol.devicecli import DeviceCli
from zigbear.radio.cc2531connector import CC2531Connector
from zigbear.radio.mockconnector import MockConnector
from zigbear.radio.nrfconnector import NrfConnector
from zigbear.radio.raspbeeconnector import RaspbeeConnector
from zigbear.radio.socketconnector import SocketConnector
from zigbear.zigbee.zigbeeCli import ZigbeeCli


class ZigbearCli(Cmd):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector
        self.prompt = "zigbear> "
        self.intro = "Welcome! Type ? to list commands"

    def do_channel(self, arg):
        '''channel <channel>: set the channel in the current connector'''
        if self.connector:
            if len(arg) > 0:
                self.connector.set_channel(int(arg))
            else:
                print(f'invalid channel {arg}')
        else:
            print("please specify a radio connector")

    def do_zigbee(self, arg):
        if self.connector:
            ZigbeeCli(self.connector).cmdloop()
        else:
            print("please specify a radio connector")

    def do_device(self, arg):
        if self.connector:
            DeviceCli(self.connector).cmdloop()
        else:
            print("please specify a radio connector")

    def do_coordinator(self, arg):
        if self.connector:
            CoordinatorCli(self.connector).cmdloop()
        else:
            print("please specify a radio connector")

    def do_send(self, inp):
        '''send <hexStr>: send the hexStr'''
        try:
            frame = bytes.fromhex(inp.strip())
            self.connector.send(frame)
        except ValueError:
            print("invalid hex number")

    def do_connector(self, arg):
        '''connector <type>: sets the connector for radio'''
        if self.connector is not None:
            self.connector.close()
        if arg == "nrf":
            port = input("COM port: ")
            self.connector = NrfConnector(port)
        elif arg == "cc2531":
            self.connector = CC2531Connector()
        elif arg == "raspbee":
            host = input("wireshark host: ")
            self.connector = RaspbeeConnector(wireshark_host=host)
        elif arg == "mock":
            self.connector = MockConnector()
        elif arg == "socket":
            r_port = input("UDP Port for receiving: ")
            t_port = input("UDP Port to send to: ")
            self.connector = SocketConnector(receive_port=r_port, target_port=t_port)
        else:
            self.connector = None
        if self.connector is not None:
            self.connector.start()

    def do_exit(self, inp):
        '''exits the CMD'''
        print("Bye")
        return True