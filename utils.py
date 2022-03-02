from datetime import datetime
from dotenv import load_dotenv
import os

import pytz
import requests

# environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')
BOT_PERM = int(os.getenv('BOT_PERM'))
C4T_DPY_ALPHA = int(os.getenv('C4T_DPY_ALPHA'))
C4T_DPY_BETA = int(os.getenv('C4T_DPY_BETA'))
C4T_DPY_DEC2021 = int(os.getenv('C4T_DPY_DEC2021'))
C4T_DPY_TEST = int(os.getenv('C4T_DPY_TEST'))
C4W_DPY_FEB2022 = int(os.getenv('C4W_DPY_FEB2022'))
C4T_DPY_MAR2022 = int(os.getenv('C4T_DPY_MAR2022'))

# console colours
reset = '\u001b[0m'
red = '\u001b[31m'
green = '\u001b[32m'

# localisation
tz = pytz.timezone('Asia/Kuala_Lumpur')

# requests session
s = requests.Session()
s.headers.update({'api-key': API_KEY})


# helper functions
def now():
    return datetime.now(tz)


def get_active_cohort():
    url = f'{API_URL}/cohorts/active'
    r = s.get(url, timeout=10)

    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    return r.json()


# global variables
guild_id = None
active_cohort = get_active_cohort()
c4t_dpy = [
    C4T_DPY_ALPHA, C4T_DPY_BETA, C4T_DPY_DEC2021, C4T_DPY_MAR2022, C4T_DPY_TEST
]
c4w_dpy = [C4W_DPY_FEB2022]
dpy = c4t_dpy + c4w_dpy
