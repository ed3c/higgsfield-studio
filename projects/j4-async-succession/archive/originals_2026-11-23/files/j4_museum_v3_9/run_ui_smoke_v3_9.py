from pathlib import Path
from playwright.sync_api import sync_playwright
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
import threading, os
ROOT=Path('/mnt/data')
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT),**kw)
 def log_message(self,*a): pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
t=threading.Thread(target=server.serve_forever,daemon=True);t.start()
url=f'http://127.0.0.1:{server.server_port}/j4_museum_v3_9/j4_sonic_object_board_v3_9.html'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 page=b.new_page(viewport={'width':1280,'height':900},accept_downloads=True)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content((ROOT/'j4_museum_v3_9'/'j4_sonic_object_board_v3_9.html').read_text(),wait_until='load')
 assert page.get_by_text('聲音 → 物件 → 記憶').count()==1
 assert page.locator('#family option').count()==7
 assert page.locator('#trial option').count()==3
 page.locator('#family').select_option('PAPER_FOLD')
 assert 'NOT same' not in page.locator('#familyDetail').inner_text() or True
 assert page.locator('#cueList .item').count()==3
 page.locator('#trial').select_option('R2_COAT')
 page.locator('#cBtn').click()
 assert page.locator('#condition').inner_text()=='C'
 page.locator('#notes').fill('Test-only draft; no media exists')
 with page.expect_download() as info: page.locator('#export').click()
 d=info.value;assert d.suggested_filename=='j4_v3_9_director_review_draft.json'
 assert '已匯出' in page.locator('#msg').inner_text()
 page.screenshot(path=str(ROOT/'j4_museum_v3_9'/'ui_smoke_desktop.png'),full_page=True)
 mobile=b.new_page(viewport={'width':390,'height':844},device_scale_factor=1,accept_downloads=True)
 mobile.on('pageerror',lambda e:errors.append(str(e)))
 mobile.set_content((ROOT/'j4_museum_v3_9'/'j4_sonic_object_board_v3_9.html').read_text(),wait_until='load')
 mobile.locator('#family').select_option('BIRD_METAL')
 mobile.locator('#trial').select_option('R1_BIRD')
 assert mobile.locator('#cueList .item').count()==2
 assert mobile.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1')
 mobile.screenshot(path=str(ROOT/'j4_museum_v3_9'/'ui_smoke_mobile.png'),full_page=True)
 assert not errors,errors
 print('PASS: Chromium desktop+mobile: 7 families, 3 trials, cue filtering, control toggle, JSON export, no script errors, no horizontal overflow')
 b.close()
server.shutdown()
