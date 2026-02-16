import discord
from discord.ext import commands
import yt_dlp
import os

TOKEN = os.getenv("TOKEN") or "MTQ3MjcyMjc3NTIzMDY0NDM5OA.Gqy8fI.8itmESt-IvpTTxFhH_10uyrEGGLEyFHE_rXej0"

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

ytdl_format_options = {
    'format': 'bestaudio',
    'quiet': True,
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="24/7 Music 🎵")
    )

@bot.command()
async def play(ctx, *, url):
    if not ctx.author.voice:
        await ctx.send("ادخل روم صوتي اول 😅")
        return

    channel = ctx.author.voice.channel

    if not ctx.voice_client:
        await channel.connect()

    info = ytdl.extract_info(url, download=False)
    url2 = info['url']

    source = await discord.FFmpegOpusAudio.from_probe(
        url2,
        method='fallback'
    )

    ctx.voice_client.play(source)
    await ctx.send("شغلت الاغنية 🔥")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("وقفت الموسيقى 👌")

bot.run(TOKEN)

