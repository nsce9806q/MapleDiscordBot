import discord
from discord.ext import commands, tasks
import urllib.parse, urllib.request
from bs4 import BeautifulSoup
import re, datetime

# 디스코드 봇 info
game = discord.Game("MapleStory")
bot = commands.Bot(command_prefix='!',status=discord.Status.online, activity=game)
token = 'ODY2NzczNjY3MDkzNjc2MDgy.YPXb4g.qyqmS68lfa3gUYKiFq_NgoC-DYw'

# 서버 id list
channel1_id = 750692218985119765 # 메 서버
channel2_id = 865269056173375500 # 듀부링 서버

# 로그 남기기 함수
def printLog(str1, str2):
    log = open('MapleDiscordLog.txt','a',encoding='utf-8')
    dt = datetime.datetime.now()
    if(dt.weekday() == 0): weekday = '월'
    if(dt.weekday() == 1): weekday = '화'
    if(dt.weekday() == 2): weekday = '수'
    if(dt.weekday() == 3): weekday = '목'
    if(dt.weekday() == 4): weekday = '금'
    if(dt.weekday() == 5): weekday = '토'
    if(dt.weekday() == 6): weekday = '일'

    print("{}년{}월{}일 {}시{}분{}초 {}요일: [{}] {}".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,weekday,str1,str2))
    log.write("{}년{}월{}일 {}시{}분{}초 {}요일: [{}] {}\n".format(dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second,weekday,str1,str2))
    log.close()

# 가이드 임베드
def getContent():
    content = discord.Embed(title='Maple++ 가이드',description='',color=0xE07000)
    content.add_field(name='기능',value="- 이벤트/캐시샵/점검/테스트월드 알림\n- 캐릭터 정보 찾기\n- 더 시드 족보",inline=False)

    guide1 = "1. 캐릭터 정보 찾기\n `!정보 [캐릭터명]` `!찾기 [캐릭터명]` `!조회 [캐릭터명]`\n(공식 홈페이지 - 마이 메이플 - 내정보 관리 - 캐릭터정보 공개설정 필요)\n\n"
    guide2 = "2. 더 시드 족보\n `!시드 [24/39/43층]`\n\n"
    guide3 = "3. 추가 예정\n\n"
    guide4 = "4. 가이드 열기\n `!도움말` `!가이드` `!h`\n\n"
    userGuide = guide1 + guide2 + guide3 + guide4
    content.add_field(name='\n사용법',value=userGuide,inline=False)

    content.set_thumbnail(url="https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FdYWa7r%2FbtqBD13bp4x%2FkYdrNKnKL7PxUj0uqVYuSK%2Fimg.png")
    content.set_footer(text="developed by 쪽빛월야@리부트")

    return content

# 도움말
@bot.command(aliases=["도움말","h","가이드"])
async def getHelp(ctx):
    content = getContent()
    await ctx.send(embed=content)

# 캐릭터 정보 URL 반환 함수
def getCharacterURL(nickname):
    url = "https://maplestory.nexon.com/Ranking/World/Total?c={}&w=254".format(urllib.parse.quote(nickname))
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    characterURL = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td.left > dl > dt > a")
    # 리부트 우선 검색 후 본섭 검색
    if (characterURL == None):
        url = "https://maplestory.nexon.com/Ranking/World/Total?c={}&w=0".format(urllib.parse.quote(nickname))
        html = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        characterURL = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td.left > dl > dt > a")

    return "https://maplestory.nexon.com"+characterURL['href']

# 주스탯 반환 함수
def getStat(statSTR, statDEX, statINT, statLUK):
    statList = [statSTR, statDEX, statINT, statLUK]
    index = statList.index(max(statList))
    
    # data[0] = 주스탯 정보, data[1] = hex 컬러 정보 
    data = []
    if(index == 0):
        data.append('STR: {}'.format(str(statSTR)))
        data.append(0xFF0000) #빨강
        return data
    elif(index == 1):
        data.append('DEX: {}'.format(str(statDEX)))
        data.append(0x00CC00) #초록
        return data
    elif(index == 2):
        data.append('INT: {}'.format(str(statINT)))
        data.append(0x9600CC) #보라
        return data
    elif(index == 3):
        data.append('LUK: {}'.format(str(statLUK)))
        data.append(0xFF00E4) #자주
        return data

# ',' 문자 제거 함수
def removeComma(string):
    return string.replace(',',"")

