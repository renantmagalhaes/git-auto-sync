#!/bin/bash

# Check if zenity is installed
if command -v zenity &> /dev/null; then
    # Use zenity to select a directory
    git_directory=$(zenity --file-selection --directory)
    # Check if user canceled the dialog or if the selection is empty
    if [ $? -ne 0 ] || [ -z "$git_directory" ]; then
        echo "Directory selection canceled or invalid. Exiting."
        exit 1
    fi
else
    # Fallback to manual input
    read -p "Zenity not found. Manually enter the path to your Git directory: " git_directory
fi

read -p "Enter the path to your SSH key (press Enter to skip): " ssh_key
read -p "Enter the cron schedule (e.g., '* * * * *' for every minute, press Enter to default to every minute): " cron_schedule

# If cron_schedule is empty, set it to default '* * * * *'
if [ -z "$cron_schedule" ]; then
    cron_schedule='* * * * *'
fi

# Construct the one-liner command with an inline function
if [ ! -z "$ssh_key" ]; then
    cmd="bash -c 'f() { cd $git_directory && GIT_SSH_COMMAND=\"ssh -i $ssh_key\" git pull && GIT_SSH_COMMAND=\"ssh -i $ssh_key\" git add . && GIT_SSH_COMMAND=\"ssh -i $ssh_key\" git commit -m \"Auto-Commit on \$(date)\" && GIT_SSH_COMMAND=\"ssh -i $ssh_key\" git push; }; f'"
else
    cmd="bash -c 'f() { cd $git_directory && git pull && git add . && git commit -m \"Auto-Commit on \$(date)\" && git push; }; f'"
fi

# Check the current crontab for the specified lines
current_cron=$(crontab -l 2>/dev/null)
shell_line_exists=$(echo "$current_cron" | grep -Fx "SHELL=/bin/sh")
path_line_exists=$(echo "$current_cron" | grep -Fx "PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin")

# If the lines don't exist, prepend them
if [ -z "$shell_line_exists" ]; then
    current_cron="SHELL=/bin/sh\n$current_cron"
fi

if [ -z "$path_line_exists" ]; then
    current_cron="PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n$current_cron"
fi

# Check and replace if the same directory exists in the current crontab
current_cron=$(echo -e "$current_cron" | grep -v "$git_directory")

# Update the crontab with the new entry
echo -e "$current_cron\n$cron_schedule $cmd" | crontab -

echo "Scheduled git pull & push for directory $git_directory with the cron schedule $cron_schedule."
