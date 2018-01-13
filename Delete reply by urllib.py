from urllib import request
from urllib import parse
from urllib import error
import sys
import json
import re
import os
import time

startPageNumber=1 #在这里设置回复的搜索起始和结束位置
endPageNumber=3

def getTbs(opener):
    tbs=''
    while tbs=='':
        try:
            response=opener.open(request.Request(url="http://tieba.baidu.com/dc/common/tbs",headers=header))
            tbs=response.read().decode()
        except error.URLError:
            pass 
    tbs=json.loads(tbs)
    tbs=tbs['tbs']
    return tbs

'''    
timePath=sys.path[0]+'\\lastTime.txt' 

timeLast=0
if os.path.exists(timePath):
    timeFile=open(timePath,'r')
    timeLast=timeFile.read()
    timeFile.close()  #读取最后一次运行时间的日期

timeNow=time.strftime('%Y-%m-%d',time.localtime(time.time()))

if timeLast!=timeNow:
    timeFile=open(timePath,'w') 
    timeFile.write(timeNow) #写入新的时间
    timeFile.close()  
else:
    sys.exit(0) #同一天退出程序 
'''

cookiePath=sys.path[0]+'\\cookie.json' #读取cookie
cookieFile=open(cookiePath)
cookie=cookieFile.read()
cookie=cookie.replace('\n','')
cookie=json.loads(cookie)

cookieStr=''
for aCookie in cookie:
    cookieStr=cookieStr+aCookie['name']+'='+aCookie['value']+';' #构造cookie
cookieStr=cookieStr[0:len(cookieStr)-1] #删掉最后一个；

header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Cookie':cookieStr 
    }

opener=request.build_opener()

listReg=re.compile(r'<span class="b_reply_txt"><a class="b_reply" href="\/p\/([0-9]{0,})\?fid=([0-9]{0,})&amp;pid=([0-9]{0,})&amp;cid=([0-9]{0,})#([0-9]{0,})" target="_blank">')

deleteCount=0
replyList=list()

while startPageNumber<=endPageNumber:
    try:
        print('正在收集第',startPageNumber,'页的回复')
        response=opener.open(request.Request(url="http://tieba.baidu.com/i/i/my_reply?pn="+str(startPageNumber),headers=header)) #获取回复列表        
        pageSource=response.read().decode() #读取网页
        replyList+=listReg.findall(pageSource) #匹配回复列表        
        startPageNumber+=1
    except error.URLError:
        print('收集失败，重试中')
        continue        
    except UnicodeDecodeError: #cookie过期会被重定向到http://static.tieba.baidu.com/tb/error.html?ErrType=1，用的是GBK编码。。所以会导致DecodeError。
        print('Cookie过期或无效，请更换')
        sys.exit(0)    

print('共收集到',len(replyList),'条回复\n')
print('开始删除')        
        
for reply in replyList:
    tid=reply[0] #找到对应ID
    fid=reply[1]
    pid=reply[2]
    cid=reply[3] 
    tbs=getTbs(opener)
    if cid=='0': #对应的是楼中楼id,如果是0的话说明这条回复是一整楼.反之这条回复是一个楼中楼.
        postData={
            'ie':'utf-8',
            'tbs':tbs,
            'fid':fid,
            'tid':tid,
            'delete_my_post':'1',
            'delete_my_thread':'0',
            'is_vipdel':'0',
            'pid':pid,
            'is_finf':'1'
        }
    else:
        postData={
            'ie':'utf-8',
            'tbs':tbs,
            'fid':fid,
            'tid':tid,
            'delete_my_post':'1',
            'delete_my_thread':'0',
            'is_vipdel':'0',
            'pid':cid,
            'is_finf':'1'
        }
    postData=parse.urlencode(postData).encode() #构造POST报文
    success=False
    
    while not success:
        try:
            response=opener.open(request.Request(url="http://tieba.baidu.com/f/commit/post/delete",headers=header),postData) #发送删帖请求
            success=True
            result=json.loads(response.read())
            if result['err_code'] == 220034: 
                print("已经达到最高每日上限")  
                print('本次共删除',deleteCount,'条')   
                sys.exit(0)
            if result['err_code'] != 230308:
                deleteCount+=1                            
            print('Err_code:',result['err_code'],"  ",'Error:',result['error'],"  ",'Data:',result['data'],"  ",'已删除',deleteCount,'条回复',"  ",'帖子ID',tid)

        except error.URLError: #捕获超时异常
            print('服务器大姨妈来了，重试中')
            pass     
            
print('本次共删除',deleteCount,'条')            