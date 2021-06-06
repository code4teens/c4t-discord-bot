# Code4Teens Discord Bot
Official Discord Bot written in Python, deployed on Replit.

## Setup
1. Remove Code4Teens Bot from previous server _(if any)_.
2. Purge Replit database _(remove previous config)_.
3. Create new Discord Server for next batch of students.
4. Add Admins & Code4Teens Bot to corresponding roles.
5. Setup Replit database _(initialise `code` to 0)_.
6. Replace Guild, Role, Channel & Message IDs in `constants.py` with IDs from new server.
7. Initialise `schedule` in `constants.py` _(optional, but highly recommended)_.
8. Update `resources/` if necessary.
9. Run Replit.
10. Add Code4Teens Bot into new server.

## Commands

### Dev
```
$devhelp - Shows this menu.
$attach  - Sends attachment with description to specified channel.
$devecho - Sends message to specified channel.
```

### Student
```
$help         - Shows this menu.
$addbot       - Adds bot to server.
$hello        - d03 ex04
$greet        - d03 ex05
$echo         - d04 ex01
$say          - d04 ex02
$rock         - d04 ex04
$paper        - d04 ex04
$scissors     - d04 ex04
$emoji        - d05 ex01
$embed_emoji  - d05 ex02
$gif          - d05 ex03
$intro        - d05 ex04
$img          - d05 ex05
$react        - d05 ex06
$new          - d06 ex01
$list         - d06 ex02
$delete       - d06 ex03
$del_list     - d06 ex04
$scrape       - d07 ex01
$currency     - d07 ex02
$job          - d07 ex03
$movie        - d07 ex04
$ip           - d08 ex01
$iplocation   - d08 ex02
$iplocation_2 - d08 ex03
```
