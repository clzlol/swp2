import csv, random
data = list()
f = open("교육부_3천단어_수정분.csv", 'r', encoding='utf-8-sig')
rea = csv.reader(f)
for row in rea:
    data.append(row[1:4]) #영단어, 한국어뜻, 난이도를 리스트에 저장
f.close

value = [] #랜덤 영단어 인덱스
for _ in range(3):
    value.append(random.randint(1,3000))

words = [] #영단어
kor = [] #한글뜻
for i in range(3):
    words.append(data[value[i]][0])
    kor.append(data[value[i]][1])

print(kor)
print(words)

answer = list(map(str, input().split(", "))) #입력값

result = [] #정답여부
for i in range(3):
    if answer[i]==data[value[i]][1]:
        result.append('correct')
    else:
        result.append('wrong')

print(result)   