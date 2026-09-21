import asyncio
import aiohttp
import random
from utils import DiscordAPI, Logger, generate_random_string

class MultiTokenRaider:
    def __init__(self, tokens):
        self.tokens = tokens
        self.apis = [DiscordAPI(token) for token in tokens]
    
    async def spam_channel(self, channel_id, message, amount=100):
        Logger.info(f"Starting spam attack on channel {channel_id}")
        tasks = []
        for api in self.apis:
            for _ in range(amount // len(self.apis)):
                tasks.append(api.request('POST', f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                                        json={'content': message}))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success = sum(1 for r in results if isinstance(r, tuple) and r[0] == 200)
        Logger.success(f"Sent {success} messages to channel {channel_id}")
    
    async def spam_all_channels(self, guild_id, message, amount=50):
        Logger.info(f"Fetching channels in guild {guild_id}")
        channels = []
        for api in self.apis:
            status, data = await api.request('GET', f'https://discord.com/api/v9/guilds/{guild_id}/channels')
            if status == 200:
                channels.extend([ch['id'] for ch in data if ch['type'] == 0])
        
        channels = list(set(channels))
        Logger.info(f"Found {len(channels)} text channels")
        
        for channel_id in channels:
            await self.spam_channel(channel_id, message, amount=amount//len(channels))
    
    async def add_reaction(self, channel_id, message_id, emoji):
        Logger.info(f"Adding reaction to message {message_id}")
        tasks = []
        for api in self.apis:
            encoded_emoji = emoji.encode('utf-8').hex() if len(emoji) > quarterly else emoji
            tasks.append(api.request('PUT', 
                f'https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me'))
        
        await asyncio.gather(*tasks)
        Logger.success("Reactions added")
    
    async def join_server(self, invite_code):
        Logger.info(f"Joining server with invite {invite_code}")
        tasks = []
        for api in self.apis:
            tasks.append(api.request('POST', f'https://discord.com/api/v9/invites/{invite_code}'))
        
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r[0] == 200)
        Logger.success(f"{success} accounts joined the server")
    
    async def leave_server(self, guild_id):
        Logger.info(f"Leaving server {guild_id}")
        tasks = []
        for api in self.apis:
            tasks.append(api.request('DELETE', f'https://discord.com/api/v9/users/@me/guilds/{guild_id}'))
        
        await asyncio.gather(*tasks)
        Logger.success("All accounts left the server")
    
    async def change_nickname(self, guild_id, nickname):
        Logger.info(f"Changing nickname in {guild_id}")
        tasks = []
        for api in self.apis:
            tasks.append(api.request('PATCH', f'https://discord.com/api/v9/guilds/{guild_id}/members/@me',
                                    json={'nick': nickname}))
        
        await asyncio.gather(*tasks)
        Logger.success("Nicknames changed")
    
    async def change_status(self, status_type="online", custom_status="Mr_McSociety"):
        Logger.info("Changing status for all accounts")
        tasks = []
        status_payload = {
            "status": status_type,
            "activities": [{
                "name": "Custom Status",
                "type": 4,
                "state": custom_status
            }]
        }
        
        for api in self.apis:
            tasks.append(api.request('PATCH', 'https://discord.com/api/v9/users/@me/settings',
                                    json=status_payload))
        
        await asyncio.gather(*tasks)
        Logger.success("Statuses updated")

async def main():
    tokens = input("Enter tokens (comma separated): ").split(',')
    raider = MultiTokenRaider(tokens)
    
    print("\n1. Spam in one channel")
    print("2. Spam in all channels")
    print("3. Add Reaction")
    print("4. Join Server")
    print("5. Leave Server")
    print("6. Change Nickname")
    print("7. Change Status")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        channel = input("Channel ID: ")
        message = input("Message: ")
        amount = int(input("Amount: "))
        await raider.spam_channel(channel, message, amount)
    
    elif choice == "2":
        guild = input("Guild ID: ")
        message = input("Message: ")
        amount = int(input("Amount per channel: "))
        await raider.spam_all_channels(guild, message, amount)
    
    elif choice == "3":
        channel = input("Channel ID: ")
        message = input("Message ID: ")
        emoji = input("Emoji: ")
        await raider.add_reaction(channel, message, emoji)
    
    elif choice == "4":
        invite = input("Invite code: ")
        await raider.join_server(invite)
    
    elif choice == "5":
        guild = input("Guild ID: ")
        await raider.leave_server(guild)
    
    elif choice == "6":
        guild = input("Guild ID: ")
        nick = input("Nickname: ")
        await raider.change_nickname(guild, nick)
    
    elif choice == "7":
        status = input("Status (online/dnd/idle/invisible): ")
        custom = input("Custom status: ")
        await raider.change_status(status, custom)

if __name__ == "__main__":
    asyncio.run(main())
