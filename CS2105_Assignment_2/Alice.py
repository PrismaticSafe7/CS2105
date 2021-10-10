import socket
import zlib
import sys

class Alice():
    def __init__(self,port):
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    def Server_process(self):
        data = ''
        ack = 1

        for line in sys.stdin:
            data = line
            while (len(data) > 0):
                message = data[0:59]

                packet = self.create_packet(ack, message)
                self.socket.sendto(packet,('localhost',self.port))

                while True:
                    self.socket.settimeout(0.005)
                    try:
                        message, address = self.socket.recvfrom(64)
                        if self.checksum_check(message) and self.received_ack(message, ack):
                            ack *= -1
                            break

                        else:
                            self.socket.sendto(packet,('localhost',self.port))
                    except:
                        self.socket.sendto(packet,('localhost',self.port))

    def create_packet(self,ack,data):
        data = data.encode()
        ack_num = (str(ack)).encode()
        checksum = zlib.crc32(ack_num + data).to_bytes(4,byteorder='little')
        packet = checksum + ack_num + data
        return packet

    def checksum_check(self, message):
        ack = message[4:]
        checksum = int.from_byte(message[0:4], 'little')
        print(checksum)
        return zlib.crc32(ack) == checksum

    def received_ack(self,packet,num):
        ack = int(packet.decode())
        print("received")
        return  ack == num


if __name__ == "__main__":
    portNumber = int(sys.argv[1])
    server = Alice(portNumber)
    server.Server_process()
