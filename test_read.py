import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from openai import AzureOpenAI

import time

script_path = Path(__file__).resolve()
project_dir = script_path.parent
os.chdir(project_dir)
sys.path.append(str(project_dir))




resources_dir_text = "Resources_Path.txt"

with open(resources_dir_text, 'a') as writer:
    pass

# Read the directory

entry_list = []

with open(resources_dir_text, 'r') as reader:
    entry_list.append(reader.read())

# Create the necessary folders

if entry_list[0]:
    resources_dir = Path(str(entry_list[0]).replace('"', ''))
    print(f"Resources Directory: {resources_dir}")



api_detail_path = resources_dir / "API Key.txt"

with open(api_detail_path, "r") as api_detail:
    api_detail_list = api_detail.read().splitlines()

API = api_detail_list[0]
endpoint = api_detail_list[1]
version = api_detail_list[2]
deployment_name = api_detail_list[3]

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=API,
    api_version=version,
)

system_prompt = """
You give insight on the message provided
"""

message_list = [
    {
        "role": "system",
        "content": system_prompt,
    }
]







def reader(HTML_file):
    with open(HTML_file, 'r', errors="ignore") as local_HTML:
        content = local_HTML.read()  # Reads the local HTML file
        soup = BeautifulSoup(content, "lxml")  # Creates soup object

    print(soup)

    message_soup = soup.findAll('div', class_='pam _3-95 _2ph- _a6-g uiBoxWhite noborder')

    print(message_soup)

    print(len(message_soup))
    print(type(message_soup))

    sorted_message_list = []

    for message in message_soup:
        sorted_message_list.append(message)

    print(len(sorted_message_list))

    inverted_list = list(reversed(sorted_message_list))

    print(len(inverted_list))

    for message in inverted_list:
        sender_block = message.find('div', class_='_3-95 _2pim _a6-h _a6-i').text
        message_block = message.find('div', class_='_3-95 _a6-p').text
        time_block = message.find('div', class_='_3-94 _a6-o').text
        # print(f"Sender: {sender_block} | Message: {message_block} | Time: {time_block}")

        complete_block = f"Sender: {sender_block} | Message: {message_block} | Time: {time_block}"

        user_prompt = complete_block

        message_list.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        response = client.chat.completions.create(
            model=deployment_name,
            messages=message_list,
        )

        response_message = response.choices[0].message

        print(f"Response: {response_message.content}")

        time.sleep(5)


with open("Resources_Path.txt", "r") as resources_text:
    resources_dir = Path(str(resources_text.readline()).replace('"', ''))

input_dir = resources_dir / "Input"

for file in input_dir.iterdir():
    print(file)

    reader(file)