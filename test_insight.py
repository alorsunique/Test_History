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

    for conversation in segmented_dir.iterdir():
        print(conversation)