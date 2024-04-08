from requests import get
from os import system
from time import sleep
from datetime import datetime
from typing import Union
from enum import Enum

class time_formats(Enum):
    AMPM = 0
    MILITARY = 1


def read_dotenv():
    ret = {}
    with open("./.env", "r") as f:
        for line in f.readlines():
            name, value = line.split("=")
            ret[name] = str(value).replace("\n", "")
    
    return ret

DOT_ENV = read_dotenv()

def get_data(team_number = 4611, event_key="2024ohmv"):
    BASE_URL = "https://www.thebluealliance.com/api/v3"
    HEADER_KEY = "X-TBA-Auth-Key"
    API_KEY = DOT_ENV["key"]


    return get(f"{BASE_URL}/team/frc{team_number}/event/{event_key}/matches", headers={HEADER_KEY:API_KEY}).json()



def get_match_type(match):
    return "Qualifiers" if match["comp_level"] == "qm" else "Playoffs"


def output(format: time_formats = time_formats.AMPM, data = get_data()):
    t = datetime.now().strftime("%H:%M:%S")

    if format == time_formats.AMPM:
        t = [int(x) for x in t.split(":")]
        if t[0] > 12:
            t = f"{t[0]-12:02}:{t[1]:02}:{t[2]:02}PM"
        else:
            t = f"{t[0]:02}:{t[1]:02}:{t[2]:02}AM"

    system('cls')
    print(f"We have completed {index} matches")
    print(f'Watching for match {data[index]["match_number"]} upload! {t}')
    sleep(1)

data = get_data()

index = 0

for match in data:
    if match["videos"] != []:
        index += 1

output(data=data)

while True:
    data = get_data()

    match = data[index]

    if match["videos"] != []:
        index += 1

        print(f"{get_match_type(match)} Match {f"{match['match_number']} " if get_match_type(match) == "Qualifiers" else ""}was uploaded! Watch at: ")
        sleep(1)
        print(f'\thttps://youtube.com/watch/{match["videos"][0]["key"]}')
        sleep(10)

    if index == len(data):
        print("You have completed all of your matches!")
        exit(0)
    else:
        output(data=data)