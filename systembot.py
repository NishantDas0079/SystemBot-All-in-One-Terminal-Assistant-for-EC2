#!/usr/bin/env python3
# systembot.py – EC2 System Bot with Games & Dashboard
# Run: python3 systembot.py  (after installing psutil)

import curses
import curses.textpad
import psutil
import time
import random
import os
from datetime import datetime

# ====================   SYSTEM DASHBOARD   ====================
def show_dashboard(stdscr):
    """Display real-time system metrics in a dashboard."""
    curses.curs_set(0)          # Hide cursor
    stdscr.nodelay(1)            # Non‑blocking input
    stdscr.timeout(500)          # Refresh every 500 ms

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Title
        title = "📊 EC2 SYSTEM DASHBOARD 📊"
        stdscr.attron(curses.A_BOLD | curses.color_pair(3))
        stdscr.addstr(1, (w - len(title)) // 2, title)
        stdscr.attroff(curses.A_BOLD | curses.color_pair(3))

        # Collect system info
        cpu_percent = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        net = psutil.net_io_counters()
        boot_time = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        uptime_seconds = time.time() - psutil.boot_time()
        uptime = f"{int(uptime_seconds // 86400)}d {int((uptime_seconds % 86400) // 3600)}h {int((uptime_seconds % 3600) // 60)}m"

        # Layout (try/except to avoid crashes on tiny terminals)
        try:
            # CPU
            stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(3, 2, "⚡ CPU")
            stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)
            stdscr.addstr(4, 4, f"Usage: {cpu_percent}%")
            draw_bar(stdscr, 5, 4, 40, cpu_percent)

            # Memory
            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(7, 2, "💾 MEMORY")
            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
            stdscr.addstr(8, 4, f"Total: {mem.total // (1024**3)} GB")
            stdscr.addstr(9, 4, f"Used:  {mem.used // (1024**3)} GB ({mem.percent}%)")
            draw_bar(stdscr, 10, 4, 40, mem.percent)

            # Disk
            stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(12, 2, "💽 DISK (/)")
            stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
            stdscr.addstr(13, 4, f"Total: {disk.total // (1024**3)} GB")
            stdscr.addstr(14, 4, f"Used:  {disk.used // (1024**3)} GB ({disk.percent}%)")
            draw_bar(stdscr, 15, 4, 40, disk.percent)

            # Network
            stdscr.attron(curses.color_pair(5) | curses.A_BOLD)
            stdscr.addstr(3, 50, "🌐 NETWORK")
            stdscr.attroff(curses.color_pair(5) | curses.A_BOLD)
            stdscr.addstr(4, 52, f"Sent:     {net.bytes_sent // (1024**2)} MB")
            stdscr.addstr(5, 52, f"Received: {net.bytes_recv // (1024**2)} MB")
            stdscr.addstr(6, 52, f"Packets Sent: {net.packets_sent}")
            stdscr.addstr(7, 52, f"Packets Recv: {net.packets_recv}")

            # System
            stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(9, 50, "🖥️ SYSTEM")
            stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            stdscr.addstr(10, 52, f"Hostname: {os.uname().nodename}")
            stdscr.addstr(11, 52, f"OS: {os.uname().sysname} {os.uname().release}")
            stdscr.addstr(12, 52, f"Uptime: {uptime}")
            stdscr.addstr(13, 52, f"Boot: {boot_time}")

        except curses.error:
            pass   # Ignore drawing errors when terminal is too small

        # Instructions
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(h-2, 2, " Press 'q' to return to menu ")
        stdscr.attroff(curses.A_REVERSE)

        stdscr.refresh()
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break


def draw_bar(stdscr, y, x, width, percent):
    """Draw a colored progress bar."""
    fill = int(width * percent / 100)
    bar = '█' * fill + '░' * (width - fill)
    try:
        if percent < 50:
            stdscr.attron(curses.color_pair(1))   # green
        elif percent < 80:
            stdscr.attron(curses.color_pair(2))   # yellow
        else:
            stdscr.attron(curses.color_pair(4))   # red
        stdscr.addstr(y, x, bar)
        stdscr.attroff(curses.color_pair(1) | curses.color_pair(2) | curses.color_pair(4))
        stdscr.addstr(y, x + width + 2, f"{percent}%")
    except:
        pass


