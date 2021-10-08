import socket
import json
import zlib
import sys

class Alice():
    def __init__(self,port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def Server_process(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect(("", self.port))
        info = 
        data = ''
        ack = 0
        noMoreData = False

        while not noMoreData:
            data = sys.stdin.read(50)
            packet = create_packet(ack, data)
            self.socket.send(packet)
            While True:
                try:
                    self.socket.settimeout(0.0005)
                    message, address = self.socket.recv(2048)
                    if checksum_check(message) && self.received_ack(message, ack):
                        ack += 1
                        ack //= 2
                        break

                    else:
                        self.socket.send(packet)
                except:
                    self.socket.send(packet)

            if not data:
                noMoreData = True

    def create_packet(self,ack,data):
        checksum = zlib.crc32(json.dumps([ack,data]).encode())
        return zlib.compress(json.dumps([checksum,ack,data]).encode())

    def checksum_check(self, message):
        try:
            message = json.loads(zlib.decompress(message).decode())
            return message[0] == zlib.crc32(json.dumps([message[1],message[2]]).encode)

        else:
            return False

    def received_ack(self,packet,num):
        packet = json.loads(zlib.decompress(packet).decode())
        return packet[0] == 'ack' and packet[1] == num


if __name__ == "__main__":
    portNumber = int(sys.argv[1])
    server = WebServer(portNumber)
    server.Server_process()


