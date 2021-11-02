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
COC_MSG_ID = int(os.getenv('COC_MSG_ID'))
BOT_PERM = int(os.getenv('BOT_PERM'))

COC = os.getenv('COC')
GUIDE = os.getenv('GUIDE')
PD1 = os.getenv('PD1')
PD2 = os.getenv('PD2')
PD3 = os.getenv('PD3')
PD4 = os.getenv('PD4')
PD5 = os.getenv('PD5')
PD6 = os.getenv('PD6')
PD7 = os.getenv('PD7')
PD8 = os.getenv('PD8')
PD9 = os.getenv('PD9')
projects = [PD1, PD2, PD3, PD4, PD5, PD6, PD7, PD8, PD9]

PRAG_PADLET = os.getenv('PRAG_PADLET')

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
    r = s.get(url, timeout=5)

    if r.status_code != requests.codes.ok:
        r.raise_for_status()

    return r.json()


# global variables
guild_id = None
active_cohort = get_active_cohort()
