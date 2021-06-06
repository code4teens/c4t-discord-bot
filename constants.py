import os

from functions import core
import utilities as u

token = os.getenv('TOKEN')
guild_id = 851007012816945153
cat_bot_id = 851007013625790484
c_dev_terminal_id = 851007012829134862
c_dev_log_id = 851007012829134863
c_imp_alerts_id = 851007013269012503
c_imp_coc_id = 851007013269012505
c_imp_townhall_id = 851007013269012506
c_stu_chit_chat_id = 851007013269012508
c_bot_clockwork_id = 851007013625790485
m_coc_id = 851012232502444062
r_devs_id = 851007012829134858
r_dev_bot_id = 851007012816945162
r_bocals_id = 851007012816945161
r_students_id = 851007012816945160
r_student_bots_id = 851007012816945159
r_village1_id = 851007012816945158
r_village2_id = 851007012816945157
r_village3_id = 851007012816945156
r_village4_id = 851007012816945155
r_village5_id = 851007012816945154

u_dev_bot_id = 826063626682368031
u_bohchu_id = 808949871281176596
u_bunyod_id = 237063450646282241
u_hans_id = 160369095965933568
u_prag_id = 266934788420534272
u_yilin_id = 801811150320828427
u_jeff_id = 800981368825315329
u_lynn_id = 257887843139977216
u_thila_id = 801602510778662922
u_tzeryee_id = 808223777073790986
p_add_student_bot_int = 257088

#\U0001F197
ok_emoji = '🆗'

#\U00002705
tick_emoji = '✅'

#\U0000274C
cross_emoji = '❌'

daily_evaluation_form = 'https://forms.gle/68X2jz4CvivBAtYPA'
attach_regex = '\$attach <#[0-9]{18}> .+'
devecho_regex = '\$devecho <#[0-9]{18}> .+'
addbot_regex = '\$addbot https://discord.com/api/oauth2/authorize\?client_id=([0-9]{18})&permissions=([0-9]+)&scope=bot'

dev_help_text = (
  '```fix\n'
  '$devhelp - Shows this menu.\n'
  '$attach  - Sends attachment with description to specified channel.\n'
  '$devecho - Sends message to specified channel.\n'
  '```'
)

help_text = (
  '```fix\n'
  '$help         - Shows this menu.\n'
  '$addbot       - Adds bot to server.\n'
  '$hello        - d03 ex04\n'
  '$greet        - d03 ex05\n'
  '$echo         - d04 ex01\n'
  '$say          - d04 ex02\n'
  '$rock         - d04 ex04\n'
  '$paper        - d04 ex04\n'
  '$scissors     - d04 ex04\n'
  '$emoji        - d05 ex01\n'
  '$embed_emoji  - d05 ex02\n'
  '$gif          - d05 ex03\n'
  '$intro        - d05 ex04\n'
  '$img          - d05 ex05\n'
  '$react        - d05 ex06\n'
  '$new          - d06 ex01\n'
  '$list         - d06 ex02\n'
  '$delete       - d06 ex03\n'
  '$del_list     - d06 ex04\n'
  '$scrape       - d07 ex01\n'
  '$currency     - d07 ex02\n'
  '$job          - d07 ex03\n'
  '$movie        - d07 ex04\n'
  '$ip           - d08 ex01\n'
  '$iplocation   - d08 ex02\n'
  '$iplocation_2 - d08 ex03\n'
  '```'
)

u_non_student_ids = [
  u_bohchu_id,
  u_bunyod_id,
  u_hans_id,
  u_prag_id,
  u_yilin_id,
  u_jeff_id,
  u_lynn_id,
  u_thila_id,
  u_tzeryee_id
]

r_village_ids = [
  r_village1_id,
  r_village2_id,
  r_village3_id,
  r_village4_id,
  r_village5_id
]

dev_commands = [
  '$devhelp',
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
  ":ghost:",
  "<:kawaii_pikachu:833590617632276531>"
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

schedule = {
  #Day 1
  '2021-06-09': [
    {'time': '08:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'Good Morning <@&{r_students_id}>, this is a reminder to join our very first Townhall Session, 9:00 am later at <#{c_imp_townhall_id}>.'},
    {'time': '10:00', 'type': u.Alert.FILE, 'payload': 'resources/day1.txt', 'message': f'<@&{r_students_id}>, this is your Day01 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'}
  ],
  #Day 2
  '2021-06-10': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day2.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day02 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'},
    {'time': '18:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, this is a reminder to join our second Townhall Session, 7:00 pm later at <#{c_imp_townhall_id}>.'}
  ],
  #Day 3
  '2021-06-11': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day3.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day03 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'}

  ],
  #Day 4
  '2021-06-12': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day4.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day04 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'},
    {'time': '18:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, this is a reminder to join our third Townhall Session, 7:00 pm later at <#{c_imp_townhall_id}>.'}
  ],
  #Day 5
  '2021-06-13': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day5.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day05 assignment.'},
    {'time': '09:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_villages, 'message': None},
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day9.txt', 'message': f'Additionally, you are now put into groups for this assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'}
  ],
  #Day 6
  '2021-06-14': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day6.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day06 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'}
  ],
  #Day 7
  '2021-06-15': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day7.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day07 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'}
  ],
  #Day 8
  '2021-06-16': [
    {'time': '09:00', 'type': u.Alert.FILE, 'payload': 'resources/day8.txt', 'message': f'Good Morning <@&{r_students_id}>, this is your Day08 assignment. All the best!'},
    {'time': '12:00', 'type': u.Alert.COROUTINE, 'payload': core.assign_peers, 'message': None},
    {'time': '12:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, upon conducting your evaluations, kindly submit below form before 10:00 pm tonight. Both the evaluator AND evaluatee must fill out the form.\n\n{daily_evaluation_form}'},
    # move to another day
    {'time': '19:00', 'type': u.Alert.FILE, 'payload': 'resources/day9.txt', 'message': f'<@&{r_students_id}>, this is your Day09 assignment. All the best!'}
  ],
  #Day 9
  '2021-06-17': [
    {'time': '16:00', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'Good Evening <@&{r_students_id}>, this is a reminder that your final evaluation will begin at 5:00 pm. The <@{r_devs_id}> will be contacting you shortly.'},
    {'time': '18:30', 'type': u.Alert.MESSAGE, 'payload': None, 'message': f'<@&{r_students_id}>, this is a reminder to join our very last Townhall Session, 7:00 pm later at <#{c_imp_townhall_id}>.'}
  ]
}