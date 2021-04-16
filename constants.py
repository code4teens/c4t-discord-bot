import os

token = os.getenv('TOKEN')
guild_id = int(os.getenv('GUILD'))
r_devs_id = int(os.getenv('ROLE_DEVS'))
r_students_id = int(os.getenv('ROLE_STUDENTS'))
r_student_bots_id = int(os.getenv('ROLE_STUDENT_BOTS'))
r_village1_id = int(os.getenv('ROLE_VILLAGE_1'))
r_village2_id = int(os.getenv('ROLE_VILLAGE_2'))
r_village3_id = int(os.getenv('ROLE_VILLAGE_3'))
r_village4_id = int(os.getenv('ROLE_VILLAGE_4'))
r_village5_id = int(os.getenv('ROLE_VILLAGE_5'))
c_dev_terminal_id = int(os.getenv('CHANNEL_DEV_TERMINAL'))
c_dev_log_id = int(os.getenv('CHANNEL_DEV_LOG'))
c_imp_alerts_id = int(os.getenv('CHANNEL_IMP_ALERTS'))
c_imp_coc_id = int(os.getenv('CHANNEL_IMP_COC'))
c_imp_introduction_id = int(os.getenv('CHANNEL_IMP_INTRODUCTION'))
c_stu_chit_chat_id = int(os.getenv('CHANNEL_STU_CHIT_CHAT'))
c_stu_ttb_id = int(os.getenv('CHANNEL_STU_TTB'))

#\U0001F197
ok_emoji = '🆗'

#\U00002705
tick_emoji = '✅'

#\U0000274C
cross_emoji = '❌'

attach_regex = '\$attach <#[0-9]{18}> .+'
devecho_regex = '\$devecho <#[0-9]{18}> .+'
addbot_regex = '\$addbot https://discord.com/api/oauth2/authorize\?client_id=[0-9]{18}&permissions=[0-9]+&scope=bot'
adopt_regex = '\$adopt <@![0-9]{18}>'
release_regex = '\$release <@![0-9]{18}>'

dev_help_text = (
  '```fix\n'
  '$assign  - Assigns students into villages.\n'
  '$attach  - Sends attachment with description to specified channel.\n'
  '$devecho - Sends message to specified channel.\n'
  '```'
)

help_text = (
  '```fix\n'
  '$help    - Shows (all?) commands.\n'
  '$addbot  - Adds bot to server.\n'
  '$adopt   - Adopts bot into your village\n'
  '$release - Releases bot from your village.\n'
  '```'
)

modules_text = (
  '```fix\n'
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
  '$ip          - d08 ex00\n'
  '$iplocation  - d08 ex01 & 02\n'
  '```'
)

r_village_ids = [
  r_village1_id,
  r_village2_id,
  r_village3_id,
  r_village4_id,
  r_village5_id
]

dev_commands = [
  '$devhelp',
  '$assign',
  '$attach',
  '$devecho'
]

rps = [
  '$rock',
  '$paper',
  '$scissors'
]

rps_ans = [
  'I choose rock!',
  'I choose paper!',
  'I choose scissors!'
]

rps_win = [
'You win!',
'You won!',
'Wow, you beat me!'
]

rps_lose = [
  'You lose!',
  'You lost!',
  'Better luck next time!'
]

rps_tie = [
  'It\'s a tie!',
  'We tied!',
  'Great minds think alike!'
]