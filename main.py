import json
import tkinter as tk
from gui import AppWindow

# Load configuration file
def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        config = {
            "endpoint_x1": 0,
            "endpoint_y1": 0,
            "endpoint_x2": 0,
            "endpoint_y2": 0,
            "record_count": 3,
            "athlete_count": 5
        }
    return config

# Save configuration file
def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

def main():
    config = load_config()
    root = tk.Tk()
    root.title("简易的终点计时系统")
    app = AppWindow(root, config)
    app.pack()
    root.mainloop()
    save_config(config)

if __name__ == "__main__":
    main()