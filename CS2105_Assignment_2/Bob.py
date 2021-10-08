import socket
import zlib
import sys
import json

class Bob:
	def __init__(self, port):
		self.port = port

	def Server_process(self):
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('',self.port))

		data = ''
		ack = 0
		noMoreData = False

		while not noMoreData:
			message, address = self.socket.recvfrom()
			if checksum_check(message):
				decoded_message = json.loads(zlib.decompress(message).decode())

				if decoded_message[1] == ack:
					data = self.create_ack(ack)
					ack += 1
					ack //= 2
					self.socket.sendto(data, address)
					print(decoded_message[2])

				else:
					data = self.create_ack((ack+1)//2)
					self.scoekt.sendto(data,address)

				if not decoded_message:
					noMoreData == True

	
	def checksum_check(self, message):
		try:
			message = json.loads(zlib.decompress(message).decode())
			return message[0] == zlib.crc32(json.dumps([message[1],message[2]]).encode)

		except:
			return False

	def create_ack(self, ack):
		checksum = zlib.crc32(json.dumps(["ack", ack]).encode)
		packet = zlib.compress(json.dumps([checksum,"ack", ack]).encode)


if __name__ == "__main__":
    portNumber = int(sys.argv[1])
    server = Bob(portNumber)
    server.ServerSocket()
