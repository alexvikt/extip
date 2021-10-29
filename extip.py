import json
import datetime

'''=========================================
        read config data
============================================='''
cfgfile='extip.cfg'
cfg={'logfile':'',
     'ipfile':'curextip.json',
    'ipsource':{
        'ipifconfig':'https://ifconfig.me'
    }}

try:
    with open(cfgfile) as cf:
        cfg=json.load(cf)
except:
    print("Error open cfg file:",cfgfile)
    print("Use default settings!")
    print("Save default settings to ",cfgfile)
    try:
        with open(cfgfile,'w') as cf:
            json.dump(cfg,cf)
    except:
        print("Error write cfg file:",cfgfile)
        raise


'''=======================================
        log function
==========================================='''  
def logwrite(message,dt=True):
    if bool(cfg["logfile"]):
        try:
            with open(cfg["logfile"],'a') as lf:
                if dt: print(datetime.datetime.now().strftime('%d-%m-%Y  %H:%M:%S'),file=lf)
                print(message,file=lf)
        except:
            print("Error open log file:",cfg["logfile"])
            print(message) 
    else:
        print(message)
        
logwrite("Start...")        

import requests

curip={}
try:
    with open(cfg['ipfile']) as f:
        curip=json.load(f)
        logwrite("Load "+cfg['ipfile']) 
except:
    logwrite("Error load "+cfg['ipfile']) 
    print("Error open file:",cfg['ipfile'])
    print('Use empty current ip table!')

getip={}
for k,v in cfg['ipsource'].items():
    logwrite("Request to "+v)  
    try:    
        getip[k]=requests.get(v).text
        logwrite('Ok',False)
    except Exception as e:
        logwrite('Error \n'+str(e),False)
        getip[k]='error'
    
if curip!=getip :
    logwrite("Update file "+cfg['ipfile'])
    try:
        with open(cfg['ipfile'],'w') as f:
            json.dump(getip,f)
            logwrite('Ok',False)
    except:
        logwrite('Error'+str(e),False)
        