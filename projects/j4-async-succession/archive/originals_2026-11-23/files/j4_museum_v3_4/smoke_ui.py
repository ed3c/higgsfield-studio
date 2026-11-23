from playwright.sync_api import sync_playwright
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import functools,threading
handler=functools.partial(SimpleHTTPRequestHandler,directory='/mnt/data/j4_museum_v3_4')
server=ThreadingHTTPServer(('127.0.0.1',0),handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
p=f'http://127.0.0.1:{server.server_port}/j4_g2a_viewer_lab_v3_4.html'
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True, executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 page=browser.new_page(viewport={'width':1100,'height':800},accept_downloads=True)
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(Path('/mnt/data/j4_museum_v3_4/j4_g2a_viewer_lab_v3_4.html').read_text(),wait_until='load')
 assert page.locator('#setup').is_visible()
 page.locator('#mode').select_option('REHEARSAL_ONLY')
 page.locator('#start').click()
 assert page.locator('#trial').is_visible()
 assert '第 1/3 組' in page.locator('#trial-number').inner_text()
 page.locator('#play').click()
 assert 'REHEARSAL' in page.locator('#clock').inner_text()
 page.screenshot(path='/mnt/data/j4_museum_v3_4/ui_rehearsal_smoke.png',full_page=True)
 # Faster JS timer preflight than waiting exact 1.3-4 s per exposure
 for i in range(15):
  if page.locator('#play').is_visible():
   page.evaluate("() => { if (currentTimer) { clearTimeout(currentTimer); currentTimer=null; } document.getElementById('next').disabled=false; }")
  if page.locator('#survey').is_visible():
   page.locator('#answer').fill('流程排練，沒有實際影像可判讀')
   if page.locator('#anchor-wrap').is_visible():page.locator('#anchor').fill('未看到任何物理線索，未載入媒體')
  page.locator('#next').click()
 assert page.locator('#finished').is_visible()
 with page.expect_download() as info:
  page.locator('#export').click()
 download=info.value
 filepath='/mnt/data/j4_museum_v3_4/rehearsal_test_result.json'
 download.save_as(filepath)
 import json
 x=json.loads(Path(filepath).read_text())
 assert x['mode']=='REHEARSAL_ONLY' and all(y['status']=='REHEARSAL_ONLY' and y['media_present']==False for y in x['trials'])
 assert x['observer_scores']=='NOT_RUN'
 assert not errors,errors
 print('PASS Browser: rehearsal without media; full 15-stage walkthrough; export statuses safe; page errors', errors)
 browser.close()
