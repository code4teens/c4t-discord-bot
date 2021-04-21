# Code4Teens Discord Bot
Official Discord Bot written in Python, deployed on Replit.

## Setup
1. Remove Code4Teens Bot from previous server _(if any)_.
2. Purge Replit database _(remove previous config)_.
3. Create new Discord Server for next batch of students.
4. Setup Replit database _(initialise `prefixes` to an empty list)_.
5. Replace Guild, Role, Channel & Message IDs in `constants.py` with IDs from new server.
6. Initialise `schedule` in `constants.py` _(optional, but highly recommended)_.
7. Update `resources/` if necessary.
7. Run Replit.
8. Add Code4Teens Bot into new server.

## Commands

### Dev
```
$attach  - Sends attachment with description to specified channel.
$devecho - Sends message to specified channel.
```

### Student
```
$help    - Shows (all?) commands.
$addbot  - Adds bot to server.
$adopt   - Adopts bot into your village.
$release - Releases bot from your village.
```

### Learning Modules
```
$hello       - d03 ex04
$greet       - d03 ex05
$echo        - d04 ex01
$say         - d04 ex02
$rock        - d04 ex04
$paper       - d04 ex04
$scissors    - d04 ex04
$emoji       - d05 ex00
$embed_emoji - d05 ex01
$gif         - d05 ex02
$intro       - d05 ex03
$img         - d05 ex04
$react       - d05 ex05
$new         - d06 ex00
$list        - d06 ex01
$delete      - d06 ex02
$del_list    - d06 ex03
$currency    - d07 ex00
$job         - d07 ex01
$movie       - d07 ex02
$ip          - d08 ex00
$iplocation  - d08 ex01 & 02
```
