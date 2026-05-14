#!/usr/bin/env python3
import os
import sys
import socket
import struct
from Crypto.Cipher import AES

RECEIVER_HOST = os.environ.get('RECEIVER_HOST', '127.0.0.1')
DATA_PORT = int(os.environ.get('DATA_PORT', 5000))
KEY_PORT = int(os.environ.get('KEY_PORT', 5001))

def recv_exact(conn, n: int) -> bytes:
    """Receive exactly n bytes from a TCP connection."""
    if n <= 0:
        raise ValueError("Số byte cần nhận phải lớn hơn 0.")
    
    chunks = []
    received = 0
    while received < n:
        chunk = conn.recv(n - received)
        if not chunk:
            raise ConnectionError("Kết nối bị đóng trước khi nhận đủ dữ liệu.")
        chunks.append(chunk)
        received += len(chunk)
    return b"".join(chunks)

def main():
    try:
        # Key channel
        key_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        key_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        key_socket.bind((RECEIVER_HOST, KEY_PORT))
        key_socket.listen(1)
        print("kênh khóa đã sẵn sàng", flush=True)
        
        # Data channel
        data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        data_socket.bind((RECEIVER_HOST, DATA_PORT))
        data_socket.listen(1)
        print("đã sẵn sàng nhận kết nối", flush=True)
        
        # Accept connections
        key_conn, key_addr = key_socket.accept()
        print(f"Đã chấp nhận kết nối key từ {key_addr}", flush=True)
        
        data_conn, data_addr = data_socket.accept()
        print(f"Đã chấp nhận kết nối data từ {data_addr}", flush=True)
        
        # Đọc key packet theo format: [key_length:4][key][iv:16]
        key_len_bytes = recv_exact(key_conn, 4)
        key_len = struct.unpack('!I', key_len_bytes)[0]
        
        key = recv_exact(key_conn, key_len)
        iv = recv_exact(key_conn, 16)  # IV luôn 16 bytes
        
        print(f"Đã nhận key ({len(key)} bytes) và IV ({len(iv)} bytes)", flush=True)
        
        # Đọc data packet: [ciphertext_length:4][ciphertext]
        ct_len_bytes = recv_exact(data_conn, 4)
        ct_len = struct.unpack('!I', ct_len_bytes)[0]
        
        ciphertext = recv_exact(data_conn, ct_len)
        
        print(f"Đã nhận ciphertext ({len(ciphertext)} bytes)", flush=True)
        
        # Giải mã
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext_padded = cipher.decrypt(ciphertext)
        
        # Xóa padding PKCS7
        pad_len = plaintext_padded[-1]
        plaintext = plaintext_padded[:-pad_len]
        plaintext_str = plaintext.decode('utf-8')
        
        print(f"[+] Bản tin gốc: {plaintext_str}", flush=True)
        
        # Đóng kết nối
        key_conn.close()
        data_conn.close()
        key_socket.close()
        data_socket.close()
        
    except Exception as e:
        print(f"Lỗi: {e}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()