# 캐릭터 정보 조회
@bot.command(aliases=["정보","찾기","조회"])
async def characterInfo(ctx, nickname:str):

    # 캐릭터 정보 가져오기
    url = getCharacterURL(nickname)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    world = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2) > span")
    level = soup.select_one("#wrap > div.center_wrap > div.char_info_top > div.char_info > dl:nth-child(1) > dd")
    job = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(4) > span")

    try:
        statSTR = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(4) > tbody > tr:nth-child(2) > td:nth-child(4) > span")
        statDEX = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(4) > tbody > tr:nth-child(3) > td:nth-child(2) > span")
        statINT = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(4) > tbody > tr:nth-child(3) > td:nth-child(4) > span")
        statLUK = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(4) > tbody > tr:nth-child(4) > td:nth-child(2) > span")

        # 제논, 데벤져 예외 처리
        if(job == '제논'):
            stat = "STR: {} DEX: {} LUK: {}".format(removeComma(statSTR.text),removeComma(statDEX.text),removeComma(statLUK.text))
            color = 0x9600CC
        elif(job == '데몬어벤져'):
            hp = soup.select_one("#container > div.con_wrap > div.contents_wrap > div > div.tab01_con_wrap > table:nth-child(4) > tbody > tr:nth-child(1) > td:nth-child(4) > span")
            stat = "HP: {}".format(removeComma(hp.text))
            color = 0xFF0000
        else:
            statData = getStat(int(removeComma(statSTR.text)),int(removeComma(statDEX.text)),int(removeComma(statINT.text)),int(removeComma(statLUK.text)))
            stat = statData[0]
            color = statData[1]
    except:
        world = soup.select_one("#wrap > div.center_wrap > div.char_info_top > div.char_info > dl:nth-child(3) > dd")
        level = soup.select_one("#wrap > div.center_wrap > div.char_info_top > div.char_info > dl:nth-child(1) > dd")
        job = soup.select_one("#wrap > div.center_wrap > div.char_info_top > div.char_info > dl:nth-child(2) > dd")
        stat = "캐릭터 정보 공개 설정 필요"
        color = 0xFF0000

    job = job.text.split('/')

    characterImage = soup.select_one("#wrap > div.center_wrap > div.char_info_top > div.char_info > div.char_img > div > img")

    # 무릉, 시드 기록은 공홈(금주, 전주), maple.gg에서 조회

    # 금주 무릉 기록 조회 (공홈)
    url_dojang = "https://maplestory.nexon.com/Ranking/World/Dojang/thisWeek?c={}&t=2".format(urllib.parse.quote(nickname))
    html = urllib.request.urlopen(url_dojang).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    dojang = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(4)")
    dojang_time = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(5)")

    # 금주 무릉 기록이 없다면 전주 기록 조회 (공홈)
    if (dojang == None):
        url_dojang = "https://maplestory.nexon.com/Ranking/World/Dojang/LastWeek?c={}&t=2".format(urllib.parse.quote(nickname))
        html = urllib.request.urlopen(url_dojang).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        dojang = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(4)")
        dojang_time = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(5)")

    # maple.gg 조회
    url_dojang = "https://maple.gg/u/{}".format(urllib.parse.quote(nickname))
    html = urllib.request.urlopen(url_dojang).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    dojangGG = soup.select_one("#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div > div > h1")
    dojangGG_time = soup.select_one("#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div > div > div > small")

    # 공홈과 maple.gg 둘 중 더 높은 기록 반영
    if(dojang == None and dojangGG == None):
        dojang_record = "기록이 없습니다."
    elif(dojang == None and dojangGG != None):
        dojang_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', dojangGG.text),dojangGG_time.text)
    elif(dojang != None and dojangGG == None):
        dojang_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', dojang.text),dojang_time.text)
    else:
        print(dojang)
        print(dojangGG)
        if(int(re.sub(r'[^0-9]', '', dojang.text)) > int(re.sub(r'[^0-9]', '', dojangGG.text))):
            dojang_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', dojang.text),dojang_time.text)
        else:
            dojang_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', dojangGG.text),dojangGG_time.text)

    # 금주 시드 기록 조회
    url_seed = "https://maplestory.nexon.com/Ranking/World/Seed/ThisWeek?c={}".format(urllib.parse.quote(nickname))
    html = urllib.request.urlopen(url_seed).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    seed = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(4)")
    seed_time = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(5)")

    # 금주 시드 기록이 없다면 전주 기록 조회
    if (seed == None):
        url_seed = "https://maplestory.nexon.com/Ranking/World/Seed/LastWeek?c={}".format(urllib.parse.quote(nickname))
        html = urllib.request.urlopen(url_seed).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        seed = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(4)")
        seed_time = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr.search_com_chk > td:nth-child(5)")

    # maple.gg 조회
    url_seed = "https://maple.gg/u/{}".format(urllib.parse.quote(nickname))
    html = urllib.request.urlopen(url_seed).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    seedGG = soup.select_one("#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div > div > h1")
    seedGG_time = soup.select_one("#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(2) > section > div > div > div > small")

    # 공홈과 maple.gg 둘 중 더 높은 기록 반영
    if(seed == None and seedGG == None):
        seed_record = "기록이 없습니다."
    elif(seed == None and seedGG != None):
        seed_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', seedGG.text),seedGG_time.text)
    elif(seed != None and seedGG == None):
        seed_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', seed.text),seed_time.text)
    else:
        if(int(re.sub(r'[^0-9]', '', seed.text)) > int(re.sub(r'[^0-9]', '', seedGG.text))):
            seed_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', seed.text),seed_time.text)
        else:
            seed_record = "{}층 ({})".format(re.sub(r'[^0-9]', '', seedGG.text),seedGG_time.text)

    # 캐릭터 정보 embed 만들기
    content = discord.Embed(title="[{}] 캐릭터 정보".format(nickname),color=color)
    content.add_field(name="레벨",value=re.sub(r'[^0-9]', '', level.text),inline=True)
    content.add_field(name="직업",value=job[1],inline=True)
    content.add_field(name="월드",value=world.text,inline=True)
    content.add_field(name="주스탯",value=stat,inline=False)
    content.add_field(name="무릉 도장",value=dojang_record,inline=True)
    content.add_field(name="더 시드",value=seed_record,inline=True)
    content.set_thumbnail(url=characterImage['src'])

    await ctx.send(embed=content)
    printLog("캐릭터 정보 조회",nickname)

