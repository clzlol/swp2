import nextcord
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="^", intents=intents)

# !hi
# Hello!

@bot.command(name = "hi")
async def SendMessage(ctx):
    await ctx.send('Hello!')

@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")

if __name__ == '__main__':
    bot.run("MTA0NDEwNTQ4NTYyNTg2MDEzNw.G2V1MC.IFV0lKqe4-VAYqMmS3IlhNlXfNPB2YETVzC_-k")