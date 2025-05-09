BitStuffing='''
def bit_stuffing(data: str) -> str:
    stuffed_data = ""
    consecutive_ones = 0
    
    for bit in data:
        if bit == '1':
            consecutive_ones += 1
            stuffed_data += bit
            if consecutive_ones == 5:
                stuffed_data += '0'
                consecutive_ones = 0
        else:
            stuffed_data += bit
            consecutive_ones = 0 
    
    return stuffed_data

def bit_unstuffing(stuffed_data: str) -> str:
    unstuffed_data = ""
    consecutive_ones = 0

    i = 0
    while i < len(stuffed_data):
        bit = stuffed_data[i]
        if bit == '1':
            consecutive_ones += 1
            unstuffed_data += bit
            if consecutive_ones == 5:

                i += 1
                consecutive_ones = 0
        else:
            unstuffed_data += bit
            consecutive_ones = 0 
        i += 1
    
    return unstuffed_data

data = "111110001111111000111"
print("Original data:      ", data)
stuffed = bit_stuffing(data)
print("Stuffed data:       ", stuffed)
unstuffed = bit_unstuffing(stuffed)
print("Unstuffed data:     ", unstuffed)
'''

ByteStuffing='''
def byte_stuffing(data: bytes, delimiter: bytes = b'\x7E', escape: bytes = b'\x7D') -> bytes:
    stuffed_data = bytearray()
    
    for byte in data:
        if byte == delimiter[0]:
            stuffed_data.extend(escape + bytes([byte ^ 0x20]))
        elif byte == escape[0]:
            stuffed_data.extend(escape + bytes([byte ^ 0x20]))
        else:
            stuffed_data.append(byte)
    
    return bytes(stuffed_data)

def byte_unstuffing(stuffed_data: bytes, delimiter: bytes = b'\x7E', escape: bytes = b'\x7D') -> bytes:
    unstuffed_data = bytearray()
    i = 0
    
    while i < len(stuffed_data):
        byte = stuffed_data[i]
        if byte == escape[0] and i + 1 < len(stuffed_data):
            unstuffed_data.append(stuffed_data[i + 1] ^ 0x20)
            i += 2
        else:
            unstuffed_data.append(byte)
            i += 1
    
    return bytes(unstuffed_data)

data = b'\x12\x7E\x45\x7D\x78\x7E\x56'
print("Original data:      ", data)
stuffed = byte_stuffing(data)
print("Stuffed data:       ", stuffed)
unstuffed = byte_unstuffing(stuffed)
print("Unstuffed data:     ", unstuffed)
'''

CharacterCount='''
def character_count(frames):
    final_string = ""
    for frame in frames:
        length = str(len(frame) + 1)
        final_string += length + frame
    return final_string

no_of_frames = int(input("Enter the number of frames: "))
frames = []

for i in range(no_of_frames):
    frame = input(f"Enter frame {i + 1}: ")
    frames.append(frame)

result = character_count(frames)
print("Result:", result)

'''

CyclicRedundancyCheck='''
def crc(data, divisor):
    n = len(divisor)
    temp = data + '0' * (n - 1)  # Append zeros 
    temp = list(temp)
    divisor = list(divisor)
    for i in range(len(data)):
        if temp[i] == '1':
            for j in range(n):
                temp[i + j] = str(int(temp[i + j]) ^ int(divisor[j]))
    
    remainder = ''.join(temp[-(n - 1):]) 
    return remainder

def crc2(received_data, divisor):
    n = len(divisor)
    temp = list(received_data)  # Dont append zeros
    divisor = list(divisor)
    for i in range(len(received_data) - n + 1):
        if temp[i] == '1':
            for j in range(n):
                temp[i + j] = str(int(temp[i + j]) ^ int(divisor[j]))
    
    remainder = ''.join(temp[-(n - 1):]) 
    return remainder
#both are same functions except for appending zeros part

#Sender Side
data = input("Enter data to be sent: ")
key = input("Enter key: ")

checksum = crc(data, key)
sent_data = data + checksum
print(f"Sent data: {sent_data}")

#Receiver side
received_data = input("Enter received data: ")
remainder = crc2(received_data, key)

if int(remainder) == 0:
    print("Data received without errors.")
else:
    print(f"Error detected in received data. Remainder: {remainder}")
'''

