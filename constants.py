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

emojis = [
  ":teddy_bear:",
  ":heart_eyes:",
  ":clap:",
  ":pleading_face:",
  ":smiling_face_with_3_hearts:",
  ":woman_facepalming:",
  ":laughing:",
  ":smirk:",
  ":eyes:",
  ":woozy_face:",
  ":exploding_head:",
  ":neutral_face:",
  ":partying_face:",
  ":money_mouth:",
  ":ghost:"
]

gifs = [
  'https://media1.tenor.com/images/861409ba9b00e46a67f4f7be00cee2f7/tenor.gif?itemid=16992959',
  'https://media1.tenor.com/images/a7ae94274d1bc120b1a59382ef5ac66b/tenor.gif?itemid=13418523',
  'https://media1.tenor.com/images/24ac13447f9409d41c1aecb923aedf81/tenor.gif?itemid=5026057',
  'https://media1.tenor.com/images/f6f02f22f3da8a85d8f600a947144b6d/tenor.gif?itemid=17202817',
  'https://media1.tenor.com/images/0796f5445e9730634315351c86d00e99/tenor.gif?itemid=15323902',
  'https://media1.tenor.com/images/ed628307910258f8d23796b7029faa19/tenor.gif?itemid=12251780',
  'https://media1.tenor.com/images/1c7bc370dc6ac84cc79660eba1f4f2c7/tenor.gif?itemid=15443300',
  'https://media1.tenor.com/images/119dd3797490c22e49cf42e5357fb719/tenor.gif?itemid=4869672',
  'https://media1.tenor.com/images/5a85818cb17039f20e3c31ba87005b72/tenor.gif?itemid=17640265',
  'https://media1.tenor.com/images/d3dac1b007907d196e3235d7fe251efe/tenor.gif?itemid=16999811',
  'https://media1.tenor.com/images/58de9f3c43b92e5f4cacc57714fd9fa5/tenor.gif?itemid=16216173'
]