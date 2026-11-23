#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
html=(P/'j4_g2a_prereg_board_v3_6.html').read_text()
errs=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':800},accept_downloads=True)
 page.on('pageerror',lambda e:errs.append(str(e)))
 page.set_content(html,wait_until='domcontentloaded')
 assert page.locator('#tabs button').count()==3
 assert page.locator('#a_visual svg').count()==1 and page.locator('#b_visual svg').count()==1
 assert 'S10' in page.locator('#a_title').inner_text()
 assert 'S21' in page.locator('#b_title').inner_text()
 page.locator('#condition').select_option('control')
 assert '負對照' in page.locator('#b_title').inner_text()
 page.locator('#device').select_option('1080')
 assert '58 ×' in page.locator('#roi').inner_text()
 page.locator('#tabs button').nth(1).click()
 assert 'S22' in page.locator('#b_title').inner_text()
 page.locator('#tabs button').nth(2).click()
 assert 'S19' in page.locator('#b_title').inner_text()
 page.locator('#notes').fill('G1: 對照僅改目標線索，尚未簽核。')
 with page.expect_download() as di:page.locator('#export').click()
 assert di.value.suggested_filename=='j4_v3_6_director_draft.json'
 page.screenshot(path=str(P/'g2a_v3_6_desktop_smoketest.png'),full_page=True)
 mobile=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 mobile.on('pageerror',lambda e:errs.append(str(e)))
 mobile.set_content(html,wait_until='domcontentloaded')
 assert mobile.locator('#tabs button').count()==3
 mobile.locator('#tabs button').nth(1).click()
 assert mobile.locator('#a_visual svg').count()==1
 mobile.screenshot(path=str(P/'g2a_v3_6_mobile_smoketest.png'),full_page=True)
 browser.close()
assert not errs,errs
print('PASS_UI_DESKTOP_MOBILE: 3 arcs; condition toggle; device ROI; note export; no runtime exceptions')
