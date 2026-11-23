from playwright.sync_api import sync_playwright
from pathlib import Path
R=Path(__file__).resolve().parent
html=(R/'j4_cross_modal_review_board_v4_0.html').read_text()
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for label,viewport in [('desktop',{'width':1280,'height':900}),('mobile',{'width':390,'height':844})]:
  page=browser.new_page(viewport=viewport,accept_downloads=True)
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.set_content(html,wait_until='domcontentloaded')
  assert page.locator('#arc option').count()==3
  assert page.locator('#condition option').count()==4
  assert 'REHEARSAL_ONLY' in page.locator('#status').inner_text()
  page.select_option('#arc','R3_PAPER')
  page.select_option('#condition','V1A1')
  assert 'R3_PAPER_V1A1_reveal.mp4' in page.locator('#revealName').inner_text()
  page.locator('#reviewMode').uncheck()
  assert page.locator('#arc').is_disabled()
  assert '測試片段' in page.locator('#arc option').first.inner_text()
  assert 'R3_PAPER' not in page.locator('#revealName').inner_text()
  assert '這段影像' in page.locator('#promptBox').inner_text()
  assert not page.locator('#originFile').is_visible()
  page.fill('#answer','這是一個建造的物件。')
  page.click('#saveStage')
  page.click('#stage2')
  page.fill('#answer','後來顯示更大的物件。')
  page.click('#saveStage')
  page.click('#stage3')
  page.fill('#answer','我更關心材質與工作方式。')
  page.click('#saveStage')
  with page.expect_download() as dl:
   page.click('#export')
  d=dl.value
  path=R/f'_smoke_{label}.json'
  d.save_as(str(path))
  import json
  data=json.loads(path.read_text())
  assert data['status']=='REHEARSAL_ONLY'
  assert data['arc']=='R3_PAPER' and data['condition']=='V1A1'
  assert set(data['answers'])=={'1','2','3'}
  page.screenshot(path=str(R/f'ui_smoke_{label}.png'),full_page=True)
  if label=='mobile':
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), 'Mobile horizontal overflow'
  print('UI_PASS',label,'3 arcs,4 conditions, blinded participant mode, staged answers, rehearsal export')
  page.close()
 browser.close()
assert not errors, errors
