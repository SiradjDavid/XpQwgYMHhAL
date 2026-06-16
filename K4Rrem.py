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