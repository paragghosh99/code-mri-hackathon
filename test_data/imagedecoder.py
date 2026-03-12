import base64

with open("repo.jpg", "rb") as img:
    encoded = base64.b64encode(img.read()).decode()

with open("base64.txt", "w") as f:
    f.write(encoded)

print("Base64 saved to base64.txt")