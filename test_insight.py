import os
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from openai import AzureOpenAI

import time
import pandas as pd
from datetime import  datetime



if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    resources_dir_text = "Resources_Path.txt"

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))

    segmented_dir = resources_dir / "Segmented"

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

    for conversation in segmented_dir.iterdir():
        current_df = pd.read_excel(conversation)

        system_prompt = """
            You are a helpful personal secretary. Provide summary and insights on the conversation. 
            Take note of the sender as that information might come in handy
            
            
            Give me the output in the following format.
            
            Summary of the Day
            --------------------------------
            
            [Insert a detailed summary of the conversation here. The summary should cover everything that is important that was sent during that day]
            
            Key Insights
            --------------------------------
            
            1. [Insight number 1]
            2. [Insight number 2]
            ......
            
            For the insights, try to limit it to 5 insights maximum. If the day only has a x<5 insights, then just show the x insights
        
            """

        message_list = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        count = 0

        for index, row in current_df.iterrows():
            count += 1
            sender_content = row['Sender']
            message_content = row['Message']
            time_content = row['Time']

            message_block = f"Message Number: {count} | Sender: {sender_content} | Time Sent: {time_content} | Message Content: {message_content}"

            message_list.append(
                {
                    "role": "user",
                    "content": message_block,
                }
            )


        response = client.chat.completions.create(
            model=deployment_name,
            messages=message_list,
        )

        response_message = response.choices[0].message

        print(f"{conversation.name}\n{response_message.content}\n\n")

        time.sleep(5)