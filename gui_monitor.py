import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading


# -------------------- FUNCTIONS --------------------

def browse_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)


def start_monitoring():
    path = folder_path.get()

    if not path:
        messagebox.showerror("Error", "Please select a folder")
        return

    output_box.insert(tk.END, "Monitoring started...\n")

    # Run monitoring in separate thread
    threading.Thread(target=run_script, daemon=True).start()


def run_script():
    path = folder_path.get()

    try:
        process = subprocess.Popen(
            ["python", "-u", "file_integrity_monitor_system.py", path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        for line in process.stdout:
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------- GUI SETUP --------------------

root = tk.Tk()
root.title("File Integrity Monitor")
root.geometry("600x400")

folder_path = tk.StringVar()

tk.Label(root, text="Select Folder to Monitor:").pack(pady=5)
tk.Entry(root, textvariable=folder_path, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=browse_folder).pack(pady=5)

tk.Button(root, text="Start Monitoring", command=start_monitoring).pack(pady=10)

output_box = tk.Text(root, height=15, width=70)
output_box.pack(pady=5)

root.mainloop()
