from pathlib import Path
from playwright.sync_api import sync_playwright
p=Path('/mnt/data/j4_museum_v3_5/j4_g2a_previs_board_v3_5.html')
html=p.read_text(encoding='utf-8')
logs=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':800},accept_downloads=True)
 page.on('pageerror',lambda err: logs.append(str(err)))
 page.set_content(html,wait_until='domcontentloaded')
 assert page.locator('#tabs button').count()==3
 assert page.locator('#leftsvg svg').count()==1
 assert page.locator('#rightsvg svg').count()==1
 assert 'S10' in page.locator('#leftlabel').inner_text()
 page.locator('#timeline').fill('90')
 assert '90%' in page.locator('#timeReadout').inner_text()
 page.locator('#condition').select_option('control')
 assert '負對照' in page.locator('#timeReadout').inner_text()
 page.locator('#tabs button').nth(1).click()
 assert 'S11' in page.locator('#leftlabel').inner_text()
 page.locator('#tabs button').nth(2).click()
 assert 'S18' in page.locator('#leftlabel').inner_text()
 page.locator('#condition').select_option('main')
 page.locator('#timeline').fill('50')
 assert page.locator('#leftsvg svg').count()==1
 page.locator('#note').fill('導演測試：仍為示意')
 with page.expect_download() as dl:
  page.locator('#export').click()
 download=dl.value
 assert download.suggested_filename=='j4_g2a_v3_5_director_draft.json'
 page.screenshot(path='/mnt/data/j4_museum_v3_5/ui_smoke_desktop.png',full_page=True)
 mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 mobile.on('pageerror',lambda err: logs.append(str(err)))
 mobile.set_content(html,wait_until='domcontentloaded')
 assert mobile.locator('#tabs button').count()==3
 assert mobile.locator('#leftsvg svg').count()==1
 mobile.screenshot(path='/mnt/data/j4_museum_v3_5/ui_smoke_mobile.png',full_page=True)
 browser.close()
assert not logs,logs
print('PASS desktop/mobile: 3 arcs; A/B SVG render; control toggle; timeline; local JSON download; zero page errors')
