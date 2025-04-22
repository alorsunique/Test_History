import os
import shutil
import sys
from pathlib import Path

from Tools.scripts.dutree import display
from bs4 import BeautifulSoup
from openai import AzureOpenAI

import time
import pandas as pd
from datetime import  datetime







def extract_time(dataframe):
    time_block_list = dataframe['Time'].tolist()

    year_list = []
    month_list = []
    day_list = []

    hour_list = []
    minute_list = []

    for entry in time_block_list:

        dt = datetime.strptime(entry, "%b %d, %Y %I:%M %p")

        year = dt.year
        month = dt.month
        day = dt.day

        hour = dt.hour
        minute = dt.minute

        year_list.append(year)
        month_list.append(month)
        day_list.append(day)

        hour_list.append(hour)
        minute_list.append(minute)

    return year_list,month_list,day_list,hour_list,minute_list




def day_segment(dataframe, earliest_year, earliest_month, earliest_day, day_output_dir):

    current_datetime = datetime.now()
    current_year = current_datetime.year

    year_counter = earliest_year
    month_counter = earliest_month
    day_counter = earliest_day

    while year_counter <= current_year:

        while month_counter <= 12:

            while day_counter <= 31:

                year_frame = dataframe.loc[dataframe['Year'] == year_counter]
                month_frame = year_frame.loc[year_frame['Month'] == month_counter]
                day_frame = month_frame.loc[month_frame['Day'] == day_counter]



                if not day_frame.empty:
                    output_file = f"{year_counter:04}{month_counter:02}{day_counter:02}_Conversation.xlsx"
                    output_path = day_output_dir / output_file

                    day_frame.to_excel(output_path, sheet_name='Conversation', index=False)



                day_counter+=1

            day_counter = 1
            month_counter += 1

        month_counter = 1
        year_counter += 1







if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_dir = script_path.parent
    os.chdir(project_dir)
    sys.path.append(str(project_dir))

    resources_dir_text = "Resources_Path.txt"

    with open("Resources_Path.txt", "r") as resources_text:
        resources_dir = Path(str(resources_text.readline()).replace('"', ''))


    global_output_dir = resources_dir / "Output"

    for file in global_output_dir.iterdir():
        print(file)

        global_df = pd.read_excel(file)
        time_block = global_df.iloc[0]['Time']

        year_list,month_list,day_list,hour_list,minute_list = extract_time(global_df)
        earliest_year = year_list[0]
        earliest_month = month_list[0]
        earliest_day = day_list[0]

        global_df["Year"] = year_list
        global_df["Month"] = month_list
        global_df["Day"] = day_list
        global_df["Hour"] = hour_list
        global_df["Minute"] = minute_list

        segmented_dir = resources_dir / "Segmented"
        if segmented_dir.exists():
            shutil.rmtree(segmented_dir)
        if not segmented_dir.exists():
            os.mkdir(segmented_dir)

        day_segment(global_df,earliest_year,earliest_month,earliest_day,segmented_dir)
