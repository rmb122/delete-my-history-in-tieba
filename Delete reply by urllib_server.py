from urllib import request
from urllib import parse
from urllib import error
import sys
import json
import re
import time
    
startPageNumber=1 
endPageNumber=10

def writeLog(content):
    logPath=sys.path[0]+'/log.txt'
    logFile=open(logPath,'a')    
    logFile.write(content+'\n')
    logFile.close()

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
    
    
writeLog('\n'+time.asctime(time.localtime(time.time()))) 
    
try:
    request.urlopen('http://www.baidu.com')
except:
    writeLog('Exit reason: No connection') 
    sys.exit(0)
  
cookiePath=sys.path[0]+'/cookie.json' 
cookieFile=open(cookiePath)
cookie=cookieFile.read()
cookie=cookie.replace('\n','')
cookie=json.loads(cookie)

cookieStr=''
for aCookie in cookie:
    cookieStr=cookieStr+aCookie['name']+'='+aCookie['value']+';' 
cookieStr=cookieStr[0:len(cookieStr)-1] 

header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    'Cookie':cookieStr 
    }

opener=request.build_opener()

listReg=re.compile(r'<span class="b_reply_txt"><a class="b_reply" href="\/p\/([0-9]{0,})\?fid=([0-9]{0,})&amp;pid=([0-9]{0,})&amp;cid=([0-9]{0,})#([0-9]{0,})" target="_blank">')

deleteCount=0
replyList=list()
failCount=0

while startPageNumber<=endPageNumber and failCount<5:
    try:
        writeLog('Now collecting page '+str(startPageNumber)+' \'s reply')
        response=opener.open(request.Request(url="http://tieba.baidu.com/i/i/my_reply?pn="+str(startPageNumber),headers=header))         
        pageSource=response.read().decode() 
        replyList+=listReg.findall(pageSource)       
        startPageNumber+=1
    except error.URLError:
        writeLog('Failed to Collect. Now retrying')
        failCount+=1
        continue 
    except UnicodeDecodeError: 
        writeLog('Cookie has been expried. Please update it')
        sys.exit(0)    

writeLog('Collected '+str(len(replyList))+' replies')        

for reply in replyList:
    tid=reply[0] 
    fid=reply[1]
    pid=reply[2]
    cid=reply[3] 
    tbs=getTbs(opener)
    if cid=='0': 
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
    postData=parse.urlencode(postData).encode() 
    success=False
    
    while not success:
        try:
            response=opener.open(request.Request(url="http://tieba.baidu.com/f/commit/post/delete",headers=header),postData) 
            success=True
            result=json.loads(response.read().decode())
            if result['err_code'] == 220034: 
                writeLog('Delete '+str(deleteCount)+' replies'+' Exit reason: Has been reached 30 per day')
                sys.exit(0)
            if result['err_code'] != 230308:
                deleteCount+=1                            
            writeLog('Err_code: '+str(result['err_code'])+"  "+'Error: '+str(result['error'])+"  "+'Data: '+str(result['data'])+"  "+'Delete Count: '+str(deleteCount)+"  "+'ID: '+str(tid))
            
        except error.URLError: 
            writeLog('Failed to delete reply. Now retrying')
            pass     
            
writeLog('Delete '+str(deleteCount)+' replies'+' Exit reason: All replies has been deleted')            