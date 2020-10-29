import ubinascii

def hex_to_bytes(hex_string):
    i = 0
    arr = []
    while (i < len(hex_string)):
        arr.append((int(hex_string[i],16) << 4) | int(hex_string[i + 1],16))
        i+=2
    return bytes(arr)

b64 = "eyJzaWduIjogIjMwNDQwMjIwMzg1N2UxZTQxNGM4MmVhODVjMzk4ZjVmZDI5ZGZiZmE0NGQ1Njg5OGNmNjU3OGI0NTBmMmUxZDNhMjY5ZTc5ZTAyMjAyZmI3YTNkYjU0OTI2M2ZiZTE2ZjAwN2QwYmFjMmU0ZGNjNmVmZjkyYjg2YTEzNTliNDI1ZWVmZmI1YzIwOGU1In0=="
# b64 = b64.encode("utf-8")

print(ubinascii.a2b_base64(b64).decode('utf-8'))