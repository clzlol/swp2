import nextcord
from nextcord.ext import commands
import requests, json, random, datetime, asyncio, csv

global words, kor, value, data, repeat
words = [] #영단어
kor = [] #한글뜻
value = [] #랜덤 영단어 인덱스
repeat = {} #틀린 단어 저장 dict

data = list()
f = open("교육부_3천단어_수정분.csv", 'r')
rea = csv.reader(f)
for row in rea:
    data.append(row[1:4]) #영단어, 한국어뜻, 난이도를 리스트에 저장
f.close

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


async def schedule_daily_message():
    # wait for some time
    # send a message
    now = datetime.datetime.now()
    #then = now + datetime.timedelta(days = 1)
    then = now.replace(hour = 16, minute = 55)
    wait_time = (then - now).total_seconds()
    await asyncio.sleep(wait_time)

    value.clear()
    for _ in range(3):
        value.append(random.randint(1,3000))

    words.clear()
    kor.clear()
    for i in range(3):
        words.append(data[value[i]][0])
        kor.append(data[value[i]][1])
        kor[i] = kor[i].split(", ")
    print(kor)
    
    channel = bot.get_channel(1042374278424829955)

    await channel.send(f"{words[0]}, {words[1]}, {words[2]}")

    
@bot.command(name = "시간")
async def SendMessage(ctx):
    await ctx.send(datetime.datetime.now())


@bot.command(name = "정답")
async def answer(ctx, one:str, two:str, three:str):
    answer = [one, two, three]
    print(answer)
    wrong_count=0
    for i in range(3):
        if len(kor[i]) != 1:
            if answer[i] not in kor[i]:
                wrong_count += 1
                repeat[words[i]] = ", ".join(kor[i])
        else:
            if answer[i] != kor[i][0]:
                wrong_count += 1
                repeat[words[i]] = kor[i][0]
    
    if wrong_count == 0:
        await ctx.send("만점!")
    else:
        await ctx.send(f"{wrong_count}개 틀렸습니다.")


@bot.command(name = "복습")
async def rework(ctx):
    repeat_output="다음 단어들을 틀렸어요.\n"
    for key in repeat:
         repeat_output += f"{key} : {repeat[key]}\n"
    await ctx.send(repeat_output)



@bot.command(name="재시험") #틀린 단어 재시험
async def retest(ctx):
    print("복습하세요!")


@bot.command(name="주간기록")
async def recall(ctx):
    #일주일 동안 틀린 단어 출력
    pass


@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    await schedule_daily_message()

    
if __name__ == '__main__':
    bot.run("MTA0NDEwNTQ4NTYyNTg2MDEzNw.GVYEnF.wq_fniuyKiERUOhNkhOV7IztJZfbPrVE_YLxnU")