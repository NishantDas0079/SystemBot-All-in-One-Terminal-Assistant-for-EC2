# SystemBot – Terminal Games & System Monitor for EC2

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SystemBot** is an interactive terminal application that runs directly on your AWS EC2 instance (or any Linux server). It combines classic games with a real‑time system dashboard – all inside your SSH session!

---

## ✨ Features

- 🐍 **Classic Snake Game** – eat food (`@`), grow, avoid walls and yourself.
- ❌⭕ **Tic‑Tac‑Toe** – play against a simple AI.
- 📊 **Live System Dashboard** – monitor CPU, memory, disk, network, and system info in real time.
- 🎨 **Attractive Curses Interface** – colours, progress bars, and a retro ASCII logo.
- 🚀 **Lightweight** – uses only `psutil` (curses is built‑in).
- 🔧 **No Internet Required** – runs entirely in your terminal.

---

## 🛠️ Prerequisites

- An **AWS EC2 instance** (or any Linux machine) with Python 3.8+.
- SSH access (PuTTY or terminal).
- Basic familiarity with the command line.

---

## 📦 Installation

1. **Connect to your EC2 instance** via SSH.

2. **Update system packages** (optional but recommended):
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
3. Install Python and pip (if not already present):
```bash
sudo apt install python3 python3-pip python3-venv -y
```
4. Create and activate a virtual environment (optional but good practice):
```bash
python3 -m venv venv
source venv/bin/activate
```
5. Install dependencies
```bash
pip install -r requirements.txt
```
6. How to execute?
```bash
python3 systembot.py
```

# 🎮 Gameplay & Dashboard
# 🐍 Snake Game
Control with arrow keys.

Eat the @ symbol to grow and increase your score.

Game ends if you hit the wall or yourself.

# ❌⭕ Tic‑Tac‑Toe
You are X, the computer is O.

Press the number corresponding to the cell you want to play (1 = top‑left, 9 = bottom‑right).

The computer uses a simple AI (win → block → random).

# 📊 System Dashboard
Real‑time graphs for CPU, memory, and disk usage.

Network traffic and system info (hostname, OS, uptime, boot time).

Updates automatically every 0.5 seconds.

