# Clockwork

Discord Bot written in Python, deployed on Google Compute Engine.

## One-Off Setup

### Virtual Machine
1. On Google Compute Engine, add SSH keys (if any) under `Settings > Metadata > SSH Keys`.
2. Change default *root* password via `sudo passwd`.
3. Upate & upgrade packages via `sudo apt update`, then `sudo apt upgrade`.
4. Install necessary packages for Python development via `sudo apt install build-essential`, `sudo apt install python3-dev` & `sudo apt install python3-venv`.
5. Install *tmux* via `sudo apt install tmux`.
6. Install *git* via `sudo apt install git`.

### Repo
1. Clone repo via `git clone [remote] [dirname]`.
2. Change directory into cloned repo via `cd [dirname]`.
3. Create virtual environment via `python3 -m venv venv`.
4. Activate virtual environment via `source venv/bin/activate`.
5. Install package dependencies via `pip install -r requirements.txt`.
6. Create *tmux* session via `tmux`.
7. In a virtual environment, start Clockwork via `python main.py`.
8. Feel free to close the window.

## Need-Basis Setup

### BotCamp Server
1. Create new server from [template](https://discord.new/h7wPddF3jmGF).
2. Invite Clockwork to server.
3. Run `$setup <date>` with `date` as BotCamp Day 1 in `yyyy-mm-dd`.

### Day 3
1. Create additional *Village Roles* & *Village Channels* to accommodate *Students* (if necessary).