HammingCode='''
def calculate_parity_positions(data_length):
    """Calculate positions of parity bits (powers of 2)."""
    i = 0
    positions = []
    while 2**i <= data_length + i + 1:
        positions.append(2**i - 1)
        i += 1
    return positions


def generate_hamming_code(data):
    """Generate Hamming code from input binary data."""
    data = list(map(int, data))
    m = len(data) 
    parity_positions = calculate_parity_positions(m)
    n = m + len(parity_positions) 
    encoded = [0] * n

    j = 0
    for i in range(n):
        if i in parity_positions:
            continue 
        encoded[i] = data[j]
        j += 1

    for parity_pos in parity_positions:
        parity = 0
        for i in range(n):
            if (i + 1) & (parity_pos + 1): 
                parity ^= encoded[i]
        encoded[parity_pos] = parity

    return ''.join(map(str, encoded))


def correct_hamming_code(encoded):
    """Detect and correct errors in the received Hamming code."""
    encoded = list(map(int, encoded))
    n = len(encoded)
    parity_positions = calculate_parity_positions(n)
    error_position = 0

    for parity_pos in parity_positions:
        parity = 0
        for i in range(n):
            if (i + 1) & (parity_pos + 1): 
                parity ^= encoded[i]
        if parity != 0:
            error_position += parity_pos + 1

    if error_position != 0:
        print(f"Error detected at position: {error_position}")
        encoded[error_position - 1] ^= 1 
        print("Error corrected.")
    else:
        print("No error detected.")

    parity_positions_set = set(parity_positions)
    decoded = [encoded[i] for i in range(n) if i not in parity_positions_set]

    return ''.join(map(str, decoded)), ''.join(map(str, encoded))


def main():
    """Main function to interact with the user."""
    while True:
        print("\n--- Hamming Code Generator and Corrector ---")
        print("1. Generate Hamming Code")
        print("2. Correct Hamming Code")
        print("3. Exit")

        def case_generate_hamming():
            data = input("Enter the binary data (e.g., 1011): ")
            if not all(c in '01' for c in data):
                print("Invalid input! Please enter binary data only.")
                return
            hamming_code = generate_hamming_code(data)
            print(f"Hamming Code: {hamming_code}")

        def case_correct_hamming():
            encoded = input("Enter the received Hamming code: ")
            if not all(c in '01' for c in encoded):
                print("Invalid input! Please enter binary data only.")
                return
            decoded_data, corrected_code = correct_hamming_code(encoded)
            print(f"Corrected Code: {corrected_code}")
            print(f"Decoded Data: {decoded_data}")

        def case_exit():
            print("Exiting...")
            exit(0)

        switch_case = {
            '1': case_generate_hamming,
            '2': case_correct_hamming,
            '3': case_exit
        }

        choice = input("Enter your choice (1, 2, or 3): ").strip()
        switch_case.get(choice, lambda: print("Invalid choice! Please try again."))()


if __name__ == "__main__":
    main()


'''

SelectiveRepeat='''
import time
import random
class SelectiveRepeat:
    def __init__(self, window_size, total_frames):
        self.window_size = window_size
        self.total_frames = total_frames
        self.sent_frames = [None] * total_frames
        self.ack_received = [False] * total_frames
        self.current_frame = 0
    def send_frame(self, frame_num):
        if self.sent_frames[frame_num] is None:
            print(f"Sending frame {frame_num}")
            self.sent_frames[frame_num] = True
            time.sleep(1)
    def receive_ack(self, frame_num):
        ack = random.choice([True, False])
        if ack:
            print(f"ACK received for frame {frame_num}")
            self.ack_received[frame_num] = True
        else:
            print(f"NACK for frame {frame_num}")
    def send_frames(self):
        while not all(self.ack_received):
            for i in range(self.window_size):
                frame_num = (self.current_frame + i) % self.total_frames
                if not self.ack_received[frame_num]:
                    self.send_frame(frame_num)
            for i in range(self.window_size):
                frame_num = (self.current_frame + i) % self.total_frames
                if not self.ack_received[frame_num]:
                    self.receive_ack(frame_num)
            self.current_frame = (self.current_frame + 1) % self.total_frames
sr = SelectiveRepeat(window_size=4, total_frames=10)
sr.send_frames()
'''

GoBack='''
import time
import random

class GoBackN:
    def __init__(self, window_size, total_frames):
        self.window_size = window_size
        self.total_frames = total_frames
        self.sent_frames = 0
        self.ack_received = 0 
    def send_frames(self):
        while self.ack_received < self.total_frames:
            for i in range(self.window_size):
                if self.sent_frames < self.total_frames:
                    print(f"Sending frame {self.sent_frames}")
                    self.sent_frames += 1
                    time.sleep(1)
            for i in range(self.window_size):
                if self.ack_received < self.total_frames:
                    ack = random.choice([True, False])
                    if ack:
                        print(f"ACK received for frame {self.ack_received}")
                        self.ack_received += 1
                    else:
                        print(f"Frame {self.ack_received} lost, resending from this frame")
                        self.sent_frames = self.ack_received
                        break
gbn = GoBackN(window_size=4, total_frames=10)
gbn.send_frames()
'''

