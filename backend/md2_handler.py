from Crypto.Hash import MD2

def generate_md2_hash(data: bytes) -> str:
    hasher = MD2.new()
    hasher.update(data)
    return hasher.hexdigest()
