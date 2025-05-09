import sys
Bte=False
Bto=open
BtX=open
Btz=True
Btf=print
BtS=input
BtI=Exception
Btw=exit
BtU=sys.argv
BtF=sys.exit 
import requests
BtD=requests.post
import os
BtP=os.remove
BtR=os.makedirs
BtO=os.path
from datetime import datetime,timedelta
BtV=datetime.now
Btm=datetime.fromtimestamp
from colorama import init,Fore,Style
import bcps
Bth=bcps.__version__
from bcps import cli
BtH=cli.main
init()
Btv="./key"
BtE=BtO.join(Btv,"key.txt")
def Btn(key,check_key=Bte):
    Btr={'resultText':key,'check_key':'true' if check_key else 'false'}
    Bts=BtD("https://www.mod-mon.com/bcsfe_pulse/checkKey.php",data=Btr)
    return Bts
if not BtO.exists(Btv):
    BtR(Btv)
if BtO.exists(BtE):
    BtA = BtO.getctime(BtE)
    Btb = Btm(BtA)
    if BtV() - Btb > timedelta(hours=24):
        BtP(BtE)
    else:
        with Bto(BtE, 'r') as BtX:
            BtJ = BtX.read().strip()
            Bts = Btn(BtJ, check_key=Btz)
            if Bts.status_code == 200:
                Btf("프로그램을 정상적으로 실행합니다.")
                BtH.Main().main()
                BtF(0)
            else:
                Btf(Bts.text)
                Btf("에러 001 : 작동이 안되면 \"쿠지티비\" 사이트에 문의")
                BtF(1)

BtC=BtS(f"\n{Fore.GREEN}구글에서 {Fore.RESET}{Fore.RED}\"쿠지티비\"{Fore.RESET}{Fore.GREEN}를 검색 해주세요!{Fore.RESET}\n{Fore.GREEN}또는 {Fore.RESET}{Fore.RED}\"www.mod-mon.com\"{Fore.RESET}{Fore.GREEN}으로 접속 해주세요!\n\n{Fore.RESET}{Fore.RED}\"쿠지티비\"{Fore.RESET}{Fore.GREEN}에서 발급받은 키를 붙여넣으세요:{Fore.RESET}\n")
Bts=Btn(BtC)
if Bts.status_code==200:
    Btf("키가 유효하며 프로그램을 실행합니다.")
    Bty=BtD("https://www.mod-mon.com/bcsfe_pulse/updateKey.php",data={'resultText':BtC}) 
    if Bty.status_code==200:
        if BtO.exists(BtE):
            BtP(BtE)
        try:
            with Bto(BtE,'w')as BtX:
                BtX.write(BtC)
        except BtI as e:
            Btf(f"에러 002 : 작동이 안되면 \"쿠지티비\" 사이트에 문의")
            BtF(1)
    else:
        Btf("에러 003 : 작동이 안되면 \"쿠지티비\" 사이트에 문의")
        BtF(1)
else:
    
    Btf(f"\n {Bts}")
    Btf(f"\n{Fore.GREEN}키가 틀렸거나 이미 사용되었습니다.\n{Fore.RED}\"쿠지티비\"{Fore.RESET} {Fore.GREEN}사이트에서 {Fore.RED}키{Fore.RESET}{Fore.GREEN}를 재발급 받으세요.{Fore.RESET}")
    BtF(1)
BtH.Main().main()
Btq=BtU[1:]
for BtK in Btq:
    if BtK.lower()in["--version","-v"]:
        Btf(Bth)
        Btw()
