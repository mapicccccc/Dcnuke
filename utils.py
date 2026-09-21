import aiohttp
import asyncio
import json
import random
import string
from colorama import Fore, Style, init

init(autoreset=True)

class DiscordAPI:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT25; Win64; x64) AppleWebKit/537.36'
        }
    
    async def request(self, method, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=self.headers, **kwargs) as resp:
                return resp.status, await resp.json() if resp.content_type == 'application/json' else await resp.text()

class TokenValidator:
    @staticmethod
    async def validate(token):
        api = DiscordAPI(token)
        status, data = await api.request('GET', 'https://discord.com/api/v9/users/@me')
        return status == 200, data if status == 200 else None

class Logger:
    @staticmethod
    def success(msg):
        print(f"{Fore.GREEN}[+] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def error(msg):
        print(f"{Fore.RED}[-] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def info(msg):
        print(f"{Fore.CYAN}[*] {msg}{Style.RESET_ALL}")
    
    @staticmethod
    def warning(msg):
        print(f"{Fore.YELLOW}[!] {msg}{Style.RESET_ALL}")

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
