"""Deterministic Playwright smoke test inspired by medium-compiler review skill.

This uses source-correct isolated fixture data; no network navigation, no private
media, no actual platform-generation calls. Real HTTP playback is covered by
`test_review_web.py` and independently exercised with private local cache.
"""
from pathlib import Path
import json
import tempfile
import sys
import os
import hashlib
import struct
import zlib
from studio_factory.art_contracts import load_contract, compile_shot
BASE=Path(__file__).resolve().parents[1]
ROOT=(BASE/'review_site') if (BASE/'review_site').is_dir() else (BASE/'studio_factory'/'review_site')
sys.path.insert(0,str(ROOT.parent.parent))
from studio_factory.review_web import Catalog


def exercise(outdir:Path):
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as d:
        folder=Path(d)
        assets=folder/'asset-root'/'files'
        assets.mkdir(parents=True)
        (assets/'demo.mp4').write_bytes(b'video-fixture-not-for-decoding')
        (assets/'test-review.html').write_text('<h1>Test fixture</h1>',encoding='utf-8')
        (assets/'README.md').write_text('## Hello World\nSource markdown',encoding='utf-8')
        project=folder/'project'/'projects'/'j4-async-succession'/'archive'/'v2_6'
        project.mkdir(parents=True)
        shots={'shots':[{'id':f'S{i:02}','start_ms':(i-1)*3600,'end_ms':i*3600,
            'duration_ms':3600,'title_zh':f'Shot {i}','title_en':'Example',
            'act':1,'art_reference':{'artist':'Method','work':'Original'},
            'image_prompt':'Image original','motion_prompt':'Camera locked',
            'sound_prompt':'Original room tone','props':[],'characters':[]} for i in range(1,26)]}
        (project/'j4_shots.json').write_text(json.dumps(shots),encoding='utf-8')
        # One fully hash-bound synthetic 1-pixel image fixture. This is NOT
        # real generated J4 art, not a provider run, and not an artistic PASS.
        def png_chunk(tag,body):
            return (struct.pack(">I",len(body))+tag+body
                    +struct.pack(">I",zlib.crc32(tag+body)))
        img=(b"\x89PNG\r\n\x1a\n"
             +png_chunk(b"IHDR",struct.pack(">IIBBBBB",1,1,8,6,0,0,0))
             +png_chunk(b"IDAT",zlib.compress(b"\x00\x20\x40\x60\xff"))
             +png_chunk(b"IEND",b""))
        asset_root=folder/'asset-root'
        photo=asset_root/'extra'/'candidates'/'G2-smoke.png'
        photo.parent.mkdir(parents=True)
        photo.write_bytes(img)
        digest=hashlib.sha256(img).hexdigest()
        art_registry=load_contract(BASE.parent)
        compiled=compile_shot(art_registry,'S14')
        receipt={
          'schema':'studio.generation-receipt.v2','project':'j4-async-succession',
          'candidate_id':'G2-smoke','shot_id':'S14','producer':'synthetic-producer',
          'provider':'SYNTHETIC_TEST_ONLY','provider_run_id':'test-no-real-model',
          'model':'test-image','model_version':'0','generated_at':'2026-11-23T00:00:00Z',
          'seed':0,'settings':{'aspect_ratio':'9:16'},'credits':0,
          'sent_prompt':compiled['prompt'],
          'sent_negative_prompt':compiled['global_negative_prompt'],
          'compiled_payload_sha256':compiled['payload_sha256'],
          'generation_gate_at_time':'EXTERNALLY_APPROVED',
          'authorization_evidence':{'owner':'fixture','director_estimate':'fixture',
                'account_balance':'fixture','rights':'fixture'},
          'reference_assets':[],
          'output':{'relative_path':'extra/candidates/G2-smoke.png',
                    'media_type':'still','sha256':digest}
        }
        receipt_dir=asset_root/'extra'/'g2_receipts'
        receipt_dir.mkdir()
        (receipt_dir/'G2-smoke.json').write_text(json.dumps(receipt))
        reviews_dir=asset_root/'extra'/'g2_reviews'/'G2-smoke'
        reviews_dir.mkdir(parents=True)
        shot_profile=next(x for x in art_registry['contract']['shots'] if x['shot_id']=='S14')
        observations={c['id']:{'observed':c['polarity']=='must_exist',
                    'media_sha256':digest,'full_frame':True,'frame_at_ms':0,
                    'evidence_note':'synthetic independent reviewer for browser fixture'}
                    for c in shot_profile['checks'] if c['modality']=='still'}
        for reviewer in ('fixture-reviewer-1','fixture-reviewer-2'):
            payload={'schema':'studio.g2-review.v2','candidate_id':'G2-smoke',
                     'shot_id':'S14','reviewer_id':reviewer,
                     'media_sha256':digest,
                     'compiled_payload_sha256':compiled['payload_sha256'],
                     'observations':observations}
            (reviews_dir/(reviewer+'.json')).write_text(json.dumps(payload))
        # Read actual source-locked J4 IR/contracts; retain isolated fixture media.
        catalog=Catalog(folder/'asset-root',BASE.parent,folder/'review.sqlite3')
        data=catalog.public();data['csrf']='test-ephemeral'
        pagehtml=(ROOT/'index.html').read_text(encoding='utf-8')
        pagehtml=pagehtml.replace('<link rel="stylesheet" href="/style.css">',
            '<style>'+(ROOT/'style.css').read_text(encoding='utf-8')+'</style>')
        pagehtml=pagehtml.replace('<script src="/app.js" defer></script>','')
        javascript=(ROOT/'app.js').read_text(encoding='utf-8')
        outdir.mkdir(parents=True,exist_ok=True)
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_BIN') or None,args=['--no-sandbox'])
            for width,height,device in [(1440,960,'desktop'),(390,844,'mobile')]:
                page=browser.new_page(viewport={'width':width,'height':height})
                page.set_content(pagehtml)
                page.evaluate("""data=>{
                  Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:()=>null,setItem:()=>{}}});
                  const reviews={}; window.fetch=async(input,opts={})=>{
                    const url=String(input);
                    if(url==='/api/bootstrap')return new Response(JSON.stringify(data),{status:200});
                    if(url==='/api/review'){
                      const obj=JSON.parse(opts.body);const review={...obj,timestamp:'test-time'};
                      reviews[review.item_id]=review;return new Response(JSON.stringify(review),{status:200});
                    }
                    if(url.startsWith('/api/media/'))return new Response('# fixture', {status:200});
                    if(url==='/api/tests/run')return new Response(JSON.stringify({state:'PASS'}),{status:200});
                    throw Error('unknown mock endpoint '+url)
                  }
                }""",data)
                errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.add_script_tag(content=javascript)
                page.wait_for_function("document.querySelector('#item-name').textContent.includes('S01')")
                assert page.locator('.item-row').count()==25
                if device=='desktop':
                    page.locator('button[data-decision="PASS"]').click()
                    page.wait_for_function("document.querySelector('#save-state').textContent.includes('PASS')")
                    page.locator('#next-item').click()
                    assert 'S02' in page.locator('#item-name').inner_text()
                    page.locator('#prev-item').click()
                    assert page.locator('.decision-buttons .pass.active').count()==1
                    page.locator('button[data-tab="media"]').click()
                    page.get_by_text('demo.mp4',exact=False).first.click()
                    assert page.locator('video[controls]').count()==1
                    page.locator('button[data-tab="html"]').click()
                    assert page.locator('iframe[sandbox="allow-scripts"]').count()==1
                    page.locator('button[data-tab="test"]').click()
                    page.locator('#run-verified-test').click()
                    page.wait_for_function("document.querySelector('#test-result').textContent.includes('PASS')")
                    page.locator('button[data-tab="art"]').click()
                    assert page.locator('.item-row').count()==6
                    assert 'S02' in page.locator('#item-name').inner_text()
                    assert 'REJECTED_BY_OBSERVATION' in page.locator('#details-area').inner_text() or 'REJECTED' in page.locator('#details-area').inner_text()
                    assert 'P0 semantic acceptance' in page.locator('#details-area').inner_text()
                    page.screenshot(path=str(outdir/'g2-art-desktop.png'),full_page=False)
                    page.locator('button[data-tab="candidate"]').click()
                    assert page.locator('.item-row').count()==1
                    assert 'G2-smoke' in page.locator('#item-name').inner_text()
                    assert page.locator('#preview-area img').count()==1
                    assert 'STATIC_REVIEW_COMPLETE_TEMPORAL_NOT_RUN' in page.locator('#preview-meta').inner_text()
                    page.screenshot(path=str(outdir/'g2-candidate-desktop.png'),full_page=False)
                    page.locator('#open-candidate-receipt').click()
                    assert page.locator('#item-kicker').inner_text()=='SOURCE ARTIFACT'
                    page.locator('button[data-tab="shot"]').click()
                else:
                    page.locator('#menu-toggle').click()
                    assert page.locator('#sidebar.open').count()==1
                    page.locator('.item-row').nth(1).click()
                    assert 'S02' in page.locator('#item-name').inner_text()
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
                    page.locator('#menu-toggle').click()
                    page.locator('button[data-tab="art"]').click()
                    assert page.locator('.item-row').count()==6
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
                    page.screenshot(path=str(outdir/'g2-art-mobile.png'),full_page=False)
                    page.locator('button[data-tab="candidate"]').click()
                    assert page.locator('.item-row').count()==1
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2')
                    page.screenshot(path=str(outdir/'g2-candidate-mobile.png'),full_page=False)
                page.screenshot(path=str(outdir/f'review-{device}.png'),full_page=False)
                assert not errors,errors
                page.close()
            browser.close()

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=Path('/tmp/j4-playwright-smoke'))
    args=p.parse_args();exercise(args.out)
    print('PASS: reviewed shot navigation, media controls, labels, notes, tests and responsive view')
