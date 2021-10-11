import socket
import zlib
import sys

class Bob():
	def __init__(self, port):
		self.port = port
		self.ack = 0
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.socket.bind(('localhost',self.port))

	def Server_process(self):
		data = b''

		while True:
			message, address = self.socket.recvfrom(64)
			if self.checksum_check(message):
				num = int(message[4:5].decode())
				data = message[5:]

				if num == self.ack:
					ack_message = self.create_ack(self.ack)
					self.ack = (self.ack + 1) % 2
					self.socket.sendto(ack_message, address)
					if data.find(b'\n') != -1:
						print(data.decode(), end='')
					else:
						print(data.decode())

				else:
					ack_message = self.create_ack(self.ack*(-1))
					self.socket.sendto(data,address)

	def checksum_check(self, message):
		checksum = int.from_bytes(message[0:4],byteorder = 'little')
		data = zlib.crc32(message[4:])
		return checksum == data

	def create_ack(self, ack):
		ack_num = (str(ack)).encode()
		checksum = zlib.crc32(ack_num).to_bytes(4,byteorder = 'little')
		packet = checksum + ack_num
		return packet


if __name__ == "__main__":
    portNumber = int(sys.argv[1])
    server = Bob(portNumber)
    server.Server_process()
