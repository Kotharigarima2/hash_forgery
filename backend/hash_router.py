from backend.md2_handler import generate_md2_hash


def route_hash(algorithm: str, data: bytes) -> str:
    algo = algorithm.upper()
    if algo == "MD2":
        return generate_md2_hash(data)
    
    else:
        return f"Unsupported algorithm: {algorithm}"
