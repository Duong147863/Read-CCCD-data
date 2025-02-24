import requests

url = "http://10.2.0.116:5000/extract_text"
image_path = "cccd.jpg"

with open(image_path, "rb") as img_file:
    files = {"image": img_file}
    response = requests.post(url, files=files)

print(response.json())
