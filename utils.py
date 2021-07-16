from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')

BOHCHU = int(os.getenv('BOHCHU'))
BUNYOD = int(os.getenv('BUNYOD'))
HANS = int(os.getenv('HANS'))
PRAG = int(os.getenv('PRAG'))
YILIN = int(os.getenv('YILIN'))
JEFF = int(os.getenv('JEFF'))
LYNN = int(os.getenv('LYNN'))
THILA = int(os.getenv('THILA'))
TZERYEE = int(os.getenv('TZERYEE'))
admins = [BOHCHU, BUNYOD, HANS, PRAG, YILIN, JEFF, LYNN, THILA, TZERYEE]

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

FD1 = os.getenv('FD1')
FD2 = os.getenv('FD2')
FD3 = os.getenv('FD3')
FD4 = os.getenv('FD4')
FD5 = os.getenv('FD5')
FD6 = os.getenv('FD6')
FD7 = os.getenv('FD7')
FD8 = os.getenv('FD8')
forms = [FD1, FD2, FD3, FD4, FD5, FD6, FD7, FD8]

PRAG_PADLET = os.getenv('PRAG_PADLET')

# console colours
reset = '\u001b[0m'
red = '\u001b[31m'
green = '\u001b[32m'
