import socket
import json
import zlib
import sys


class Alice():
    def __init__(self,port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect(("", self.port))

    def Work(self):
        return

    def timeout_setting(self,time):
        self.socket.settimeout(time)

    def send(self, packet):
        self.socket.send(packet)

    def receive(self,data):
        return self.socket.recv(data)

    def create_packet(self,ack,data):
        checksum = zlib.crc32(json.dumps([ack,data]).encode())
        return zlib.compress(json.dumps([ack,data,checksum]).encode())

    def check_corrupt(self,packet):
        try:
            updated_packet = json.loads(zlib.decompress(packet).decode())
            return updated_packet[2] != zlib.crc32(json.dumps(updated_packet[0:2]).encode())
        except:
            return True

    def get_ack(self,packet,num):
        packet = json.loads(zlib.decompress(packet).decode())
        return packet[0] == num and packet[1] == 'ack'