StopandWaitClient='''
import socket
import time

HOST = '127.0.0.1'
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

TIMEOUT = 5 

while True:
    message = input("Enter the data here: ")
    client_socket.sendall(message.encode())
    if message == 'end':
        break

    client_socket.settimeout(TIMEOUT)
    try:
        data = client_socket.recv(1024)
        print(data.decode())
    except socket.timeout:
        print(f"ACK not received for '{message}', retransmitting...")
        client_socket.sendall(message.encode())  # Retransmit the message

print("Ended the connection")
client_socket.close()
'''

StopandWaitServer='''
import socket
import time
import random

HOST = '127.0.0.1'
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"The server is listening on {HOST}:{PORT}")
conn, address = server_socket.accept()
print(f"Connected by {address}")

def generate_ack(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        received_data = data.decode()
        time.sleep(2)
        print(f"The data which is received is: {received_data}")
        
        if received_data == 'end':
            break
        
        # Simulate ACK loss
        if random.random() < 0.3:
            print(f"Simulating lost ACK for: {received_data}")
            continue
        
        # Send ACK if not dropped
        ack = f"ACK for: {received_data}"
        conn.sendall(ack.encode())
    conn.close()

generate_ack(conn)
server_socket.close()
'''

SubnetMask='''
def get_ip_class_and_subnet(ip):
    octets = ip.split('.')
    
    if len(octets) != 4:
        return 'Invalid IP address', 'N/A'

    try:
        octets = [int(octet) for octet in octets]
        
        if any(octet < 0 or octet > 255 for octet in octets):
            return 'Invalid IP address', 'N/A'
        
        first_octet = octets[0]

        if first_octet >= 1 and first_octet <= 127:
            ip_class = 'Class A'
            subnet_mask = '255.0.0.0'
        elif first_octet >= 128 and first_octet <= 191:
            ip_class = 'Class B'
            subnet_mask = '255.255.0.0'
        elif first_octet >= 192 and first_octet <= 223:
            ip_class = 'Class C'
            subnet_mask = '255.255.255.0'
        elif first_octet >= 224 and first_octet <= 239:
            ip_class = 'Class D (Multicast)'
            subnet_mask = 'N/A'
        elif first_octet >= 240 and first_octet <= 255:
            ip_class = 'Class E (Reserved)'
            subnet_mask = 'N/A'
        else:
            ip_class = 'Unknown'
            subnet_mask = 'N/A'
        
        return ip_class, subnet_mask

    except ValueError:
        return 'Invalid IP address', 'N/A'


ip_address = input("Enter an IP address: ")
ip_class, subnet_mask = get_ip_class_and_subnet(ip_address)
print(f"IP Address: {ip_address}")
print(f"Class: {ip_class}")
print(f"Subnet Mask: {subnet_mask}")
'''

BellmanFord='''
weight = [
    [0, 4, 0, 0],
    [0, 0, -2, 0],
    [0, 0, 0, 3],
    [0, 0, 0, 0],
]

n = 4 
dist = [9999] * n
parent = [-1] * n

source = 0
dist[source] = 0

def relax(u, v):
    if dist[v] > dist[u] + weight[u][v]:
        dist[v] = dist[u] + weight[u][v]
        parent[v] = u

def BellmanFord():
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if weight[u][v] != 0:
                    relax(u, v)

    for u in range(n):
        for v in range(n):
            if weight[u][v] != 0 and dist[v] > dist[u] + weight[u][v]:
                return False  
    return True

if BellmanFord():
    print(f"Shortest distances from source {source}: {dist}")
    print(f"Parent nodes: {[p + 1 for p in parent]}") 
else:
    print("Graph contains a negative weight cycle. No solution.")
'''

Dijikstra='''
graph = [
    [0, 7, 9, 0, 0, 4],
    [7, 0, 10, 15, 0, 0],
    [9, 10, 0, 11, 0, 2],
    [0, 15, 11, 0, 6, 0],
    [0, 0, 0, 6, 0, 9],
    [4, 0, 2, 0, 9, 0]
]

n = 6

dist = [9999] * n
parent = [-1] * n
visited = [0] * n

source = 0
dist[source] = 0

def extract_min():
    return min((dist[i], i) for i in range(n) if not visited[i])[1]

def relax(u, v):
    if dist[v] > dist[u] + graph[u][v]:
        dist[v] = dist[u] + graph[u][v]
        parent[v] = u

for _ in range(n):
    u = extract_min()
    for v in range(n):
        if graph[u][v] != 0 and not visited[v]:
            relax(u, v)
    visited[u] = 1

print(f"Shortest distances from source {source}: {dist}")
parent = [p + 1 if p != -1 else -1 for p in parent]
print(f"Parent nodes: {parent}")
'''