# 캐릭터 조회 예외 처리
@characterInfo.error
async def characterInfo_error(ctx,error):
    await ctx.send("캐릭터의 정보가 없거나 공식 홈페이지 - 마이 메이플 - 내정보 관리 - 캐릭터정보 공개설정이 필요합니다.")
    print(error)

# 더 시드 족보
@bot.command(aliases=["시드","seed"])
async def theSeed(ctx, floor:str):
    if("24" in floor):
        title = "더 시드 24층 BGM"
        url = "https://www.youtube.com/watch?v=tvBfW1m6DiM"
    elif("39" in floor):
        title = "더 시드 39층 족보"
        url = "http://39.theseed.ze.am/"
    elif("43" in floor):
        title = "더 시드 43층 문제 기록지"
        url = "http://43.theseed.ze.am/"
    else:
        title = "24층/39층/43층만 가능합니다."
        url = ''

    content = discord.Embed(title=title,description=url,color=0x00FF00)
    content.set_footer(text="리레 4렙 기원")
    await ctx.send(embed=content)
    printLog("더 시드",floor)

# 더 시드 족보 예외 처리
@theSeed.error
async def theSeed_error(ctx,error):
    await ctx.send("입력 예시: `시드 39층`")
    print(error)

# 이벤트 공지 함수
async def eventNoticeFunc():
    constant = open("event_num.txt",'r',encoding='utf-8')
    temp = constant.readline()
    constant.close()
    url = "https://maplestory.nexon.com/News/Event/Ongoing/{}".format(temp)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one("#container > div > div.contents_wrap > p > span")
    date = soup.select_one("#container > div > div.contents_wrap > div.qs_info_wrap > span")
    image = soup.select_one("#container > div > div.contents_wrap > div.qs_text > div > div:nth-child(1) > div > img")
    if(title == None):
        pass
    else:
        content = discord.Embed(title=title.text,description=url,color=0xFF91D5)
        try:
            content.set_image(url=image['src'])
        except:
            pass
        content.set_footer(text=date.text)
        channel1 = bot.get_channel(channel1_id)
        channel2 = bot.get_channel(channel2_id)
        await channel1.send(embed=content)
        printLog("이벤트 공지1",title.text)
        await channel2.send(embed=content)
        printLog("이벤트 공지2",title.text)
        constant = open("event_num.txt",'w',encoding='utf-8')
        temp = str(int(temp) + 1)
        constant.write(temp)
        constant.close()
        await eventNoticeFunc()

