from openai import OpenAI
import base64
import json
import os
from urllib.parse import urlparse


def rot13_encrypt(input_string):
    result = ''
    for char in input_string:
        char_code = ord(char)

        if 65 <= char_code <= 90:
            result += chr(((char_code - 65 + 13) % 26) + 65)
        elif 97 <= char_code <= 122:
            result += chr(((char_code - 97 + 13) % 26) + 97)
        else:
            result += char

    return result


os.environ["OPENAI_API_KEY"] = rot13_encrypt("fx-cebw-YBlVcFEOf92bDUbcQATmG3OyoxSWTNJh8mm11FPdrYA9V3zU")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# hna ghadi tcreer fih ghadi tsava data dialak
data_directory = "./Data"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

image_local = './*'
image_url = f"data:image/jpeg;base64,{encode_image(image_local)}"


client = OpenAI()

response = client.chat.completions.create(
    model='gpt-4-vision-preview',
    messages=[
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "Return JSON document with data. Only return JSON not other text"},
                {
                    "type": "image_url",
                    "image_url": {"url": image_url}
                }
            ],
        }
    ],
    max_tokens=500,
)

# Extract JSON data from the response and remove Markdown formatting
json_string = response.choices[0].message.content
json_string = json_string.replace("json\n", "").replace("\n", "")

# Parse the string into a JSON object
json_data = json.loads(json_string)

filename_without_extension = os.path.splitext(os.path.basename(urlparse(image_url).path))[0] #for URL image
#filename_without_extension = os.path.splitext(os.path.basename(image_local))[0] #for local image

# Add .json extension to the filename
json_filename = f"{filename_without_extension}.json"

# Save the JSON data to a file with proper formatting
with open(os.path.join(data_directory, json_filename), 'w') as file:
    json.dump(json_data, file, indent=4)

print(f"JSON data saved to {os.path.join(data_directory, json_filename)}")
