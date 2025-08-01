from translator import translate
from config_manager import get_channel_map

async def route_message(client, message):
    channel_map = get_channel_map()
    source_id = str(message.channel.id)

    if source_id in channel_map:
        targets = channel_map[source_id]
        for lang, target_id in targets.items():
            translated = translate(message.content, lang)
            target_channel = client.get_channel(int(target_id))
            await target_channel.send(f"{translated}")
