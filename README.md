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


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

