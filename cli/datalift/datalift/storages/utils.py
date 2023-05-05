import uuid


def generate_filename() -> str:
    return str(uuid.uuid4())
