import http.client
import hashlib
import urllib.parse
import random
import json
import time
chtTransDic={}
enTransDic={}
frTransDic={}
def baiduTranslate(q="structure étatique", fromLang="fra", toLang="cht"):
    #print(q)
    # appid = '20200305000392970' #你的appid(这里是必填的, 从百度 开发者信息一览获取)
    # secretKey = 'xpDfHkO0hWJpPKhrtEeO' #你的密钥(这里是必填的, 从百度 开发者信息一览获取)
    # appid = '20200311000396568'
    # secretKey = 'Ogt39jKDJTbONJ1OxZ6Y'
    appid = '20200312000397158'
    secretKey = 'Rg2o_T_13X4LvWCQDUVJ'
    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode())
    sign = m1.hexdigest()
    myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    result = ""
    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com',timeout=10)
        httpClient.request('GET', myurl)
        #response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
    except Exception as e:
        print (e)
        time.sleep(50)
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com',timeout=10)
        httpClient.request('GET', myurl)
        # response是HTTPResponse对象
        response = httpClient.getresponse()
        result = response.read()
    finally:
        if httpClient:
            httpClient.close()
    result=json.loads(result)['trans_result'][0]['dst']
    result=result.replace(' ','')
    return [q.replace(' ',''),result.lower()]


def transList(ql,s,d):
    result=[]
    n=0
    for q in ql:
        trans=''
        if d=='cht':
            if q in chtTransDic:
                trans=chtTransDic[q]
            else:
                trans=baiduTranslate(q,s,d)
                if len(chtTransDic)>100:
                    chtTransDic.popitem()
                chtTransDic[q]=trans
        if d=='en':
            if q in enTransDic:
                trans=enTransDic[q]
            else:
                trans=baiduTranslate(q,s,d)
                if len(enTransDic)>100:
                    enTransDic.popitem()
                enTransDic[q]=trans
        if d=='fr':
            if q in frTransDic:
                trans=frTransDic[q]
            else:
                trans=baiduTranslate(q,s,d)
                if len(frTransDic)>100:
                    frTransDic.popitem()
                frTransDic[q]=trans
        if trans!=None:
            result.append(trans)
    return result
print(baiduTranslate())