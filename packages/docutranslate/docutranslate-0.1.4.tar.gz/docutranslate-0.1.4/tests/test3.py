from io import BytesIO
file_like = BytesIO(b'this is a sample bytearray')
print(file_like.read())