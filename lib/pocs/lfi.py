from lib.utils import *
import requests
import copy
from urllib import urlencode


def poc(request,config):
    exists = 0
    result = ''
    try:
        reqs = config['requests']
        resp = config['responces']
        headers,cookiesJar=parseHeaders(request['headers'])
        url,get_params=url2params(request)
        session=requests.session()
        for p in get_params:
            new_params=copy.copy(get_params)
            for fi in reqs:
                new_params[p]=fi
                new_url=url+'?'+urlencode(new_params)
                if(request['method']=='GET'):
                    back_content=session.get(new_url,cookies=cookiesJar,headers=headers,timeout=5).content
                elif(request['method']=='POST'):
                    back_content=session.post(new_url,cookies=cookiesJar,headers=headers,timeout=5).content
                for res in resp:
                    if res in back_content:
                        exists+=1
                        result+='lfi found:get param %s\n'%p
    except Exception,e:
        print (e.message)
    finally:
        return exists,result

if __name__=='__main__':
    print poc({'url':"http://127.0.0.1:5555/echo.php?1=a",'headers':{},'method':'GET'},{'xss_str':'mdzz'})