# ====================   SNAKE GAME (fixed)   ====================
def snake_game(stdscr):
    """Classic Snake game – no emoji, safe for all terminals."""
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Get terminal size
    h, w = stdscr.getmaxyx()
    if h < 20 or w < 60:
        stdscr.clear()
        stdscr.addstr(0, 0, "Terminal too small. Please resize to at least 20x60.")
        stdscr.refresh()
        stdscr.getch()
        return

    # Initial snake
    snake = [(10, 10), (9, 10), (8, 10)]
    direction = curses.KEY_RIGHT
    food = (random.randint(5, h-5), random.randint(5, w-5))
    score = 0
    game_over = False

    while not game_over:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Border
        stdscr.border(0)

        # Display score
        stdscr.addstr(0, 2, f"🐍 SCORE: {score} ")

        # Get user input
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Prevent snake from reversing
            if (direction == curses.KEY_UP and key != curses.KEY_DOWN) or \
               (direction == curses.KEY_DOWN and key != curses.KEY_UP) or \
               (direction == curses.KEY_LEFT and key != curses.KEY_RIGHT) or \
               (direction == curses.KEY_RIGHT and key != curses.KEY_LEFT):
                direction = key

        # Move snake head
        head = snake[0]
        if direction == curses.KEY_UP:
            new_head = (head[0] - 1, head[1])
        elif direction == curses.KEY_DOWN:
            new_head = (head[0] + 1, head[1])
        elif direction == curses.KEY_LEFT:
            new_head = (head[0], head[1] - 1)
        elif direction == curses.KEY_RIGHT:
            new_head = (head[0], head[1] + 1)

        # Check collision with walls
        if new_head[0] <= 0 or new_head[0] >= h-1 or new_head[1] <= 0 or new_head[1] >= w-1:
            game_over = True
            break

        snake.insert(0, new_head)

        # Check if food eaten
        if new_head == food:
            score += 1
            # Generate new food, avoid snake body
            while True:
                food = (random.randint(5, h-5), random.randint(5, w-5))
                if food not in snake:
                    break
        else:
            snake.pop()

        # Check collision with self
        if new_head in snake[1:]:
            game_over = True
            break

        # Draw snake
        for i, segment in enumerate(snake):
            if i == 0:
                stdscr.addch(segment[0], segment[1], 'O', curses.color_pair(2))
            else:
                stdscr.addch(segment[0], segment[1], 'o', curses.color_pair(3))

        # Draw food (simple ASCII)
        stdscr.addch(food[0], food[1], '@', curses.color_pair(4))

        stdscr.refresh()

    # Game over screen
    stdscr.clear()
    stdscr.nodelay(0)
    h, w = stdscr.getmaxyx()
    msg = "GAME OVER!"
    stdscr.addstr(h//2 - 1, (w - len(msg)) // 2, msg, curses.A_BOLD | curses.color_pair(4))
    msg = f"Your Score: {score}"
    stdscr.addstr(h//2, (w - len(msg)) // 2, msg)
    msg = "Press any key to continue"
    stdscr.addstr(h//2 + 2, (w - len(msg)) // 2, msg)
    stdscr.refresh()
    stdscr.getch()


# ====================   TIC-TAC-TOE (fixed)   ====================
def tictactoe_game(stdscr):
    """Tic‑Tac‑Toe vs computer (simple AI)."""
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(0)

    board = [' '] * 9
    player = 'X'
    computer = 'O'
    game_over = False
    winner = None

    def draw_board():
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        title = "❌ TIC TAC TOE ⭕ (You: X, Computer: O)"
        stdscr.addstr(1, (w - len(title)) // 2, title, curses.A_BOLD)

        # Board lines
        start_y = 4
        start_x = (w - 9) // 2
        for i in range(3):
            for j in range(3):
                y = start_y + i * 2
                x = start_x + j * 4
                stdscr.addstr(y, x, f" {board[i*3 + j]} ")
            if i < 2:
                stdscr.addstr(start_y + i*2 + 1, start_x, "-----------")

        # Status message
        if game_over:
            if winner == 'X':
                msg = "🎉 YOU WIN! 🎉"
            elif winner == 'O':
                msg = "💻 COMPUTER WINS! 💻"
            else:
                msg = "🤝 IT'S A DRAW! 🤝"
        else:
            msg = f"Your turn ({player}) – use number keys 1-9"
        stdscr.addstr(12, (w - len(msg)) // 2, msg)
        stdscr.refresh()

    def check_win(board):
        """Return winner ('X' or 'O') or 'draw' or None."""
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for i1, i2, i3 in wins:
            if board[i1] == board[i2] == board[i3] != ' ':
                return board[i1]
        if ' ' not in board:
            return 'draw'
        return None

    def computer_move():
        # Try to win
        for i in range(9):
            if board[i] == ' ':
                board[i] = computer
                if check_win(board) == computer:
                    return
                board[i] = ' '
        # Block player win
        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                if check_win(board) == player:
                    board[i] = computer
                    return
                board[i] = ' '
        # Random move
        empty = [i for i, v in enumerate(board) if v == ' ']
        if empty:
            board[random.choice(empty)] = computer

    while not game_over:
        draw_board()
        # Player move
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break
        if ord('1') <= key <= ord('9'):
            pos = key - ord('1')
            if board[pos] == ' ':
                board[pos] = player
                # Check win/draw
                result = check_win(board)
                if result:
                    game_over = True
                    winner = result if result != 'draw' else None
                    break
                # Computer move
                computer_move()
                result = check_win(board)
                if result:
                    game_over = True
                    winner = result if result != 'draw' else None
                    break

    draw_board()
    stdscr.getch()


# ====================   MAIN MENU   ====================
def main_menu(stdscr):
    """Display the main menu and handle navigation."""
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    current_row = 0
    menu_items = [
        ("🐍 Play Snake", snake_game),
        ("❌⭕ Play Tic-Tac-Toe", tictactoe_game),
        ("📊 System Dashboard", show_dashboard),
        ("🚪 Exit", None)
    ]

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # ASCII Art Logo
        logo = [
            "███████╗██╗   ██╗███████╗████████╗███████╗███╗   ██╗██████╗  ██████╗ ████████╗",
            "██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗  ██║██╔══██╗██╔═══██╗╚══██╔══╝",
            "███████╗ ╚████╔╝ █████╗     ██║   █████╗  ██╔██╗ ██║██║  ██║██║   ██║   ██║   ",
            "╚════██║  ╚██╔╝  ██╔══╝     ██║   ██╔══╝  ██║╚██╗██║██║  ██║██║   ██║   ██║   ",
            "███████║   ██║   ███████╗   ██║   ███████╗██║ ╚████║██████╔╝╚██████╔╝   ██║   ",
            "╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚═════╝  ╚═════╝    ╚═╝   "
        ]

        # Display logo centered
        start_y = 2
        for i, line in enumerate(logo):
            try:
                stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                stdscr.addstr(start_y + i, (w - len(line)) // 2, line[:w-1])
                stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
            except:
                pass

        # Menu box
        box_y = start_y + len(logo) + 2
        box_width = 40
        box_x = (w - box_width) // 2

        # Draw box border
        stdscr.attron(curses.color_pair(5))
        for i in range(box_width):
            stdscr.addch(box_y, box_x + i, curses.ACS_HLINE)
            stdscr.addch(box_y + len(menu_items) + 3, box_x + i, curses.ACS_HLINE)
        for i in range(len(menu_items) + 4):
            stdscr.addch(box_y + i, box_x, curses.ACS_VLINE)
            stdscr.addch(box_y + i, box_x + box_width - 1, curses.ACS_VLINE)
        stdscr.addch(box_y, box_x, curses.ACS_ULCORNER)
        stdscr.addch(box_y, box_x + box_width - 1, curses.ACS_URCORNER)
        stdscr.addch(box_y + len(menu_items) + 3, box_x, curses.ACS_LLCORNER)
        stdscr.addch(box_y + len(menu_items) + 3, box_x + box_width - 1, curses.ACS_LRCORNER)
        stdscr.attroff(curses.color_pair(5))

        # Title inside box
        stdscr.attron(curses.A_BOLD | curses.color_pair(2))
        stdscr.addstr(box_y + 1, box_x + 2, "🤖 SYSTEMBOT - MAIN MENU")
        stdscr.attroff(curses.A_BOLD | curses.color_pair(2))

        # Menu items
        for idx, (item, _) in enumerate(menu_items):
            y = box_y + 3 + idx
            x = box_x + 4
            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, x, f"> {item} <")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, f"  {item}  ")

        # Instructions
        instr_y = box_y + len(menu_items) + 5
        stdscr.addstr(instr_y, box_x + 2, "↑/↓ or 1-4 to navigate, Enter to select")
        stdscr.addstr(instr_y + 1, box_x + 2, "Press 'q' in any screen to return here")

        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_row = (current_row - 1) % len(menu_items)
        elif key == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(menu_items)
        elif key == ord('1'):
            current_row = 0
        elif key == ord('2'):
            current_row = 1
        elif key == ord('3'):
            current_row = 2
        elif key == ord('4'):
            current_row = 3
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == len(menu_items) - 1:   # Exit
                break
            else:
                # Clear screen and run the selected function
                stdscr.clear()
                stdscr.refresh()
                menu_items[current_row][1](stdscr)

        elif key == ord('q') or key == ord('Q'):
            break


def main():
    """Entry point for the application."""
    curses.wrapper(main_menu)


if __name__ == "__main__":
    main()