LeakyBucketClient='''
import socket, random, time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    packet_size = random.randint(1, 5)
    message = str(packet_size)
    client_socket.sendto(message.encode(), ('localhost', 12345))
    print(f"Sent packet of size {packet_size}")
    
    time.sleep(1)
'''

LeakyBucketServer='''
import socket, time

bucket_size = 10
current_level = 0

def leak_packets():
    global current_level
    leak_amount = 2
    if current_level > 0:
        current_level -= leak_amount
        print(f"Leaked {leak_amount} packets. Current level: {current_level}")
    else:
        print("No packets to leak.")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 12345))

while True:
    data, addr = server_socket.recvfrom(1024)
    packet_size = int(data.decode())
    
    
    if current_level + packet_size <= bucket_size:
        current_level += packet_size
        print(f"Received packet of size {packet_size}. Current level: {current_level}")
    else:
        print(f"Bucket overflow! Dropped packet of size {packet_size}")

    # Leak packets every 2 seconds
    leak_packets()
    time.sleep(2)
'''

TokenBucketClient='''
import socket

def create_client_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 50003))
    print("Connected to server")
    return client_socket

def communicate_with_server(client_socket):
    while True:
        data = input("Enter data (or 'exit' to quit): ")
        if data == "exit":
            break
        client_socket.send(data.encode())
    client_socket.close()

def start_client():
    client_socket = create_client_socket()
    communicate_with_server(client_socket)

start_client()
'''

TokenBucketServer = '''
import socket
import threading
import time

bucket_token_list = []
MAX_BUCKET_SIZE = 10
TIME_LAPSE = 3
lock = threading.Lock()

def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 50003))
    server_socket.listen(5)
    print("Server started on 127.0.0.1:50003")
    return server_socket

def add_token_to_bucket():
    while True:
        with lock:
            if len(bucket_token_list) < MAX_BUCKET_SIZE:
                bucket_token_list.append(1)
        time.sleep(TIME_LAPSE)

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024).decode()
        if not data:
            continue
        print(f"Received: {data}")
        with lock:
            if bucket_token_list:
                bucket_token_list.pop(0)
                print(f"Token used, bucket: {bucket_token_list}")
            else:
                client_socket.send("Token not available, wait.".encode())
                print("No token available")
    client_socket.close()

def start_server():
    server_socket = create_server_socket()
    threading.Thread(target=add_token_to_bucket, daemon=True).start()
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

start_server()
'''

ClassfulAddressing = '''
ip = input("Enter IP address: ")
iplist = ip.split(".")

if len(iplist) != 4:
    print("ERROR IN IP")
else:
    firstoctet=int(iplist[0])
    if (firstoctet>=0 and firstoctet<=127):
        print("Class: A")
        print("Subnet mask: 255.0.0.0")
        iplist[1]=iplist[2]=iplist[3]="0"
        modified_ip = ".".join(iplist)
        print("Subnet address: ", modified_ip)
    elif (firstoctet>=128 and firstoctet<=191):
        print("Class: B")
        print("Subnet mask: 255.255.0.0")
        iplist[2]=iplist[3]="0"
        modified_ip = ".".join(iplist)
        print("Subnet address: ", modified_ip)
    elif (firstoctet>=192 and firstoctet<=223):
        print("Class: C")
        print("Subnet mask: 255.255.255.0")
        iplist[3]="0"
        modified_ip = ".".join(iplist)
        print("Subnet address: ", modified_ip)
    elif (firstoctet>=224 and firstoctet<=239):
        print("Class: D")
        print("Subnet mask: Multicast")
    elif (firstoctet>=240 and firstoctet<=255):
        print("Class: E")
        print("Subnet mask: Reserved")
'''

cn_exp = {
    'BitStuffing.py': BitStuffing,
    'ByteStuffing.py': ByteStuffing,
    'CharacterCount.py': CharacterCount,
    'CyclicRedundancyCheck.py': CyclicRedundancyCheck,
    'HammingCode.py': HammingCode,
    'SelectiveRepeat.py': SelectiveRepeat,
    'GoBack.py': GoBack,
    'StopandWaitClient.py': StopandWaitClient,
    'StopandWaitServer.py': StopandWaitServer,
    'SubnetMask.py': SubnetMask,
    'BellmanFord.py': BellmanFord,
    'Dijikstra.py': Dijikstra,
    'LeakyBucketClient.py': LeakyBucketClient,
    'LeakyBucketServer.py': LeakyBucketServer,
    'TokenBucketClient.py': TokenBucketClient,
    'TokenBucketServer.py': TokenBucketServer,
    'ClassfulAddressing.py': ClassfulAddressing
}

def cn_():
    for filename, content in cn_exp.items():
        print(filename)
    exp = input("Enter Code : ")
    with open(exp, 'w') as file:
        file.write(cn_exp[exp])
