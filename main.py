import discord
from discord.ext import commands
import yt_dlp
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ytdl = yt_dlp.YoutubeDL({
    'format': 'bestaudio/best',
    'quiet': True
})

@bot.event
async def on_ready():
    print(f"{bot.user} online hai!")

@bot.command()
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Voice channel join karo")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    info = ytdl.extract_info(url, download=False)
    url2 = info['url']

    source = await discord.FFmpegOpusAudio.from_probe(url2)

    vc.stop()
    vc.play(source)

    await ctx.send("Playing 🎵")

@bot.command()
async def stop(ctx):
    await ctx.voice_client.disconnect()

bot.run(TOKEN)
