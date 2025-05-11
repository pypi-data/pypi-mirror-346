import re,json
import blake3,lzma
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from os import urandom
from typing import Any, List
import base64
import requests
import logging

# Enable logging for urllib3
logging.basicConfig(level=logging.DEBUG)

class AuthenticationError(Exception):
    def __init__(self, message):
            super().__init__(message)

class BadURLError(Exception):
    def __init__(self, message):
            super().__init__(message)


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
        
        match = re.match(r"tytodb://([0-9]{1,3}(?:\.[0-9]{1,3}){3}):([0-9]{1,5}), url")
        if not match:
            raise BadURLError("Invalid URL format. Expected: tytodb://<ip>:<port>")
        if len(secret_key) not in (16, 24, 32):
            raise ValueError("Secret key must be 16, 24, or 32 bytes")
        self.ip = match.group(1)
        self.port = match.group(2)
        self.secret_key = secret_key
        self.cipher = AESGCM(secret_key)
        self.timeout = timeout
        self.authenticated = False
        self.client = requests.session()
        self.url = "http://"+self.ip+":"+self.port
        self.authenticate()
        
    def command(self, command: str, arguments: List[Any]) -> QueryResult:
        if not self.authenticated:
            raise AuthenticationError("Not authenticated")
        try:
            step = 0
            print("client step",step)
            step += 1
            data_connection = {'command': command, 'arguments': [str(x) for x in arguments]}
            json_datacon = json.dumps(data_connection).encode('utf-8')
            iv = urandom(12)
            print("client step",step)
            step += 1
            encrypted = self.session_cipher.encrypt(iv, json_datacon, None)  
            payload = self.session_id_hash + iv + encrypted
            response = self.client.post(self.url,data=payload)
            print("client step",step)
            step += 1
            print("client step send",step)
            step += 1
            print("sent, now receiving...")
            bresponse = response.content
            size = int.from_bytes(bresponse[:8])
            response = bresponse[8:]
            if size == 0:
                raise RuntimeError("Something went wrong:Empty response.") 
            print("client step",step)
            step += 1
            iv = response[:12]
            ciphertext = response[12:]
            print(len(iv),len(ciphertext))
            content : str= self.session_cipher.decrypt(iv, ciphertext, None)
            print("client step",step)
            step += 1
            print(content)
            result = json.loads(content)
            return QueryResult(result,self)
        except Exception as e:
            raise RuntimeError(e)
    def authenticate(self):
        try:
            response = self.client.put(self.url,data=blake3.blake3(self.secret_key).digest(32))
            payload = response.content
            session_id_cipher = payload[1:]
            iv = session_id_cipher[:12]
            ciphertext = session_id_cipher[12:]
            self.session_id = self.cipher.decrypt(iv, ciphertext, None)  
            self.session_cipher = AESGCM(self.session_id)  
            self.session_id_hash = blake3.blake3(self.session_id).digest(32)
            self.authenticated = True
            
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {e}")
