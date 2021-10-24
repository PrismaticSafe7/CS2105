import sys

end = False
while not end:
    integer = ""
    while True:
        byte = sys.stdin.buffer.read1(1)
        if bytes.decode(byte) == " ":
            byte = sys.stdin.buffer.read1(1)
            while bytes.decode(byte) != "B":
                integer += bytes.decode(byte)
                byte = sys.stdin.buffer.read1(1)
            break

    size = int(integer)

    for i in range(size):
        data = sys.stdin.buffer.read1(1)
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()

    if sys.stdin.buffer.peek(1) == b"":
        end = True
