#!/usr/bin/env python3
import asyncio
import sys
import os
import time
import math
import random
from colorama import Fore, Style, init

init(autoreset=True)

from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn

console = Console(highlight=False)

C_BLOOD   = "#500000"
C_RED     = "#FF0000"
C_NEON    = "#FF0000"
C_WHITE   = "#FFFFFF"
C_SILVER  = "#CCCCCC"

_RAIN = list("01▓▒░│┤╣║╗╝┐└┴┬├─┼╚╔╩╦╠═╬┘┌MRMCSOCIETY")

def cls():
    os.system("cls" if os.name == "nt" else "clear")

def set_title():
    if os.name == "nt":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("BREACH-PROTOCOL V3.0 | MR_MCSOCIETY")

def _rain_frame(w, h, t):
    f = Text()
    for row in range(h):
        for col in range(w):
            spd = 1.0 + (col % 7) * 0.3
            ph  = int((t * spd * 12 + col * 3.7)) % len(_RAIN)
            ch  = _RAIN[(col * 17 + row * 3 + ph) % len(_RAIN)]
            r   = int(0x18 + abs(math.sin(col * 0.4 + t * 0.8)) * (0x99 - 0x18))
            f.append(ch, style=f"#{r:02X}0000")
        if row < h - 1: f.append("\n")
    return f

def play_intro():
    t0 = time.monotonic()
    with Live(console=console, screen=True, refresh_per_second=24, transient=True) as live:
        while time.monotonic() - t0 < 1.0:
            live.update(_rain_frame(100, 25, time.monotonic() - t0))
            time.sleep(1 / 24)

def boot_sequence():
    tasks = [
        ("SYNCING KERNEL", 0.1), 
        ("LOADING MODULES", 0.2), 
        ("ESTABLISHING LINK", 0.1)
    ]
    with Progress(
        SpinnerColumn(style=f"{C_NEON} bold"),
        TextColumn(f"[{C_SILVER}]{{task.description:<20}}"),
        BarColumn(bar_width=35, style=C_BLOOD, complete_style=C_NEON),
        console=console, transient=True
    ) as progress:
        for label, dur in tasks:
            jid = progress.add_task(label, total=100)
            while not progress.tasks[jid].finished:
                progress.advance(jid, random.uniform(5, 15))
                time.sleep(dur / 5)

def banner():
    cls()
    print(Fore.RED + r"""
  ███▄ ▄███▓ ██▀███   ███▄ ▄███▓  ▄████▄    ██████  ▒█████   ▄████▄   ██▓ ▓█████ ▄▄▄█████▓ ▓██   ██▓
 ▓██▒▀█▀ ██▒▓██ ▒ ██▒▓██▒▀█▀ ██▒ ▒██▀ ▀█   ▒██    ▒ ▒██▒  ██▒▒██▀ ▀█  ▓██▒▓█   ▀ ▓  ██▒ ▓▒ ▒██  ██▒
 ▓██    ▓██░▓██ ░▄█ ▒▓██    ▓██░ ▒▓█    ▄  ░ ▓██▄   ▒██░  ██▒▒▓█    ▄  ▒██▒▒███   ▒ ▓██░ ▒░  ▒██ ██░
 ▒██    ▒██ ▒██▀▀█▄  ▒██    ▒██  ▒▓▓▄ ▄██▒   ▒   ██▒▒██   ██░▒▓▓▄ ▄██▒ ░██░▒▓█  ▄ ░ ▓██▓ ░   ░ ▐██▓░
 ▒██▒   ░██▒░██▓ ▒██▒▒██▒   ░██▒ ▒ ▓███▀ ░ ▒██████ ▒░ ████▓▒░▒ ▓███▀ ░ ░██░░▒████▒  ▒██▒ ░   ░ ██▒▓░
 ░ ▒░   ░  ░░ ▒▓ ░▒▓░░ ▒░   ░  ░ ░ ░▒ ▒  ░ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ░▒ ▒  ░ ░▓  ░░ ▒░ ░  ▒ ░░       ██▒▒▒
 ░  ░      ░  ░▒ ░ ▒░░  ░      ░   ░ ▒     ░ ░▒  ░ ░  ░ ▒ ▒░   ░  ▒     ▒ ░ ░ ░  ░    ░      ▓██ ░▒░
 ░      ░     ░░   ░ ░      ░    ░           ░  ░ ░ ░ ░ ░ ▒   ░           ▒ ░   ░      ░      ▒ ▒ ░░
        ░      ░            ░    ░ ░                 ░ ░   ░ ░                 ░  ░         ░ ░
────────────────────────────────────────────────────────────────────────────────────────────────────
 ʙʀᴇᴀᴄʜ-ᴘʀᴏᴛᴏᴄᴏʟ ᴠ3.0 | ᴅᴇᴠ: ᴍʀ_ᴍᴄꜱᴏᴄɪᴇᴛʏ | ᴀᴜᴛʜ: ᴍʀ_ᴍᴄꜱᴏᴄɪᴇᴛʏ | ᴋᴇʀɴᴇʟ: ᴜɴɪᴠᴇʀꜱᴀʟ ꜱʏɴᴄ
────────────────────────────────────────────────────────────────────────────────────────────────────""")

async def main_menu():
    banner()
    print(Fore.RED + """
                                << Tokens Category >>

  >> Multi Token Raiding         >> Single Token Nuking         >> Account Nuking                >> Tools
  1. Spam in one channel         8.  Webhook Spam Channels      15. Remove all friends           22. Check Token
  2. Spam in all channels        9.  Mass Create Roles          16. Block all friends            23. Check Tokens
  3. Add Reaction to Message     10. Mass Create channels       17. Leave all servers            24. Get Guild info
  4. Join to a server            11. Delete all channels        18. Cycle Token Settings         25. Get Token Info
  5. Leave a server              12. Delete all roles           19. Mass dm                      26. Get Tokens Info
  6. Change Nickname             13. Remove all Emojis          20. Close all Dms                27. Back to Main Menu
  7. Change Status               14. Change server icon         21. Delete all personal guilds   28. Exit
""")
    
    choice = input(Fore.RED + "\n  mcsociety@breach >> " + Style.RESET_ALL).strip()
    
    if choice in ["1", "2", "3", "4", "5", "6", "7"]:
        import MultiTokenRaiding
        await MultiTokenRaiding.main()
    
    elif choice in ["8", "9", "10", "11", "12", "13", "14"]:
        import SingleTokenNuking
        await SingleTokenNuking.main()
    
    elif choice in ["15", "16", "17", "18", "19", "20", "21"]:
        import AccountNuking
        await AccountNuking.main()
    
    elif choice in ["22", "23", "24", "25", "26"]:
        import Tools
        result = await Tools.main()
        if result == "back":
            await main_menu()
    
    elif choice == "27":
        await main_menu()
    
    elif choice == "28":
        print(Fore.RED + "\n[!] Termination Signal Received. Shutting down...")
        sys.exit(0)
    else:
        print(Fore.RED + " [!] Command Invalid.")
        await asyncio.sleep(1)
        await main_menu()

async def entry():
    set_title()
    play_intro()
    boot_sequence()
    await main_menu()

if __name__ == "__main__":
    try:
        asyncio.run(entry())
    except KeyboardInterrupt:
        sys.exit(0)