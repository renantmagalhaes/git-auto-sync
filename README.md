# git-auto-sync

A simple GUI tool to automatically pull and push changes from a Git repository based on a cron-style schedule.

## Features
Select Git Directory: Specify the local path of your Git directory.
SSH Key Support: Use a default or specific SSH key for your Git operations.
Cron-Style Scheduling: Set up the tool to pull and push based on a cron-style schedule.

## Installation


```
git clone https://github.com/renantmagalhaes/git-auto-sync.git
cd git-auto-sync
pip install -r requirements.txt
python main.py
```

Use the GUI to specify the Git directory, (optionally) an SSH key, and a cron-style schedule.

Click "Start Pull & Push" to begin the periodic Git operations based on your schedule.

# Headless version
## Overview
This script automates Git operations by scheduling a cron job to pull the latest changes, stage all changes, commit them with a timestamp, and then push them back to the repository. It provides an interactive interface for setting up the automation, allowing users to specify the Git directory, an optional SSH key, and a cron schedule.

## Prerequisites
1. Zenity (optional): The script uses Zenity for a GUI-based directory selection. If Zenity is not installed, the script will fall back to a command-line prompt for directory input.
2. Git: Ensure Git is installed and configured on your system.

## How to Use

```shell
./crontab-version.sh
```

If Zenity is installed, a GUI dialog will appear prompting you to select your Git directory. Otherwise, you'll be prompted in the terminal.

Input the path to your SSH key if you use one (press Enter to skip if not required).

Specify the cron schedule (e.g., * * * * * for every minute). Press Enter to default to every minute if no input is given.

The script will set up a cron job to automate the Git operations based on your input.

## Script Details
**Directory Selection:** The script first checks if Zenity is installed. If present, Zenity provides a GUI dialog for directory selection. Without Zenity, the script reverts to terminal prompts.

**SSH Key:** If an SSH key path is provided, the script uses it for Git operations. This is beneficial for repositories that require key-based authentication.

**Cron Schedule:** The user specifies how frequently the Git operations should run. If no input is given, the default is set to run every minute.

**Ensuring Environment in Cron:** The script checks the user's current crontab for specific environment settings (SHELL and PATH). If they are not present, the script adds them to ensure the cron job runs in the correct environment.

**Commit Message:** The script commits changes with a message "Auto-Commit on [current date and time]". This provides a timestamped record of each automated commit.

**Cron Job Setup:** The script constructs a one-liner bash command that will navigate to the specified Git directory, perform a pull, add all changes, commit, and then push. This command is added to the user's crontab based on the specified schedule.