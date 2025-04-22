import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from openai import AzureOpenAI

import time
import pandas as pd
from datetime import  datetime





def HTML_reader(message_HTML_file, dataframe):
    # Reads the HTML file
    with open(message_HTML_file, 'r', errors="ignore") as local_HTML:
        content = local_HTML.read()  # Reads the local HTML file
        soup = BeautifulSoup(content, "lxml")  # Creates soup object

    # Finds all the message blocks in the file
    message_soup = soup.find_all('div', class_='pam _3-95 _2ph- _a6-g uiBoxWhite noborder')
    sorted_message_list = []

    for message in message_soup:
        sorted_message_list.append(message)

    # Inverts the list so that it starts at the very beginning
    inverted_list = list(reversed(sorted_message_list))

    for message in inverted_list:

        # Here the sender, the message, and the time are extracted
        sender_block = message.find('div', class_='_3-95 _2pim _a6-h _a6-i').text
        message_block = message.find('div', class_='_3-95 _a6-p').text
        time_block = message.find('div', class_='_3-94 _a6-o').text
        print(time_block)
        dt = datetime.strptime(time_block, "%b %d, %Y %I:%M %p")
        print(dt)

        content_list = [sender_block, message_block, time_block]
        dataframe.loc[len(dataframe)] = content_list

    return dataframe

if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    resources_dir_text = "Resources_Path.txt"

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    input_dir = resources_dir / "Input"

    # Creates the dataframe
    df = pd.DataFrame(columns=['Sender', 'Message', 'Time'])

    for file in input_dir.iterdir():
        df = HTML_reader(file, df)


    print(f"Senders Involed: {df['Sender'].unique()}")

    file_name = str(input("Input File Name: "))

    global_output_dir = resources_dir / "Output"

    if not global_output_dir.exists():
        os.mkdir(global_output_dir)

    global_chat_file = global_output_dir / f"{file_name}.xlsx"
    df.to_excel(global_chat_file, sheet_name='Conversation', index=False)