# 캐시샵 공지 함수
async def cashNoticeFunc():
    constant = open("cashshop_num.txt",'r',encoding='utf-8')
    temp = constant.readline()
    constant.close()
    url = "https://maplestory.nexon.com/News/CashShop/Sale/{}".format(temp)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.select_one("#container > div > div.contents_wrap > p > span")
    date = soup.select_one("#container > div > div.contents_wrap > div.qs_info_wrap > span")
    image = soup.select_one("#container > div > div.contents_wrap > div.qs_text > div > div:nth-child(1) > div > img")

    if(title == None):
        pass
    else:
        content = discord.Embed(title=title.text,description=url,color=0xFFFF00)
        content.set_image(url=image['src'])
        content.set_footer(text=date.text)
        channel1 = bot.get_channel(channel1_id)
        channel2 = bot.get_channel(channel2_id)
        await channel1.send(embed=content)
        printLog("캐시샵 공지1",title.text)
        await channel2.send(embed=content)
        printLog("캐시샵 공지2",title.text)
        constant = open("cashshop_num.txt",'w',encoding='utf-8')
        temp = str(int(temp) + 1)
        constant.write(temp)
        constant.close()
        await cashNoticeFunc()

#이벤트 알림 (30분 주기)
@tasks.loop(minutes=30)
async def eventNotice():
    await eventNoticeFunc()

# 캐시샵 알림 (30분 주기)
@tasks.loop(minutes=30)
async def cashNotice():
    await cashNoticeFunc()

# 점검 공지 알림 (30분 주기) 
@tasks.loop(minutes=30)
async def inspection():
    file = open('inspection.txt','r',encoding='utf-8')
    oldPost = file.readline()
    file.close()

    url = "https://maplestory.nexon.com/News/Notice/Inspection"
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    newPost = soup.select_one("#container > div > div.contents_wrap > div.news_board > ul > li:nth-child(1) > p > a > span")

    if(newPost.text == oldPost):
        pass
    else:
        url = soup.select_one("#container > div > div.contents_wrap > div.news_board > ul > li:nth-child(1) > p > a")
        content = discord.Embed(title=newPost.text,description="https://maplestory.nexon.com"+url['href'],color=0x00B8DB)
        channel1 = bot.get_channel(channel1_id)
        channel2 = bot.get_channel(channel2_id)
        await channel1.send(embed=content)
        printLog("점검 공지1",newPost.text)
        await channel2.send(embed=content)
        printLog("점검 공지2",newPost.text)
        file = open('inspection.txt','w',encoding='utf-8')
        file.write(newPost.text)
        file.close()

# 테스트 서버 공지 알림 (30분 주기)
@tasks.loop(minutes=30)
async def testServer():
    file = open('testserver.txt','r',encoding='utf-8')
    oldPost = []
    for i in range(0,5):
        oldPost.append(file.readline())
    file.close()

    
    url = "https://maplestory.nexon.com/News/Notice/Notice"
    html = urllib.request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    newPost = []
    for i in range(1,6):
        tempPost = soup.select_one("#container > div > div.contents_wrap > div.news_board > ul > li:nth-child({}) > p > a > span".format(i))
        newPost.append(tempPost.text)

    for i in range(0,5):
        temp = True
        for j in range(0,5):
            if(newPost[i] in oldPost[j]):
                temp = False
        
        if(temp == True):
            if('테스트월드' in newPost[i]):
                if ('종료' in newPost[i]):
                    pass
                else:
                    url = soup.select_one("#container > div > div.contents_wrap > div.news_board > ul > li:nth-child(1) > p > a")
                    content = discord.Embed(title=newPost[i],description="https://maplestory.nexon.com"+str(url['href']),color=0x4490E1)
                    channel1 = bot.get_channel(channel1_id)
                    channel2 = bot.get_channel(channel2_id)
                    await channel1.send(embed=content)
                    printLog("테스트 서버 공지1",newPost[i])
                    await channel2.send(embed=content)
                    printLog("테스트 서버 공지2",newPost[i])
    
    file = open('testserver.txt','w',encoding='utf-8')
    file.write(newPost[0])
    file.write('\n'+newPost[1])
    file.write('\n'+newPost[2])
    file.write('\n'+newPost[3])
    file.write('\n'+newPost[4])
    file.close()

# 최초 실행
@bot.event
async def on_ready():
    # content = getContent()
    # channel1 = bot.get_channel(channel1_id)
    # channel2 = bot.get_channel(channel2_id)
    # await channel1.send(embed=content)
    # await channel2.send(embed=content)
    eventNotice.start()
    cashNotice.start()
    inspection.start()
    testServer.start()

bot.run(token)