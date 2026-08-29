pythonimport discord
import requests

TOKEN_DISCORD = "MTU0MzA3NDI5MjI1NjczOTQwMQ.GDUgDc.d88_bWm97WGRNOxt4JTDK6JVn774LXhPFuvNqs"
BOT_ID_BOTPRESS = "e42f29a4-2a11-4ae3-b251-4cbc2a659b09"
API_KEY_BOTPRESS = "bp_pat_exEOqIOIe7ST4XM72BIqqRIUdctULThIioMb"

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Пахан зашел в хату Дискорда как {bot.user}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        clean_text = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        if not clean_text:
            await message.reply("Че притих, пассажир? Говори по делу, не тяни резину.")
            return

        async with message.channel.typing():
            # ВОТ ЗДЕСЬ ССЫЛКА ИСПРАВЛЕНА НА ПРАВИЛЬНУЮ:
            url = "https://botpress.cloud/v1/chat/messages"
            headers = {
                "Authorization": f"Bearer {API_KEY_BOTPRESS}",
                "Content-Type": "application/json",
                "x-bot-id": BOT_ID_BOTPRESS
            }
            payload = {
                "payload": {"type": "text", "text": clean_text},
                "conversationId": f"discord_{message.author.id}"
            }
            
            try:
                res = requests.post(url, json=payload, headers=headers).json()
                bot_response = res.get('message', {}).get('payload', {}).get('text', "Че-то связь оборвалась, за базар отвечать некому.")
                await message.reply(bot_response)
            except Exception:
                await message.reply("Связь лагает, чертила. Обожди немного.")

bot.run(TOKEN_DISCORD)