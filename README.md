# Clockwork

Official Discord Bot written in Python, deployed on Google Compute Engine.

## Setup

### Virtual Machine
1. On Google Compute Engine, add SSH keys under `Settings > Metadata > SSH Keys`.
2. Change default *root* password via `sudo passwd`.
3. Upate & upgrade packages via `sudo apt update`, then `sudo apt upgrade`.
4. Install necessary packages for Python development via `sudo apt install build-essential`, `sudo apt install python3-dev` & `sudo apt install python3-venv`.
5. Install *git* via `sudo apt install git`.

### Repo
1. Clone repo via `git clone [remote] [dirname]`.
2. Change directory into cloned repo via `cd [dirname]`.
2. Create virtual environment via `python3 -m venv venv`.
3. Activate virtual environment via `source venv/bin/activate`.
2. Install package dependencies via `pip install -r requirements.txt`.

### BotCamp Server
1. In a virtual environment, start Clockwork via `python main.py`.
2. 
