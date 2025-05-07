import base64
import codecs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import marshal, zlib, string, random 
class UltraCrypt:
    def encode_base64(self, text: str) -> str:
        return base64.b64encode(text.encode()).decode()
    def decode_base64(self, encoded: str) -> str:
        return base64.b64decode(encoded.encode()).decode()
    def encrypt_xor(self, text: str, key: str) -> str:
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
    def decrypt_xor(self, cipher: str, key: str) -> str:
        return self.encrypt_xor(cipher, key)  # XOR is symmetric
    def encrypt_aes(self, text: str, key: str) -> str:
        key_hash = hashlib.sha256(key.encode()).digest()
        cipher = AES.new(key_hash, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode()
    def decrypt_aes(self, enc_text: str, key: str) -> str:
        key_hash = hashlib.sha256(key.encode()).digest()
        raw = base64.b64decode(enc_text)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(key_hash, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode()
    def encrypt_reverse(self, text: str) -> str:
        return text[::-1]
    def decrypt_reverse(self, text: str) -> str:
        return text[::-1]
    def caesar(self, text: str, shift: int = 3) -> str:
        result = ''
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result += chr((ord(char) - base + shift) % 26 + base)
            else:
                result += char
        return result
    def decaesar(self, text: str, shift: int = 3) -> str:
        return self.encrypt_caesar(text, -shift)
    def rot13(self, text: str) -> str:
        return codecs.encode(text, 'rot_13')
    def encrypt_layer1(self, code: str) -> str:
        compressed = zlib.compress(code.encode())
        marshaled = marshal.dumps(compressed)
        encoded = base64.b64encode(marshaled)
        return encoded.hex()
    def decrypt_layer1(self, data: str) -> str:
        decoded = base64.b64decode(bytes.fromhex(data))
        decompressed = marshal.loads(decoded)
        return zlib.decompress(decompressed).decode()
    def encrypt_xor(self, text: str, key: str) -> str:
        xored = ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
        return base64.b64encode(xored.encode()).decode()
    def decrypt_xor(self, text: str, key: str) -> str:
        decoded = base64.b64decode(text).decode()
        return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))
    def encrypt_caesar(self, text: str, shift: int = 13) -> str:
        return ''.join(chr((ord(char) + shift) % 256) for char in text)
    def decrypt_caesar(self, text: str, shift: int = 13) -> str:
        return ''.join(chr((ord(char) - shift) % 256) for char in text)
    def encrypt_zlib(self, text: str) -> str:
        return base64.b64encode(zlib.compress(text.encode())).decode()
    def decrypt_zlib(self, text: str) -> str:
        return zlib.decompress(base64.b64decode(text)).decode()
    def encrypt_marshal(self, text: str) -> str:
        hashed = hashlib.md5(text.encode()).hexdigest()
        marshaled = marshal.dumps((text, hashed))
        return base64.b64encode(marshaled).decode()
    def decrypt_marshal(self, data: str) -> str:
        text, stored_hash = marshal.loads(base64.b64decode(data))
        real_hash = hashlib.md5(text.encode()).hexdigest()
        if stored_hash != real_hash:
            return "[!] Tampered or corrupted data"
        return text
    def encrypt_marshal_pro(self, text: str) -> str:
        compressed = zlib.compress(text.encode())
        hashed = hashlib.sha256(text.encode()).hexdigest()
        payload = (compressed, hashed)
        dumped = marshal.dumps(payload)
        encoded = base64.b64encode(dumped).decode()
        return encoded
    def decrypt_marshal_pro(self, data: str) -> str:
        try:
            decoded = base64.b64decode(data)
            compressed, hashed = marshal.loads(decoded)
            text = zlib.decompress(compressed).decode()
            if hashlib.sha256(text.encode()).hexdigest() != hashed:
                return "[!] Integrity check failed."
            return text
        except Exception as e:
            return f"[!] Error: {e}"
    def encrypt_reverse(self, text: str) -> str:
        rev = text[::-1]
        hashed = hashlib.md5(rev.encode()).hexdigest()
        enc = base64.b64encode(f"{rev}:{hashed}".encode()).decode()
        return enc
    def decrypt_reverse(self, data: str) -> str:
        raw = base64.b64decode(data).decode()
        rev, hashval = raw.rsplit(":", 1)
        if hashlib.md5(rev.encode()).hexdigest() != hashval:
            return "[!] Invalid hash"
        return rev[::-1]
    def encrypt_substitute(self, text: str) -> str:
        key = ''.join(random.sample(string.printable, len(string.printable)))
        table = str.maketrans(string.printable, key)
        encrypted = text.translate(table)
        return base64.b64encode(f"{key}|||{encrypted}".encode()).decode()
    def decrypt_substitute(self, data: str) -> str:
        decoded = base64.b64decode(data).decode()
        key, enc = decoded.split("|||")
        table = str.maketrans(key, string.printable)
        return enc.translate(table)
    def encrypt_blocks(self, text: str) -> str:
        parts = [text[i:i+3] for i in range(0, len(text), 3)]
        indexed = [f"{i}:{part}" for i, part in enumerate(parts)]
        random.shuffle(indexed)
        return '|'.join(indexed)
    def decrypt_blocks(self, data: str) -> str:
        try:
            parts = data.split('|')
            ordered = sorted(parts, key=lambda x: int(x.split(':')[0]))
            return ''.join(p.split(':', 1)[1] for p in ordered)
        except:
            return "[!] Failed to decrypt."
    def encrypt_dynamic_key(self, text: str) -> str:
        key = hashlib.md5(text.encode()).hexdigest()[:16]
        encrypted = ''.join(chr((ord(c) ^ ord(key[i % len(key)])) + 3) for i, c in enumerate(text))
        return base64.b64encode(encrypted.encode()).decode()
    def decrypt_dynamic_key(self, data: str) -> str:
        decoded = base64.b64decode(data).decode()
        key = hashlib.md5(decoded.encode()).hexdigest()[:16]
        decrypted = ''.join(chr((ord(c) - 3) ^ ord(key[i % len(key)])) for i, c in enumerate(decoded))
        return decrypted
    def encrypt_advanced(self, text: str) -> str:
        layer1 = zlib.compress(text.encode())
        layer2 = base64.b64encode(layer1)[::-1]
        return layer2.hex()
    def decrypt_advanced(self, data: str) -> str:
        try:
            step1 = bytes.fromhex(data)[::-1]
            decompressed = zlib.decompress(base64.b64decode(step1))
            return decompressed.decode()
        except Exception as e:
            return f"[!] Error: {e}"