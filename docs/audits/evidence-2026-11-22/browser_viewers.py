import json
from playwright.sync_api import sync_playwright
B='http://127.0.0.1:8765/';OUT='/workspace/j4-evidence/'
def ensure_menu(p):
    if p.locator('#menu-toggle').is_visible() and not p.evaluate("()=>document.getElementById('sidebar').classList.contains('open')"):
        p.click('#menu-toggle');p.wait_for_timeout(400)
def tab(p,t):
    ensure_menu(p);p.fill('#item-search','');p.wait_for_timeout(200);ensure_menu(p);p.click(f'#nav-tabs button[data-tab="{t}"]');p.wait_for_timeout(500)
def pick(p,text):
    ensure_menu(p);p.fill('#item-search',text);p.wait_for_timeout(400);ensure_menu(p)
    rows=p.locator('#item-list > *');n=rows.count()
    for i in range(n):
        if text in rows.nth(i).inner_text(): rows.nth(i).click();break
    p.wait_for_timeout(1500)
res={}
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox'])
    for dev,vp in [('desktop',{'width':1440,'height':960}),('mobile',{'width':390,'height':844})]:
        r={};p=br.new_page(viewport=vp,is_mobile=dev=='mobile',has_touch=dev=='mobile');p.goto(B);p.wait_for_timeout(1500)
        for name,key in [('j4_character_prop_bible.md','markdown'),('j4_shots.json','json'),('j4_qc_matrix.csv','csv'),('j4_master_prompt_book.md','markdown2')]:
            tab(p,'all');pick(p,name)
            d=p.locator('#details-area')
            r[key]={'item':p.inner_text('#item-name'),'details_text_len':len(d.inner_text()),'h':d.locator('h1,h2,h3,h4').count(),'pre':d.locator('pre').count(),'tr':d.locator('tr').count(),'th':d.locator('th').count(),'script_tags_in_details':d.locator('script').count(),'snippet':d.inner_text()[:160]}
            p.screenshot(path=OUT+f'{dev}_07_{key}_details.png',full_page=True)
        tab(p,'html');r['html_list']=p.locator('#item-list > *').count();names=[]
        for i in range(min(3,r['html_list'])):
            ensure_menu(p);row=p.locator('#item-list > *').nth(i);names.append(row.inner_text().split('\n')[0]);row.click();p.wait_for_timeout(2500)
            fr=p.locator('#preview-area iframe')
            info={'iframe':fr.count()}
            if fr.count():
                info['sandbox']=fr.get_attribute('sandbox')
                try: info['body_text_len']=len(p.frame_locator('#preview-area iframe').locator('body').inner_text(timeout=5000))
                except Exception as e: info['body_text_len']='ERR '+str(e)[:100]
            r.setdefault('html_items',[]).append([names[-1],info])
            if i==0:p.screenshot(path=OUT+f'{dev}_05_history_html.png')
        tab(p,'test');r['test_list']=p.locator('#item-list > *').count()
        res[dev]=r;p.close()
    br.close()
print(json.dumps(res,ensure_ascii=False,indent=1))
