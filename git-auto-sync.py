import tkinter as tk
from tkinter import filedialog
import subprocess
from datetime import datetime
from croniter import croniter

# GUI functions
def select_git_directory():
    folder_selected = filedialog.askdirectory()
    git_path_var.set(folder_selected)

def select_ssh_key_file():
    file_selected = filedialog.askopenfilename()
    ssh_key_var.set(file_selected)

# Git functions
def git_pull_and_push(directory, ssh_key=None):
    env = None
    if ssh_key:
        env = {"GIT_SSH_COMMAND": f"ssh -i {ssh_key}"}

    # Generate a commit message with the current date and time
    commit_message = f"Auto-commit on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    try:
        subprocess.check_call(['git', '-C', directory, 'pull'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        
        # Add all changes to staging
        subprocess.check_call(['git', '-C', directory, 'add', '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        
        # Commit the changes
        subprocess.check_call(['git', '-C', directory, 'commit', '-m', commit_message], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

        subprocess.check_call(['git', '-C', directory, 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    except subprocess.CalledProcessError:
        # Handle exceptions (e.g., Git not installed, no internet, etc.)
        pass

# Cron functions
def get_next_runtime(cron_schedule):
    now = datetime.now()
    iter = croniter(cron_schedule, now)
    next_date = iter.get_next(datetime)
    return (next_date - now).total_seconds() * 1000  # Return milliseconds until next run

scheduled_task = None  # To store the identifier of the scheduled task

def start_periodic_pull_and_push():
    global scheduled_task
    git_pull_and_push(git_path_var.get(), ssh_key=ssh_key_var.get())
    next_run_time = get_next_runtime(cron_schedule_var.get())
    scheduled_task = app.after(int(next_run_time), start_periodic_pull_and_push)

def stop_sync():
    global scheduled_task
    if scheduled_task:
        app.after_cancel(scheduled_task)
        scheduled_task = None

# GUI setup
app = tk.Tk()
app.title("Git Auto Pull & Push")

git_path_var = tk.StringVar()
ssh_key_var = tk.StringVar()
cron_schedule_var = tk.StringVar(value="* * * * *")  # Default value set to every minute

tk.Label(app, text="Git Directory:").pack(pady=10)
tk.Entry(app, textvariable=git_path_var, width=50).pack(pady=10)
tk.Button(app, text="Browse", command=select_git_directory).pack(pady=10)

tk.Label(app, text="SSH Key (Optional - will fallback to default if empty):").pack(pady=10)
tk.Entry(app, textvariable=ssh_key_var, width=50).pack(pady=10)
tk.Button(app, text="Browse", command=select_ssh_key_file).pack(pady=10)

tk.Label(app, text="Schedule (Cron format - Default is every minute):").pack(pady=10)
tk.Entry(app, textvariable=cron_schedule_var, width=50).pack(pady=10)

tk.Button(app, text="Start Pull & Push", command=start_periodic_pull_and_push).pack(pady=10)
tk.Button(app, text="Stop Sync", command=stop_sync).pack(pady=10)

app.mainloop()
