# backend/md4_handler.py

import struct


class MD4:
    def __init__(self, message=b"", A=0x67452301, B=0xefcdab89, C=0x98badcfe, D=0x10325476, count=0):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.buffer = b""
        self.count = count  # total bytes processed
        if message:
            self.update(message)

    def update(self, data):
        self.buffer += data
        self.count += len(data)
        while len(self.buffer) >= 64:
            self._compress(self.buffer[:64])
            self.buffer = self.buffer[64:]

    def digest(self):
        total_bits = self.count * 8
        self.update(b'\x80')
        while len(self.buffer) % 64 != 56:
            self.update(b'\x00')
        self.update(struct.pack("<Q", total_bits))
        return struct.pack("<4I", self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return self.digest().hex()

    def _F(self, x, y, z): return (x & y) | (~x & z)
    def _G(self, x, y, z): return (x & y) | (x & z) | (y & z)
    def _H(self, x, y, z): return x ^ y ^ z

    def _left_rotate(self, x, n):
        x &= 0xFFFFFFFF
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    def _compress(self, block):
        X = list(struct.unpack("<16I", block))
        A, B, C, D = self.A, self.B, self.C, self.D

        S = [3, 7, 11, 19]
        for i in range(0, 16, 4):
            A = self._left_rotate((A + self._F(B, C, D) + X[i]) & 0xFFFFFFFF, S[0])
            D = self._left_rotate((D + self._F(A, B, C) + X[i+1]) & 0xFFFFFFFF, S[1])
            C = self._left_rotate((C + self._F(D, A, B) + X[i+2]) & 0xFFFFFFFF, S[2])
            B = self._left_rotate((B + self._F(C, D, A) + X[i+3]) & 0xFFFFFFFF, S[3])

        S = [3, 5, 9, 13]
        for i in range(0, 4):
            A = self._left_rotate((A + self._G(B, C, D) + X[i] + 0x5a827999) & 0xFFFFFFFF, S[0])
            D = self._left_rotate((D + self._G(A, B, C) + X[i+4] + 0x5a827999) & 0xFFFFFFFF, S[1])
            C = self._left_rotate((C + self._G(D, A, B) + X[i+8] + 0x5a827999) & 0xFFFFFFFF, S[2])
            B = self._left_rotate((B + self._G(C, D, A) + X[i+12] + 0x5a827999) & 0xFFFFFFFF, S[3])

        S = [3, 9, 11, 15]
        order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for i in range(0, 16, 4):
            A = self._left_rotate((A + self._H(B, C, D) + X[order[i]] + 0x6ed9eba1) & 0xFFFFFFFF, S[0])
            D = self._left_rotate((D + self._H(A, B, C) + X[order[i+1]] + 0x6ed9eba1) & 0xFFFFFFFF, S[1])
            C = self._left_rotate((C + self._H(D, A, B) + X[order[i+2]] + 0x6ed9eba1) & 0xFFFFFFFF, S[2])
            B = self._left_rotate((B + self._H(C, D, A) + X[order[i+3]] + 0x6ed9eba1) & 0xFFFFFFFF, S[3])

        self.A = (self.A + A) & 0xFFFFFFFF
        self.B = (self.B + B) & 0xFFFFFFFF
        self.C = (self.C + C) & 0xFFFFFFFF
        self.D = (self.D + D) & 0xFFFFFFFF


def md4_padding(original_length: int) -> bytes:
    pad = b'\x80'
    pad += b'\x00' * ((56 - (original_length + 1) % 64) % 64)
    pad += struct.pack("<Q", original_length * 8)
    return pad


def generate_md4_hash(data: bytes) -> str:
    return MD4(data).hexdigest()


def forge_md4(original_data: bytes, append_data: bytes) -> dict:
    # Step 1: compute original hash
    original_md4 = MD4(original_data)
    original_hash = original_md4.hexdigest()
    A, B, C, D = struct.unpack("<4I", bytes.fromhex(original_hash))

    # Step 2: compute glue padding for original length
    glue_padding = md4_padding(len(original_data))

    # Step 3: create forged MD4 with internal state
    new_len = len(original_data) + len(glue_padding)
    forged_md4 = MD4(append_data, A, B, C, D, count=new_len)
    forged_hash = forged_md4.hexdigest()

    return {
        "original_hash": original_hash,
        "forged_data": original_data + glue_padding + append_data,
        "forged_hash": forged_hash
    }
