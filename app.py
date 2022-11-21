import nextcord
from nextcord.ext import commands
import requests, json, random, datetime, asyncio

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# !hi
# Hello!

@bot.command(name = "시간")
async def SendMessage(ctx):
    await ctx.send(datetime.datetime.now())

async def schedule_daily_message():
    # wait for some time
    # send a message
    # while True:
    #     now = datetime.datetime.now()
    #     #then = now + datetime.timedelta(days = 0)
    #     then = now.replace(hour = 16, minute = 37)
    #     wait_time = (then - now).total_seconds()
    #     await asyncio.sleep(wait_time)

    #     channel = bot.get_channel(1042374278424829955)

    #     await channel.send("Good morning")
    print("주기적인 영어 단어 제시")


eng = ['A', 'B', 'C']
words = ['가', '나', '다']
repeat = {}


@bot.command(name = "정답")
async def answer(ctx, first:str, second:str, third:str):
    answer = [first, second, third]
    result=[]
    wrong_count=0
    for i in range(3):
        if answer[i] != words[i]:
            result.append('wrong')
            wrong_count+=1
            repeat[eng[i]] = words[i]
    if wrong_count == 0:
        await ctx.send("만점!")
    else:
        await ctx.send(f"{wrong_count}개 틀렸습니다.")


@bot.command(name = "복습")
async def rework(ctx):
    repeat_output=""
    for key in repeat:
         repeat_output += f"{key} : {repeat[key]}\n"
    await ctx.send(repeat_output)


@bot.command(name="재시험")
async def retest(ctx):
    print("복습하세요!")




@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    await schedule_daily_message()

if __name__ == '__main__':
    bot.run("MTA0NDEwNTQ4NTYyNTg2MDEzNw.GVYEnF.wq_fniuyKiERUOhNkhOV7IztJZfbPrVE_YLxnU")
