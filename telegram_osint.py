import asyncio
import re
import json
from telethon import TelegramClient, functions, types

print("[*] Importing load_config from config_handler...")
from config_handler import load_config

# Constants
tgdb_session = "telegram_threatintel_session"
bot_username = 'tgdb_bot'
SESSION_FILE_NAME = tgdb_session
JSON_OUTPUT = "final_results.json"

# Load API credentials
api_id, api_hash = load_config()

# Load keywords from file
def load_keywords(filename="keywords.txt"):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# Extract usernames from messages
def extract_usernames(text):
    return re.findall(r'@[\w\d_]{5,}', text)

# Step 1: Search keywords with bot
async def search_keywords_and_collect_usernames():
    async with TelegramClient(tgdb_session, api_id, api_hash) as client:
        print("[*] Telegram client started for keyword search.")
        all_results = []
        search_modes = ['/group', '/channel', '/title']
        keywords = load_keywords()

        for mode in search_modes:
            await client.send_message(bot_username, mode)
            await asyncio.sleep(1.5)

            for tag in keywords:
                await client.send_message(bot_username, tag)
                await asyncio.sleep(4)

                async for msg in client.iter_messages(bot_username, limit=10):
                    if tag.lower() in msg.text.lower():
                        usernames = extract_usernames(msg.text)
                        for user in usernames:
                            all_results.append({
                                "username": user,
                                "type": mode.replace('/', '')
                            })

        # Deduplicate
        seen = set()
        unique_results = []
        for entry in all_results:
            key = (entry['username'], entry['type'])
            if key not in seen:
                unique_results.append(entry)
                seen.add(key)

        print(f"[+] Found {len(unique_results)} unique usernames.")
        return unique_results

# Step 2: Enrich usernames with channel info + similar channels
async def get_channel_info(client, username):
    try:
        entity = await client.get_entity(username)
        return entity.id, entity.title
    except Exception as e:
        print(f"[!] Error fetching channel info for {username}: {e}")
        return None, None

async def safe_api_request(coroutine):
    try:
        return await coroutine
    except Exception as e:
        print(f"[!] Error during API request: {e}")
        return None

async def get_similar_channels(client, username):
    try:
        entity = await client.get_input_entity(username)
        if isinstance(entity, (types.InputChannel, types.InputPeerChannel)):
            input_channel = types.InputChannel(channel_id=entity.channel_id, access_hash=entity.access_hash)
            result = await safe_api_request(client(functions.channels.GetChannelRecommendationsRequest(channel=input_channel)))
            if not result:
                return []
            return [{
                'username': f"@{ch.username}" if ch.username else None,
                'title': ch.title,
                'id': ch.id
            } for ch in result.chats if ch.username]
        return []
    except Exception as e:
        print(f"[!] Error fetching similar channels for {username}: {e}")
        return []

async def enrich_usernames_with_similar_channels(user_entries):
    client = TelegramClient(SESSION_FILE_NAME, api_id, api_hash)
    results = []

    async with client:
        for entry in user_entries:
            username = entry['username']
            if not username.startswith('@'):
                username = '@' + username

            channel_id, title = await get_channel_info(client, username)
            if channel_id is None:
                continue

            similar = await get_similar_channels(client, username)

            results.append({
                "username": username,
                "channels_name": title,
                "similar_channels": similar
            })

    return results

# Save to JSON
def save_to_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Full execution
async def main():
    user_entries = await search_keywords_and_collect_usernames()
    enriched_data = await enrich_usernames_with_similar_channels(user_entries)
    save_to_json(enriched_data, JSON_OUTPUT)
    print(f"[+] Final data saved to {JSON_OUTPUT}")

# Entrypoint
if __name__ == "__main__":
    asyncio.run(main())
