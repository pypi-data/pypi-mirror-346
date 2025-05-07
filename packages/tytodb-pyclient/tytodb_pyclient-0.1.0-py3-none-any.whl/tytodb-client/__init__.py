import socket as socket_module,re,json
import blake3,lzma
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
from socket import socket as Socket

from typing import Any, List
import base64

class AuthenticationError(Exception):
    def __init__(self, message):
            super().__init__(message)

class BadURLError(Exception):
    def __init__(self, message):
            super().__init__(message)

def send_all(socket, data):
    total_sent = 0
    while total_sent <= len(data):
        sent = socket.send(data[total_sent:])
        if sent == 0:
            break
        total_sent += sent

def recv_all(sock, n):
    buf = b''
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            break
        buf += chunk
    return buf

class QueryResult:
    success : bool = False
    text : str = ""
    rows : list = []
    pages : list = []
    current_page : int = []
    id : str = ""
    def __init__(self,object,link):
        self.link = link
        if "!" in object and "?" in object:
            self.success : bool = object["!"]
            if not self.success:
                self.text = object["?"]
                raise RuntimeWarning(self.text)
            object_woa = json.loads(object["?"])
            self.rows = object_woa["rows"]
            self.pages = object_woa["pages"]
            self.current_page = object_woa["current_page"]
            self.id = object_woa["id"]
        else:
            raise RuntimeError("Failed to get QueryResult")
    def next_page(self) -> list:
        """
            If there is any page forward, the query will step into it.
        """
        result = self.link.command("QYCNNXT "+self.id)
        if result.success:
            self.rows = result.rows
            self.current_page = result.current_page
    def previous_page(self) -> list:
        """
            If there is any page backwards, the query will step into it.
        """
        result = self.link.command("QYCNPVS "+self.id)
        if result.success:
            self.rows = result.rows
            self.current_page = result.current_page
    def close_query(self) -> list:
        """
            The query data remains on the server until closed, so its a good idea to close the query when you're done with it!
        """
    def __exit__(self):
        result = self.link.command("QYCNEXT "+self.id)
        if result.success:
            self.rows = result.rows
            self.current_page = result.current_page
        self.close_query()
    def get_page_rows(self) -> list:
        """
            Return all the rows in the current page
        """
        return self.rows
    def __str__(self) -> str:
        return "query<"+self.id+">"
    def __repr__(self) -> str:
        return str(self)

class ConnectionHandler:
    def __init__(self, url: str, secret_key: bytes, timeout: int = 5):
        match = re.match(r"tytodb://([0-9]{1,3}(?:\.[0-9]{1,3}){3}):([0-9]{1,5}):([0-9]{1,5})$", url)
        if not match:
            raise BadURLError("Invalid URL format. Expected: tytodb://<ip>:<command_port>:<auth_port>")
        if len(secret_key) not in (16, 24, 32):
            raise ValueError("Secret key must be 16, 24, or 32 bytes")
        self.ip = match.group(1)
        self.command_port = match.group(2)
        self.authenticate_port = match.group(3)
        self.secret_key = secret_key
        self.cipher = AESGCM(secret_key)
        self.timeout = timeout
        self.authenticated = False
        self.authenticate()
    def command(self, command: str, arguments: List[Any]) -> QueryResult:
        if not self.authenticated:
            raise AuthenticationError("Not authenticated")
        data_connection = {'command': command, 'arguments': [str(x) for x in arguments]}
        json_datacon = json.dumps(data_connection).encode('utf-8')
        json_datacon = lzma.compress(json_datacon, format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256)
        iv = urandom(12)
        encrypted = self.session_cipher.encrypt(iv, json_datacon, None)  
        payload = self.session_id_hash + iv + encrypted
        length = (len(iv) + len(encrypted)).to_bytes(4, byteorder='big')
        data_socket = socket_module.create_connection((self.ip, int(self.command_port)), self.timeout)
        send_all(data_socket, length + payload)
        
        length_bytes = recv_all(data_socket, 8)
        length = int.from_bytes(length_bytes, 'big')
        if length == 0:
            raise RuntimeError("Something went wrong, check the database logs.")
        response = recv_all(data_socket, length)
        iv = response[:12]
        ciphertext = response[12:]
        print(len(iv),len(ciphertext))
        decrypted_and_uncompressed = lzma.decompress(self.session_cipher.decrypt(iv, ciphertext, None))
        content : str= decrypted_and_uncompressed.decode('utf-8')
        print(content)
        result = json.loads(content)
        return QueryResult(result,self)
    def authenticate(self):
        socket = socket_module.create_connection((self.ip, int(self.authenticate_port)), self.timeout)
        try:
            socket.sendall(blake3.blake3(self.secret_key).digest(32))
            payload = b""
            socket.settimeout(5)
            while True:
                b = socket.recv(10)
                if not b:
                    break
                payload += b
            success = bool(payload[0])
            if not success:
                raise AuthenticationError("Authentication failed")
            session_id_cipher = payload[1:]   [success] + iv + ciphertext
            iv = session_id_cipher[:12]
            ciphertext = session_id_cipher[12:]
            self.session_id = self.cipher.decrypt(iv, ciphertext, None)  
            self.session_cipher = AESGCM(self.session_id)  
            self.session_id_hash = blake3.blake3(self.session_id).digest(32)
            self.authenticated = True
        except socket_module.error as e:
            raise AuthenticationError(f"Authentication failed: {e}")
        finally:
            socket.close()
