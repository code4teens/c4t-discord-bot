import os

token = os.getenv('TOKEN')
guild = int(os.getenv('GUILD'))
devs = int(os.getenv('ROLE_DEVS'))
students = int(os.getenv('ROLE_STUDENTS'))
student_bots = int(os.getenv('ROLE_STUDENT_BOTS'))
dev_terminal = int(os.getenv('CHANNEL_DEV_TERMINAL'))
dev_log = int(os.getenv('CHANNEL_DEV_LOG'))
imp_alerts = int(os.getenv('CHANNEL_IMP_ALERTS'))
imp_coc = int(os.getenv('CHANNEL_IMP_COC'))
stu_chit_chat = int(os.getenv('CHANNEL_STU_CHIT_CHAT'))
stu_ttb = int(os.getenv('CHANNEL_STU_TTB'))

#\U0001F197
ok_emoji = '🆗'

#\U00002705
tick_emoji = '✅'

#\U0000274C
cross_emoji = '❌'

dev_command_list = [
  '$devhelp',
  '$attach',
  '$devecho'
]

dev_help_text = (
  '```fix\n'
  '$attach  - Sends attachment with description to specified channel.\n'
  '$devecho - Sends message to specified channel.\n'
  '```'
)

help_text = (
  '```fix\n'
  '$help        - Shows (all?) commands.\n'
  '$hello       - d03 ex04\n'
  '$greet       - d03 ex05\n'
  '$echo        - d04 ex01\n'
  '$say         - d04 ex02\n'
  '$rock        - d04 ex04\n'
  '$paper       - d04 ex04\n'
  '$scissors    - d04 ex04\n'
  '$emoji       - d05 ex00\n'
  '$embed_emoji - d05 ex01\n'
  '$gif         - d05 ex02\n'
  '$intro       - d05 ex03\n'
  '$img         - d05 ex04\n'
  '$react       - d05 ex05\n'
  '$new         - d06 ex00\n'
  '$list        - d06 ex01\n'
  '$delete      - d06 ex02\n'
  '$del_list    - d06 ex03\n'
  '$currency    - d07 ex00\n'
  '$job         - d07 ex01\n'
  '$movie       - d07 ex02\n'
  '$joke        - d08 ex00\n'
  '$ip          - d08 ex01\n'
  '$iplocation  - d08 ex02 & 03\n'
  '```'
)

rpslist = [
  '$rock',
  '$paper',
  '$scissors'
]

rpsans = [
  'I choose rock!',
  'I choose paper!',
  'I choose scissors!'
]

winlist = [
'You win!',
'You won!',
'Wow, you beat me!'
]

loselist = [
  'You lose!',
  'You lost!',
  'Better luck next time!'
]

tielist  = [
  'It\'s a tie!',
  'We tied!',
  'Great minds think alike!'
]

attach_regex = '\$attach <#[0-9]{18}> .+'
devecho_regex = '\$devecho <#[0-9]{18}> .+'
add_bot_regex = '\$addbot https://discord.com/api/oauth2/authorize\?client_id=[0-9]{18}&permissions=[0-9]+&scope=bot'