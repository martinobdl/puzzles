import base64

with open("key.txt", "rb") as f:
    encoded = base64.b64encode(f.read())
    print(encoded.decode('utf-8'))
