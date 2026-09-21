import asyncio
import json
import requests
from utils import DiscordAPI, Logger, TokenValidator

class DiscordTools:
    @staticmethod
    async def check_token(token):
        valid, data = await TokenValidator.validate(token)
        if valid:
            Logger.success(f"Token is VALID")
            print(f"Username: {data['username']}#{data['discriminator']}")
            print(f"ID: {data['id']}")
            print(f"Email: {data.get('email', 'N/A')}")
            print(f"Phone: {data.get('phone', 'N/A')}")
            print(f"MFA: {data.get('mfa_enabled', False)}")
            print(f"Verified: {data.get('verified', False)}")
            return True
        else:
            Logger.error("Token is INVALID")
            return False
    
    @staticmethod
    async def check_tokens(tokens):
        Logger.info(f"Checking {len(tokens)} tokens")
        valid_tokens = []
        
        for token in tokens:
            valid, data = await TokenValidator.validate(token.strip())
            if valid:
                valid_tokens.append((token, data))
                Logger.success(f"✓ {data['username']}")
        
        Logger.info(f"\nValid: {len(valid_tokens)}/{len(tokens)}")
        return valid_tokens
    
    @staticmethod
    async def get_guild_info(guild_id, token):
        api = DiscordAPI(token)
        status, data = await api.request('GET', f'https://discord.com/api/v9/guilds/{guild_id}')
        
        if status == 200:
            Logger.success(f"Guild Info for {data['name']}")
            print(f"Name: {data['name']}")
            print(f"ID: {data['id']}")
            print(f"Owner ID: {data['owner_id']}")
            print(f"Member Count: {data.get('member_count', 'N/A')}")
            print(f"Description: {data.get('description', 'N/A')}")
            print(f"Verification Level: {data.get('verification_level', 'N/A')}")
            print(f"Features: {', '.join(data.get('features', []))}")
            return data
        else:
            Logger.error("Failed to fetch guild info")
            return None
    
    @staticmethod
    async def get_token_info(token):
        valid, data = await TokenValidator.validate(token)
        if valid:
            Logger.success("Token Information:")
            
            # Get billing info
            api = DiscordAPI(token)
            status, billing = await api.request('GET', 'https://discord.com/api/v9/users/@me/billing/payment-sources')
            
            print("\n=== Account Info ===")
            print(f"Username: {data['username']}#{data['discriminator']}")
            print(f"ID: {data['id']}")
            print(f"Email: {data.get('email', 'N/A')}")
            print(f"Phone: {data.get('phone', 'N/A')}")
            print(f"Bio: {data.get('bio', 'N/A')}")
            print(f"Avatar: {data.get('avatar', 'N/A')}")
            print(f"Banner: {data.get('banner', 'N/A')}")
            print(f"Accent Color: {data.get('accent_color', 'N/A')}")
            print(f"Locale: {data.get('locale', 'N/A')}")
            
            print("\n=== Security ===")
            print(f"MFA Enabled: {data.get('mfa_enabled', False)}")
            print(f"Verified: {data.get('verified', False)}")
            
            print("\n=== Billing ===")
            if status == 200 and billing:
                print(f"Payment Methods: {len(billing)}")
                for method in billing:
                    print(f"  - {method.get('brand', 'Unknown')} ****{method.get('last_4', '')}")
            else:
                print("No payment methods found")
            
            return data
        return None
    
    @staticmethod
    async def get_tokens_info(tokens):
        results = []
        for token in tokens:
            info = await DiscordTools.get_token_info(token.strip())
            if info:
                results.append((token, info))
        
        Logger.info(f"\nCollected info for {len(results)} tokens")
        return results

async def main():
    print("\n22. Check Token")
    print("23. Check Tokens")
    print("24. Get Guild Info")
    print("25. Get Token Info")
    print("26. Get Tokens Info")
    print("27. Back to Main Menu")
    print("28. Exit")
    
    choice = input("\nSelect option: ")
    
    if choice == "22":
        token = input("Token: ")
        await DiscordTools.check_token(token)
    
    elif choice == "23":
        tokens = input("Tokens (comma separated or file path): ")
        if tokens.endswith('.txt'):
            with open(tokens, 'r') as f:
                tokens_list = f.read().splitlines()
        else:
            tokens_list = tokens.split(',')
        
        await DiscordTools.check_tokens(tokens_list)
    
    elif choice == "24":
        token = input("Token: ")
        guild_id = input("Guild ID: ")
        await DiscordTools.get_guild_info(guild_id, token)
    
    elif choice == "25":
        token = input("Token: ")
        await DiscordTools.get_token_info(token)
    
    elif choice == "26":
        tokens = input("Tokens (comma separated or file path): ")
        if tokens.endswith('.txt'):
            with open(tokens, 'r') as f:
                tokens_list = f.read().splitlines()
        else:
            tokens_list = tokens.split(',')
        
        await DiscordTools.get_tokens_info(tokens_list)
    
    elif choice == "27":
        return "back"
    
    elif choice == "28":
        exit()

if __name__ == "__main__":
    asyncio.run(main())
