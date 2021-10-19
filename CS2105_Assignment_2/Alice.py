import socket
import zlib
import sys

class Alice():
    def __init__(self,port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ack = 0

    def Server_process(self):
        for line in sys.stdin:
            data = line
            while (len(data) != 0):
                message = data[0:59]

                packet = self.create_packet(self.ack, message)
                self.socket.sendto(packet,('localhost',self.port))

                self.socket.settimeout(0.005)
                try:
                    message, address = self.socket.recvfrom(64)
                    checksum = message[0:4]
                    ack_num = message[4:5]
                    if self.checksum_check(ack_num, checksum) and self.received_ack(ack_num, self.ack):
                        self.ack = (self.ack + 1) % 2
                        data = data[59:]

                except:
                    continue

    def create_packet(self,ack,data):
        data = data.encode()
        ack_num = (str(ack)).encode()
        checksum = zlib.crc32(ack_num + data).to_bytes(4,byteorder='little')
        packet = checksum + ack_num + data
        return packet

    def checksum_check(self, ack, checksum):
        checksum_int = int.from_bytes(checksum, byteorder='little')
        return zlib.crc32(ack) == checksum_int

    def received_ack(self,packet,num):
        return  int(packet.decode()) == num


if __name__ == "__main__":
    portNumber = int(sys.argv[1])
    server = Alice(portNumber)
    server.Server_process()
