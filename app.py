import nextcord
from nextcord.ext import commands
import random, datetime, asyncio, csv

global words, kor, value, data, repeat
words = [] #영단어
kor = [] #한글뜻
value = [] #랜덤 영단어 인덱스
repeat = {} #틀린 단어 저장 dict


#공부하려는 단어장 불러오기
data = list()
f = open("교육부_3천단어_수정분.csv", 'r')
rea = csv.reader(f)
for row in rea:
    data.append(row[1:3]) #영단어와 한국어뜻을 리스트에 저장
f.close

intents = nextcord.Intents.default()
intents.message_content = True

#명령어 접두사 지정, 게이트웨이설정
bot = commands.Bot(command_prefix="!", intents=intents)


#매일 같은 시간에 단어 시험을 진행한다
async def schedule_daily_message():
    while True:
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days=1)
        then = then.replace(hour = 0, minute=0)
        wait_time = (then - now).total_seconds()
        print(wait_time)
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
        #print(kor)
        
        channel = bot.get_channel(1042374278424829955) #봇이 단어시험을 진행할 채널 지정

        await channel.send(f"오늘의 단어입니다.\n{words[0]}, {words[1]}, {words[2]}")


#정답 입력하는 명령어 (ex: !정답 답1 답2 답3)
@bot.command(name = "정답")
async def answer(ctx, one:str, two:str, three:str):
    answer = [one, two, three]
    #print(answer)
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


#틀린 단어를 복습하기 위해 영단어와 한글뜻을 출력시키는 명령어 (ex: !복습)
@bot.command(name = "복습")
async def rework(ctx):
    repeat_output="다음 단어들을 틀렸어요.\n"
    for key in repeat:
         repeat_output += f"{key} : {repeat[key]}\n"
    await ctx.send(repeat_output)

    f = open('틀린_단어.csv', 'a', newline='')
    wr = csv.writer(f)
    wr.writerow([f'{datetime.datetime.today().month}/{datetime.datetime.today().day}', '---------', '---------'])
    for key in repeat:
        wr.writerow(['', key, repeat[key]])
    f.close()


#최근 7일간 복습한 단어 출력 (ex: !주간기록)
@bot.command(name="주간기록") 
async def recall(ctx):
    repeat_data = list()
    f = open("틀린_단어.csv", 'r')
    read = csv.reader(f)
    for row in read:
        repeat_data.append(row)
    f.close
    report_output=""
    k=7
    #print(repeat_data)
    for i in range(len(repeat_data)-1, 0, -1):
        if k==0:
            break
        if repeat_data[i][0] != '':
            report_output = "\n" + repeat_data[i][0] + "\n" + report_output
            k-=1
            continue
        report_output = f"{repeat_data[i][1]} : {repeat_data[i][2]}\n" + report_output
    report_output = '다음 단어들을 복습했어요\n' + report_output
    await ctx.send(report_output)


#봇이 준비되는 이벤트가 발생하면 다음 명령어를 실행한다
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    await schedule_daily_message()

#봇 실행
if __name__ == '__main__':
    bot.run("봇 토큰 입력")