import json,sys,time
from playwright.sync_api import sync_playwright
B='http://127.0.0.1:8765/';OUT='/workspace/j4-evidence/'
res={}
def items_count(p):
    return p.locator('#item-list > *').count()
def ensure_menu(p):
    if p.locator('#menu-toggle').is_visible() and not p.evaluate("()=>document.getElementById('sidebar').classList.contains('open')"):
        p.click('#menu-toggle');p.wait_for_timeout(400)
def click_tab(p,t):
    ensure_menu(p)
    p.click(f'#nav-tabs button[data-tab="{t}"]',force=True);p.wait_for_timeout(500)
def open_item(p,text):
    ensure_menu(p)
    p.fill('#item-search',text);p.wait_for_timeout(400)
    ensure_menu(p)
    p.locator('#item-list > *').first.click(force=True);p.wait_for_timeout(1200)
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
    for dev,vp in [('desktop',{'width':1440,'height':960}),('mobile',{'width':390,'height':844})]:
        r={};ctx=br.new_context(viewport=vp,is_mobile=(dev=='mobile'),has_touch=(dev=='mobile'));p=ctx.new_page()
        errs=[];p.on('pageerror',lambda e:errs.append(str(e)));p.on('console',lambda m:errs.append('console.'+m.type+': '+m.text) if m.type=='error' else None)
        p.goto(B);p.wait_for_timeout(2000)
        r['title']=p.title();r['meta']=p.inner_text('#project-meta')
        if dev=='mobile' and p.locator('#menu-toggle').is_visible(): r['menu_toggle_visible']=True
        r['counts']={t:p.inner_text('#count-'+t) for t in ['shot','resource','media','html','manager','test','all']}
        click_tab(p,'shot');r['shot_list']=items_count(p)
        r['timeline_blocks']=p.locator('#timeline > *').count()
        p.screenshot(path=OUT+f'{dev}_01_shot.png',full_page=False)
        click_tab(p,'manager');r['manager_list']=items_count(p);p.screenshot(path=OUT+f'{dev}_02_managers.png')
        click_tab(p,'media');open_item(p,'IMG_7835.mp4')
        v=p.locator('#preview-area video')
        r['video_present']=v.count()
        if v.count():
            p.evaluate("()=>{const v=document.querySelector('#preview-area video');v.muted=true;return v.play()}")
            p.wait_for_timeout(2500)
            r['video_after_play']=p.evaluate("()=>{const v=document.querySelector('#preview-area video');return {t:v.currentTime,paused:v.paused,rs:v.readyState,dur:v.duration,w:v.videoWidth,h:v.videoHeight,err:v.error&&v.error.code}}")
            p.evaluate("()=>document.querySelector('#preview-area video').pause()")
            p.evaluate("()=>{document.querySelector('#preview-area video').currentTime=42.0}");p.wait_for_timeout(2000)
            r['video_after_seek42']=p.evaluate("()=>{const v=document.querySelector('#preview-area video');return {t:v.currentTime,paused:v.paused,rs:v.readyState,seeking:v.seeking}}")
        p.screenshot(path=OUT+f'{dev}_03_video_seek.png')
        for name,key in [('IMG_7870.jpeg','image'),('j4_character_prop_bible.md','markdown'),('j4_shots.json','json'),('j4_qc_matrix.csv','csv')]:
            click_tab(p,'all');open_item(p,name)
            pa=p.locator('#preview-area')
            info={'img':pa.locator('img').count(),'table_rows':pa.locator('tr').count()+p.locator('#details-area tr').count(),'pre':pa.locator('pre').count(),'h':pa.locator('h1,h2,h3').count(),'text_len':len(pa.inner_text())}
            if info['img']: info['img_natural']=p.evaluate("()=>{const i=document.querySelector('#preview-area img');return [i.naturalWidth,i.naturalHeight,i.complete]}")
            r[key]=info;p.screenshot(path=OUT+f'{dev}_04_{key}.png')
        click_tab(p,'html');r['html_list']=items_count(p)
        ensure_menu(p);p.locator('#item-list > *').first.click(force=True);p.wait_for_timeout(2000)
        fr=p.locator('#preview-area iframe');r['html_iframe']=fr.count()
        if fr.count():
            r['iframe_sandbox']=fr.first.get_attribute('sandbox')
            try:r['iframe_text_len']=len(p.frame_locator('#preview-area iframe').locator('body').inner_text(timeout=4000))
            except Exception as e:r['iframe_text_len']='ERR '+str(e)[:120]
        p.screenshot(path=OUT+f'{dev}_05_history_html.png')
        # review persistence via UI on shot S05 (desktop) / S06 (mobile)
        click_tab(p,'shot');p.fill('#item-search','');p.wait_for_timeout(300)
        idx=4 if dev=='desktop' else 5
        ensure_menu(p);p.locator('#item-list > *').nth(idx).click(force=True);p.wait_for_timeout(800)
        target=p.inner_text('#item-name')
        if dev=='mobile' and p.locator('.inspector').count(): p.locator('.inspector').scroll_into_view_if_needed()
        p.fill('#reviewer','grok-bot-audit-ui');p.fill('#review-notes',f'UI probe {dev} 2026-11-22')
        p.click('.decision-buttons button[data-decision="DEFER"]',force=True);p.wait_for_timeout(1500)
        r['save_state_after_click']=p.inner_text('#save-state')
        p.reload();p.wait_for_timeout(2000);click_tab(p,'shot')
        ensure_menu(p);p.locator('#item-list > *').nth(idx).click(force=True);p.wait_for_timeout(800)
        r['review_target']=target;r['after_reload_state']=p.inner_text('#save-state');r['after_reload_notes']=p.input_value('#review-notes')
        p.screenshot(path=OUT+f'{dev}_06_review_persist.png')
        r['horizontal_overflow']=p.evaluate("()=>document.documentElement.scrollWidth>window.innerWidth")
        r['errors']=errs[:10];res[dev]=r;ctx.close()
    br.close()
print(json.dumps(res,ensure_ascii=False,indent=1))
