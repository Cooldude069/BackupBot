import discord
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="$")


@client.event
async def on_ready():
    print("Bot online.")


TOKEN = "ODQ3ODQzNTY2MzYwNTkyNDY1.YLD92g.CiFVj-jedLY9vsPJvhzHwqlp8DI"
client.load_extension("cogs.Backups")
client.run(TOKEN)
