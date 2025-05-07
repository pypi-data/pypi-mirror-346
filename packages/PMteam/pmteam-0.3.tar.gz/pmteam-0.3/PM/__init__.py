import base64
import codecs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import marshal, zlib, string, random, os
def use():
    print('''1. التشفير الأساسي Base64
encode_base64(text) و decode_base64(encoded)
> يستخدمان ترميز base64 لتشفير النصوص أو إعادتها للنص الأصلي.
---
2. تشفير XOR (متماثل - symmetric)
encrypt_xor(text, key) و decrypt_xor(cipher, key)
> يستخدم XOR بين كل حرف والنص المفتاح. XOR متماثل، لذا التشفير وفك التشفير نفس العملية.
---
3. التشفير AES
encrypt_aes(text, key) و decrypt_aes(enc_text, key)
> يستخدم خوارزمية AES في وضع CBC مع مفتاح مشتق من SHA-256، ويوفّر تشفير قوي ومعتمد.
---
4. التشفير المعكوس
encrypt_reverse(text) و decrypt_reverse(text)
> يقوم بعكس النص، وفي نسخة محسنة يتم أيضًا توليد Hash لمطابقة صحة البيانات.
---
5. تشفير القيصر Caesar
caesar(text, shift) و decaesar(text, shift)
> يحرك الحروف الأبجدية بعدد معين من الخانات، نوع بدائي من التشفير.
---
6. rot13
rot13(text)
> خوارزمية بسيطة تعتمد على تدوير الحروف 13 خانة. قابلة للعكس ذاتيًا.
---
7. تشفير بالطبقات (Layered Encoding)
encrypt_layer1(code) و decrypt_layer1(data)
> تضغط النص باستخدام zlib ثم تُحوّل بـ marshal ثم base64 ثم hex. قوية ضد التحليل اليدوي.
---
8. marshal & zlib
encrypt_zlib() / decrypt_zlib()
encrypt_marshal() / decrypt_marshal()
encrypt_marshal_pro() / decrypt_marshal_pro()
> تستخدم Marshal لحفظ البيانات بشكل خام (binary) و zlib لضغط البيانات. النسخة “pro” تتحقق أيضًا من سلامة البيانات عبر Hash.
---
9. التشفير بالاستبدال (Substitution Cipher)
encrypt_substitute() / decrypt_substitute()
> ينشئ مفتاح تبديل عشوائي للحروف، ويتم استخدامه لترجمة كل حرف.
---
10. تقطيع النص وترتيبه عشوائيًا
encrypt_blocks() / decrypt_blocks()
> يقسم النص إلى كتل، يضع لكل كتلة رقمًا، ويغير ترتيبها. يتم إعادتها بترتيب الرقم.
---
11. مفتاح ديناميكي (Dynamic Key XOR)
encrypt_dynamic_key() / decrypt_dynamic_key()
> يولد مفتاحًا من MD5 للنص، ويشفّر باستخدام XOR مع بعض الزيادة
---
12. التشفير المتقدم متعدد الطبقات
encrypt_advanced() / decrypt_advanced()
> zlib + base64 + reverse + hex = تشفير طبقي متداخل، يصعب التحليل
---
13. تشفير شامل مع التحقق (Encrypt Sajad Source)

encrypt_all() / decrypt_all()

> يجزئ النص حسب مفتاح عشوائي من 16 بايت، يضيف checksum، ثم يستخدم XOR + base64. قوي جدًا ومناسب للحماية من التلاعب.''')
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
    #Encrypt Sajad Source
    def encrypt_all(self, data: str):
        k = os.urandom(16)
        r = []
        data_bytes = data.encode()
        for i in range(0, len(data_bytes), len(k)):
            ch = data_bytes[i:i+len(k)]
            chs = ch + bytes([sum(ch) % 256])
            enc = bytes([chs[j] ^ k[j % len(k)] for j in range(len(chs))])
            r.append((base64.b64encode(enc).decode(), base64.b64encode(k).decode()))
        return r
    def decrypt_all(self, data):
        result = bytearray()
        for c, k in data:
            c_dec = base64.b64decode(c)
            k_dec = base64.b64decode(k)
            dec = bytearray([z ^ y for z, y in zip(c_dec, (k_dec * ((len(c_dec) // len(k_dec)) + 1))[:len(c_dec)])])
            if sum(dec[:-1]) % 256 == dec[-1]:
                result += dec[:-1]
            else:
                raise ValueError("Checksum mismatch!")
        return result.decode('utf-8')