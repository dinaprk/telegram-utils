from telethon.sync import TelegramClient, events
from telethon.tl.types import Photo

from auth import API_ID, API_HASH, SESSION

with TelegramClient(SESSION, API_ID, API_HASH) as client:
    @client.on(events.NewMessage(pattern="/pfp.*"))
    async def cmd_pfp(event):
        message_words = event.text.split()
        target: str = message_words[1]
        target = event.chat_id if target == "." else target
        try:
            params = {"limit": int(message_words[2])}
        except (IndexError, ValueError):
            params = {}

        # hide command usage from chat
        # await event.delete()

        photos: list[Photo] = [photo async for photo in client.iter_profile_photos(target, **params)]

        print(f"Sending {params.get('limit', 'all')} profile photos of {target}")
        await client.send_file(event.chat_id, photos)


    client.run_until_disconnected()
