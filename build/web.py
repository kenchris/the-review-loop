#!/usr/bin/env python
"""Writes web/: the deck as a self-contained web page (open web/index.html, or serve the folder).
Slides are the same HTML the PDF and PowerPoint are rendered from, shown in a scaled player.
On a phone: a full screen button that also asks for landscape, a hint to turn the phone, tap or swipe to move,
and a tap on a video plays it full screen. On a computer: arrows, space, Tab, F (full screen), G (overview), V (video)."""
import glob, io, json, os, re, shutil, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'build', 'html')
OUT = os.path.join(ROOT, 'web')
LF = chr(10)
TITLE = 'The review loop'
BUILD = time.strftime('%Y%m%d%H%M%S')   # added to the slide and script addresses so a phone does not keep an old cached copy

PLAYER = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>__TITLE__</title>
<meta name="theme-color" content="#05080F">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-180.png">
<style>
 html,body{margin:0;width:100%;height:100%;background:#05080F;color:#C9D3E8;font-family:"Segoe UI",system-ui,sans-serif;overflow:hidden;overscroll-behavior:none;touch-action:manipulation;-webkit-tap-highlight-color:transparent}
 html,body{position:fixed;inset:0;touch-action:none}
 /* nothing on the page can be selected or dragged, and a long press shows no menu */
 *{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-user-drag:none}
 /* the slide is 1920 wide: it lives in a clipped box so it can never make the page wider than the screen */
 #wrap{position:fixed;inset:0;overflow:hidden;contain:strict}
 #stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;background:#0B1020}
 #stage iframe{position:absolute;inset:0;width:1920px;height:1080px;border:0;background:#0B1020}
 #hit{position:fixed;inset:0;z-index:3;display:none;touch-action:none;background:transparent}
 body.coarse #hit{display:block}
 body.overview #hit{display:none}
 #bar{position:fixed;left:0;right:0;bottom:0;height:4px;background:#121A33}
 #bar i{display:block;height:100%;width:0;background:#3DD9FF;transition:width .2s}
 #hud{position:fixed;right:max(14px,env(safe-area-inset-right));bottom:max(12px,env(safe-area-inset-bottom));font-size:14px;opacity:0;transition:opacity .3s;background:rgba(5,8,15,.8);padding:6px 10px;border-radius:8px;pointer-events:none}
 body.show #hud{opacity:1}
 #ui{position:fixed;top:max(8px,env(safe-area-inset-top));right:max(8px,env(safe-area-inset-right));display:flex;gap:8px;z-index:5;transition:opacity .25s}
 #ui button:not(#b-menu){display:none}
 body.ui #ui button:not(#b-menu),body.overview #ui button:not(#b-menu){display:inline-block}
 #b-menu{opacity:.5;font-size:22px;line-height:1;letter-spacing:1px}
 body.ui #b-menu,body.overview #b-menu{opacity:1}
 body:not(.coarse):not(.ui):not(.overview) #ui{opacity:0;pointer-events:none}
 #ui button,#rot button{font:600 15px "Segoe UI",system-ui,sans-serif;color:#E6ECF8;background:rgba(18,26,51,.88);border:1px solid #2D3B66;border-radius:12px;min-width:44px;height:44px;padding:0 14px;cursor:pointer}
 #ui button:active,#rot button:active{background:#2D3B66}
 #ui svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;vertical-align:middle}
 #rot{position:fixed;inset:0;display:none;flex-direction:column;align-items:center;justify-content:center;gap:18px;background:#05080F;z-index:9;text-align:center;padding:24px;box-sizing:border-box}
 #rot.on{display:flex}
 #rot h1{font-size:22px;font-weight:600;margin:0;color:#E6ECF8}
 #rot p{margin:0;font-size:15px;color:#9FB2D8;max-width:22em;line-height:1.4}
 #rot .row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
 #rot svg{width:88px;height:88px;stroke:#3DD9FF;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;animation:turn 2.6s ease-in-out infinite}
 @keyframes turn{0%,20%{transform:rotate(0)}60%,100%{transform:rotate(-90deg)}}
 #dbg{position:fixed;left:8px;bottom:8px;max-width:70vw;font:12px/1.3 ui-monospace,Consolas,monospace;color:#8CF0B8;background:rgba(5,8,15,.85);padding:4px 8px;border-radius:6px;z-index:20;pointer-events:none;display:none}
 #note{position:fixed;left:50%;bottom:max(24px,env(safe-area-inset-bottom));transform:translateX(-50%);max-width:80vw;background:rgba(18,26,51,.95);border:1px solid #2D3B66;border-radius:12px;padding:10px 16px;font-size:14px;opacity:0;pointer-events:none;transition:opacity .25s;z-index:8;text-align:center}
 #note.on{opacity:1}
 #grid{position:fixed;inset:0;background:#05080F;overflow:auto;display:none;padding:24px;box-sizing:border-box}
 body.overview #grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(320px,100%),1fr));gap:18px;padding-top:68px}
 body.overview #wrap{display:none}
 .th{position:relative;aspect-ratio:16/9;overflow:hidden;border-radius:10px;box-shadow:0 0 0 2px #24304F;cursor:pointer;background:#0B1020}
 .th.cur{box-shadow:0 0 0 3px #3DD9FF}
 .th iframe{position:absolute;left:0;top:0;width:1920px;height:1080px;border:0;transform-origin:0 0;pointer-events:none}
 .th b{position:absolute;right:8px;bottom:6px;font-size:13px;background:rgba(5,8,15,.8);padding:2px 7px;border-radius:6px}
</style></head><body>
<div id="wrap"><div id="stage"><iframe id="f" title="slide" allow="fullscreen" allowfullscreen></iframe></div></div>
<div id="grid"></div>
<div id="hit"></div>
<div id="bar"><i id="p"></i></div>
<div id="hud"></div>
<div id="ui">
 <button id="b-prev" aria-label="Previous slide">&#8249;</button>
 <button id="b-next" aria-label="Next slide">&#8250;</button>
 <button id="b-grid" aria-label="All slides"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg></button>
 <button id="b-fs" aria-label="Full screen"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button>
 <button id="b-menu" aria-label="Menu">&#8943;</button>
</div>
<div id="rot"><svg viewBox="0 0 24 24"><rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/></svg>
 <h1>Turn your phone sideways</h1><p>The slides are made for a wide screen. Turn the phone, or go full screen and it will turn by itself.</p>
 <div class="row"><button id="r-fs">Full screen</button><button id="r-go">Show anyway</button></div></div>
<div id="note"></div>
<div id="dbg"></div>
<script>
var N=__N__, cur=1, wrap=document.getElementById('wrap'), f=document.getElementById('f'), stage=document.getElementById('stage'), hud=document.getElementById('hud'), hudT, uiT, noteT, ignoreRot=false;
var coarse=window.matchMedia&&matchMedia('(pointer:coarse)').matches;
function pad(n){return (n<10?'0':'')+n}
function url(n){return 'html/auto/'+pad(n)+'.html?v=__V__'}
function size(){var vv=window.visualViewport;return [Math.round((vv&&vv.width)||wrap.clientWidth||innerWidth),Math.round((vv&&vv.height)||wrap.clientHeight||innerHeight)]}
function fit(){var d=size(),w=d[0],h=d[1],s=Math.min(w/1920,h/1080);
 stage.style.transform='translate('+((w-1920*s)/2)+'px,'+((h-1080*s)/2)+'px) scale('+s+')';checkRot();if(window.holes)holes()}
function checkRot(){var d=size(),portrait=d[1]>d[0]*1.1;
 document.getElementById('rot').classList.toggle('on',portrait&&coarse&&!ignoreRot&&!document.body.classList.contains('overview'))}
function note(t){var n=document.getElementById('note');n.textContent=t;n.classList.add('on');clearTimeout(noteT);noteT=setTimeout(function(){n.classList.remove('on')},4200)}
function ui(on){var b=document.body;if(on===undefined)on=!b.classList.contains('ui');b.classList.toggle('ui',on);clearTimeout(uiT);if(on)uiT=setTimeout(function(){b.classList.remove('ui')},3500)}
function show(n){cur=Math.max(1,Math.min(N,n));if(preEl&&preReady&&preN===cur)swapIn();else{dropPre();f.src=url(cur)}document.getElementById('p').style.width=(cur/N*100)+'%';
 history.replaceState(null,'','#'+cur);hud.textContent=cur+' / '+N;document.body.classList.add('show');clearTimeout(hudT);hudT=setTimeout(function(){document.body.classList.remove('show')},1500)}
function overview(on){var b=document.body,g=document.getElementById('grid');
 if(on===undefined)on=!b.classList.contains('overview');
 if(on){g.innerHTML='';for(var i=1;i<=N;i++){(function(i){var d=document.createElement('div');d.className='th'+(i==cur?' cur':'');
  var fr=document.createElement('iframe');fr.loading='lazy';fr.src=url(i);d.appendChild(fr);var l=document.createElement('b');l.textContent=i;d.appendChild(l);
  d.onclick=function(){overview(false);show(i)};g.appendChild(d)})(i)}
  b.classList.add('overview');checkRot();requestAnimationFrame(function(){var th=g.querySelector('.th');var s=th.clientWidth/1920;
   g.querySelectorAll('iframe').forEach(function(x){x.style.transform='scale('+s+')'});var c=g.querySelector('.cur');c&&c.scrollIntoView({block:'center'})})}
 else{b.classList.remove('overview');checkRot();fit()}}
function fsEl(){return document.fullscreenElement||document.webkitFullscreenElement}
function lockLandscape(){try{if(screen.orientation&&screen.orientation.lock)screen.orientation.lock('landscape').catch(function(){})}catch(x){}}
function enterFs(){var el=document.documentElement,rq=el.requestFullscreen||el.webkitRequestFullscreen;
 if(!rq){note('This browser has no full screen for web pages. On iPhone, use Share, then Add to Home Screen, and open it from there.');return}
 try{var r=rq.call(el);if(r&&r.then)r.then(lockLandscape,function(){note('Full screen was not allowed.')});else lockLandscape()}catch(x){note('Full screen was not allowed.')}}
function exitFs(){var ex=document.exitFullscreen||document.webkitExitFullscreen;if(ex)ex.call(document)}
function toggleFs(){fsEl()?exitFs():enterFs()}
function onFsChange(){if(!fsEl()){try{screen.orientation&&screen.orientation.unlock&&screen.orientation.unlock()}catch(x){}}setTimeout(fit,150)}
document.addEventListener('fullscreenchange',onFsChange);document.addEventListener('webkitfullscreenchange',onFsChange);
var pfs=false;
var DEBUG=/[?&]debug/.test(location.search),dbgEl=document.getElementById('dbg'),dbgN=0;
if(DEBUG)dbgEl.style.display='block';
function dbg(m){if(!DEBUG)return;dbgEl.textContent=(++dbgN)+' '+m}
var preEl=null,preReady=false,preN=0;
function dropPre(){if(preEl){preEl.remove();preEl=null}preReady=false}
// the next slide is loaded in a second frame underneath the current one; when it is time, that frame simply becomes the slide (no reload, no flash)
function preload(){if(cur>=N)return;dropPre();var p=document.createElement('iframe');p.title='slide';p.setAttribute('allow','fullscreen');p.setAttribute('allowfullscreen','');
 p.setAttribute('aria-hidden','true');preN=cur+1;p.addEventListener('load',function(){if(preEl===p)preReady=true});p.src=url(preN);stage.insertBefore(p,f);preEl=p;
 setTimeout(function(){if(preEl===p&&p!==f)dropPre()},8000)}
function swapIn(){var old=f;f=preEl;preEl=null;preReady=false;f.removeAttribute('aria-hidden');f.id='f';old.removeAttribute('id');old.remove();wireFrame(f);pfs=false;
 setTimeout(holes,100);setTimeout(holes,800);if(window.reviveHit)reviveHit()}
function wireFrame(fr){fr.addEventListener('load',function(){window.focus();pfs=false;setTimeout(holes,100);setTimeout(holes,800);if(window.reviveHit)reviveHit()})}
function videoCmd(){try{f.contentWindow.postMessage({cmd:'video'},'*')}catch(x){}}
function onKey(k,e,shift){
 if(document.body.classList.contains('overview')){if(k==='Escape'||k==='g'||k==='G')overview(false);return}
 if(pfs&&k==='Escape'){videoCmd();if(e)e.preventDefault();return}
 if(k==='Tab')show(cur+(shift?-1:1));
 else if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'||k==='ArrowDown')show(cur+1);
 else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'||k==='ArrowUp')show(cur-1);
 else if(k==='Home')show(1);else if(k==='End')show(N);
 else if(k==='f'||k==='F')toggleFs();
 else if(k==='v'||k==='V')videoCmd();
 else if(k==='g'||k==='G'||k==='Escape')overview();
 else return;if(e)e.preventDefault()}
addEventListener('keydown',function(e){if(e.ctrlKey||e.metaKey||e.altKey)return;onKey(e.key,e,e.shiftKey)});
addEventListener('click',function(e){if(pfs&&e.pointerType==='mouse')videoCmd()});
addEventListener('selectstart',function(e){e.preventDefault()});addEventListener('contextmenu',function(e){e.preventDefault()});addEventListener('dragstart',function(e){e.preventDefault()});
addEventListener('message',function(e){if(e.source!==f.contentWindow||!e.data)return;
 if(typeof e.data.k==='string')onKey(e.data.k,null,!!e.data.shift);else if(e.data.ui)ui();else if(e.data.dbg)dbg(e.data.dbg);else if(typeof e.data.pfs==='number')pfs=!!e.data.pfs;else if(e.data.preload)preload()});
document.getElementById('b-prev').onclick=function(){show(cur-1);ui(true)};
document.getElementById('b-next').onclick=function(){show(cur+1);ui(true)};
document.getElementById('b-grid').onclick=function(){overview()};
document.getElementById('b-fs').onclick=function(){toggleFs()};
document.getElementById('b-menu').onclick=function(){ui()};
if(coarse)document.body.classList.add('coarse');
else addEventListener('mousemove',function(){ui(true)});
// On a touch screen one transparent layer over the whole player takes every tap and swipe, so nothing depends on the slide
// document inside the frame (which is reloaded on each slide and was easy to lose after a video left full screen).
(function(){var hit=document.getElementById('hit'),sx,sy,t0=null,tx,ty,tt=null,lastAct=0;
 function onVideo(cx,cy){try{var m=stage.getBoundingClientRect(),s=m.width/1920,el=f.contentDocument.elementFromPoint((cx-m.left)/s,(cy-m.top)/s),v=el&&el.closest&&el.closest('video');
  if(v){if(f.contentWindow.__playFull){f.contentWindow.__playFull(v);return true}}}catch(x){}return false}
 function finish(dx,dy,dt,cx,cy,src){var now=Date.now();if(now-lastAct<300)return;
  if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)*1.3){lastAct=now;show(cur+(dx<0?1:-1));dbg('swipe '+(dx<0?'next':'back')+' ('+src+')');return}
  if(Math.abs(dx)>18||Math.abs(dy)>18){dbg('ignored: finger moved '+Math.round(Math.abs(dx))+','+Math.round(Math.abs(dy))+' px ('+src+')');return}
  if(dt>700){dbg('ignored: held '+dt+' ms ('+src+')');return}
  lastAct=now;var d=size();
  if(pfs){videoCmd();dbg('tap outside the video: close it');return}
  if(cy<Math.max(48,d[1]*0.1)){ui();dbg('tap top: buttons')}
  else if(onVideo(cx,cy)){dbg('tap video: play full screen')}
  else if(cx<d[0]*0.3){show(cur-1);dbg('tap left: back ('+src+')')}
  else{show(cur+1);dbg('tap: next ('+src+')')}}
 hit.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'||!e.isPrimary)return;sx=e.screenX;sy=e.screenY;t0=Date.now();dbg('down')},{passive:true});
 hit.addEventListener('pointercancel',function(){if(t0!==null)dbg('pointer cancelled by the browser');t0=null});
 hit.addEventListener('pointerup',function(e){if(e.pointerType==='mouse'||t0===null)return;var dt=Date.now()-t0;t0=null;finish(e.screenX-sx,e.screenY-sy,dt,e.clientX,e.clientY,'pointer')});
 hit.addEventListener('touchstart',function(e){if(e.touches.length!==1){tt=null;return}tx=e.touches[0].screenX;ty=e.touches[0].screenY;tt=Date.now()},{passive:true});
 hit.addEventListener('touchend',function(e){if(tt===null||!e.changedTouches.length)return;var c=e.changedTouches[0],dt=Date.now()-tt;tt=null;
  setTimeout(function(){finish(c.screenX-tx,c.screenY-ty,dt,c.clientX,c.clientY,'touch')},30)},{passive:true});
 // after full screen, a video, a call or a tab switch: forget any half-finished touch and make the browser find the layer again
 function revive(){t0=null;tt=null;hit.style.display='none';void hit.offsetHeight;hit.style.display='';dbg('ready')}
 document.addEventListener('visibilitychange',revive);addEventListener('focus',revive);addEventListener('pageshow',revive);
 document.addEventListener('fullscreenchange',function(){setTimeout(revive,200)});document.addEventListener('webkitfullscreenchange',function(){setTimeout(revive,200)});
 window.reviveHit=revive})();
// A tap on the video must reach the slide itself: only a tap that starts there counts as the touch that may start full screen.
// So the touch layer has a hole where the video is.
function holes(){var h=document.getElementById('hit');try{var v=f.contentDocument.querySelector('video.vvid');
 if(!v){h.style.clipPath='';return}
 var m=stage.getBoundingClientRect(),s=m.width/1920,r=v.getBoundingClientRect(),d=size(),
  x1=Math.round(m.left+r.left*s),y1=Math.round(m.top+r.top*s),x2=Math.round(m.left+r.right*s),y2=Math.round(m.top+r.bottom*s);
 h.style.clipPath='polygon(evenodd,0 0,'+d[0]+'px 0,'+d[0]+'px '+d[1]+'px,0 '+d[1]+'px,0 0,'+x1+'px '+y1+'px,'+x1+'px '+y2+'px,'+x2+'px '+y2+'px,'+x2+'px '+y1+'px,'+x1+'px '+y1+'px)'}catch(x){h.style.clipPath=''}}

document.getElementById('r-fs').onclick=function(){enterFs()};
document.getElementById('r-go').onclick=function(){ignoreRot=true;checkRot()};
wireFrame(f);
addEventListener('resize',fit);addEventListener('orientationchange',function(){setTimeout(fit,200)});
if(window.visualViewport)visualViewport.addEventListener('resize',fit);
fit();
show(parseInt(location.hash.slice(1))||1);
if(coarse)ui(true);
</script></body></html>
'''

FORWARD = LF + r"""// web player: the slide hands keys, taps and swipes to the player, and plays its video full screen on a tap
(function () {
  if (window.parent === window) return;
  var post = function (m) { window.parent.postMessage(m, '*'); };
  var coarse = window.matchMedia && matchMedia('(pointer:coarse)').matches;
  var sty = document.createElement('style');
  sty.textContent = 'html,body{touch-action:none;-webkit-tap-highlight-color:transparent}*{-webkit-user-select:none;user-select:none;-webkit-touch-callout:none;-webkit-user-drag:none}';
  document.head.appendChild(sty);
  var KEYS = ['ArrowRight','ArrowLeft','ArrowUp','ArrowDown','PageDown','PageUp','Home','End',' ','Enter','Backspace','Escape','f','F','g','G','v','V','Tab'];
  addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    if (pfs && e.key === 'Escape') { e.preventDefault(); toggleVideo(); return; }
    if (KEYS.indexOf(e.key) < 0) return;
    e.preventDefault(); post({ k: e.key, shift: e.shiftKey });
  });
  function fsEl() { return document.fullscreenElement || document.webkitFullscreenElement; }
  function lockLandscape() { try { if (screen.orientation && screen.orientation.lock) screen.orientation.lock('landscape').catch(function () {}); } catch (x) {} }
  // When the presentation itself is already full screen, the video fills the slide instead of asking for a second full screen,
  // so the presentation never leaves full screen. The player knows (pfs) and a tap outside the video closes it.
  var pfs = false, viaFull = false, warned = false;
  // half a second before the end the player loads the next slide out of sight, so it shows at once when the video is over
  document.addEventListener('timeupdate', function (e) {
    var v = e.target; if (!viaFull || !v || v.tagName !== 'VIDEO' || !(v.duration > 0)) return;
    if (v.duration - v.currentTime > 0.5) { warned = false; return; }
    if (!warned) { warned = true; post({ preload: 1 }); }
  }, true);
  var psty = document.createElement('style');
  psty.textContent = '.vvid.pfs{position:fixed!important;left:0!important;top:0!important;width:1920px!important;height:1080px!important;z-index:99999;border-radius:0!important;object-fit:contain;background:#000}';
  document.head.appendChild(psty);
  // full screen by the player's own button, or by the browser (F11, an installed app): the window then fills the whole screen
  function pageFs() {
    try {
      var w = window.parent, d = w.document;
      if (d.fullscreenElement || d.webkitFullscreenElement) return true;
      if (w.matchMedia && w.matchMedia('(display-mode: fullscreen)').matches) return true;
      return w.innerWidth >= screen.width - 1 && w.innerHeight >= screen.height - 1;
    } catch (x) { return false; }
  }
  function setPfs(v, on) { pfs = on; v.classList.toggle('pfs', on); post({ pfs: on ? 1 : 0 }); }
  function playFull(v) {
    if (!v) return false;
    viaFull = true;
    v.controls = true;
    if (pageFs()) { setPfs(v, true); var q = v.play(); if (q && q.catch) q.catch(function () {}); dbg('video fills the slide'); return true; }
    var p = v.play(); if (p && p.catch) p.catch(function () {});
    var alt = function (why) { dbg('full screen refused: ' + why); if (v.webkitEnterFullscreen) { try { v.webkitEnterFullscreen(); dbg('using the phone video player'); } catch (x) { dbg('no full screen possible: ' + x); } } };
    var rq = v.requestFullscreen || v.webkitRequestFullscreen;
    if (rq) { try { var r = rq.call(v); if (r && r.then) r.then(lockLandscape, function (err) { alt(err && err.message || err); }); else lockLandscape(); } catch (x) { alt(x); } }
    else alt('this browser has no full screen for a video element');
    return true;
  }
  window.__playFull = playFull;
  function toggleVideo() {
    var v = document.querySelector('video.vvid'); if (!v) return;
    if (pfs) { viaFull = false; v.pause(); setPfs(v, false); rewind(); }
    else if (fsEl()) { viaFull = false; (document.exitFullscreen || document.webkitExitFullscreen).call(document); v.pause(); }
    else playFull(v);
  }
  addEventListener('message', function (e) { if (e.data && e.data.cmd === 'video') toggleVideo(); });
  // when the video ends it leaves full screen by itself and the slide is back (the ended event does not bubble, so listen while capturing)
  document.addEventListener('ended', function (e) {
    if (e.target && e.target.tagName === 'VIDEO' && viaFull) { viaFull = false; post({ k: 'ArrowRight' }); }   // a video played full screen ends on the next slide (already loaded behind the scenes, see timeupdate)
    if (e.target && e.target.tagName === 'VIDEO' && pfs) { setPfs(e.target, false); return; }
    if (!e.target || e.target.tagName !== 'VIDEO' || !fsEl()) return;
    var ex = document.exitFullscreen || document.webkitExitFullscreen; if (ex) { try { var r = ex.call(document); if (r && r.catch) r.catch(function () {}); } catch (x) {} }
  }, true);
  function onFs() { if (!fsEl()) { viaFull = false; try { screen.orientation && screen.orientation.unlock && screen.orientation.unlock(); } catch (x) {} } }
  document.addEventListener('fullscreenchange', onFs); document.addEventListener('webkitfullscreenchange', onFs);
  // a tap on the video of a video slide plays it full screen (on a touch screen; with a mouse the video plays in place)
  // On a touch screen the video has no controls of its own while it sits in the slide (they would take the tap and only offer a small play button);
  // the tap starts it full screen, where the controls are on.
  function setControls() { var v = document.querySelector('video.vvid'); if (v) v.controls = !!fsEl() || pfs; }
  // when the video is over or full screen is left, show the first picture again (an ended video on a phone can come back blank)
  function rewind() {
    var v = document.querySelector('video.vvid'); if (!v) return;
    setTimeout(function () {
      if (fsEl() || pfs) return;
      try { v.pause(); v.currentTime = 0.01; } catch (x) {}
      v.style.display = 'none'; void v.offsetHeight; v.style.display = ''; setControls();
    }, 250);
  }
  document.addEventListener('ended', function (e) { if (e.target && e.target.tagName === 'VIDEO') rewind(); }, true);
  document.addEventListener('fullscreenchange', function () { if (!fsEl()) rewind(); });
  document.addEventListener('webkitfullscreenchange', function () { if (!fsEl()) rewind(); });
  document.addEventListener('webkitendfullscreen', rewind, true);
  setControls(); document.addEventListener('DOMContentLoaded', setControls); addEventListener('load', setControls); document.addEventListener('fullscreenchange', setControls); document.addEventListener('webkitfullscreenchange', setControls);
  var vx, vy, vt = 0, lastTouch = 0;
  document.addEventListener('pointerdown', function (e) { if (e.pointerType === 'touch') { vx = e.screenX; vy = e.screenY; vt = Date.now(); } }, true);
  document.addEventListener('pointerup', function (e) {
    if (e.pointerType !== 'touch' || fsEl() || pfs) return;
    lastTouch = Date.now();
    var v = e.target && e.target.closest && e.target.closest('video'); if (!v) return;
    if (Math.abs(e.screenX - vx) > 18 || Math.abs(e.screenY - vy) > 18 || Date.now() - vt > 700) return;
    playFull(v); dbg('tap video: full screen');
  }, true);
  document.addEventListener('click', function (e) {
    var v = e.target && e.target.closest && e.target.closest('video'); if (!v || fsEl() || pfs || Date.now() - lastTouch < 800) return;
    e.preventDefault(); e.stopPropagation(); playFull(v);
  }, true);
  // Taps and swipes on a touch screen: left third back, the rest forward, the top strip shows the buttons.
  // The slide is drawn about a third of its size on a phone, so how far a finger moved is measured in real screen
  // pixels (screenX, screenY), not in the slide's own pixels; touch-action none stops the browser taking a swipe as a scroll.
  // Both pointer events and touch events are listened to (some phone browsers are odd about one of them); a gesture is
  // acted on once. A selection or the long-press menu can no longer swallow taps. ?debug on the page address shows why a tap was ignored.
  function dbg(m) { post({ dbg: m }); }
  var lastAct = 0;
  function finish(dx, dy, dt, target, cx, cy, src) {
    var now = Date.now(); if (now - lastAct < 350) return;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.3) { lastAct = now; post({ k: dx < 0 ? 'ArrowRight' : 'ArrowLeft' }); dbg('swipe ' + (dx < 0 ? 'next' : 'back') + ' (' + src + ')'); return; }
    var why = null;
    if (Math.abs(dx) > 18 || Math.abs(dy) > 18) why = 'finger moved ' + Math.round(Math.abs(dx)) + ',' + Math.round(Math.abs(dy)) + ' px';
    else if (dt > 700) why = 'held ' + dt + ' ms';
    else if (target && target.closest && target.closest('video')) why = 'tap on the video';
    if (why) { dbg('ignored: ' + why + ' (' + src + ')'); return; }
    lastAct = now;
    if (cy < 110) { post({ ui: 1 }); dbg('tap top: buttons (' + src + ')'); }
    else if (cx < 576) { post({ k: 'ArrowLeft' }); dbg('tap left: back (' + src + ')'); }
    else { post({ k: 'ArrowRight' }); dbg('tap: next (' + src + ')'); }
  }
  var sx, sy, t0 = null, tx, ty, tt = null;
  addEventListener('pointerdown', function (e) { if (e.pointerType !== 'touch' || !e.isPrimary) return; sx = e.screenX; sy = e.screenY; t0 = Date.now(); }, { passive: true });
  addEventListener('pointercancel', function () { if (t0 !== null) dbg('pointer cancelled by the browser'); t0 = null; });
  addEventListener('pointerup', function (e) {
    if (e.pointerType !== 'touch' || t0 === null) return;
    var dt = Date.now() - t0, d0 = t0; t0 = null;
    finish(e.screenX - sx, e.screenY - sy, dt, e.target, e.clientX, e.clientY, 'pointer');
  });
  addEventListener('touchstart', function (e) { if (e.touches.length !== 1) { tt = null; return; } tx = e.touches[0].screenX; ty = e.touches[0].screenY; tt = Date.now(); }, { passive: true });
  addEventListener('touchend', function (e) {
    if (tt === null || !e.changedTouches.length) return;
    var c = e.changedTouches[0], dt = Date.now() - tt; tt = null;
    setTimeout(function () { finish(c.screenX - tx, c.screenY - ty, dt, e.target, c.clientX, c.clientY, 'touch'); }, 30);   // after the pointer events, which win
  }, { passive: true });
  function reset() { t0 = null; tt = null; }
  addEventListener('blur', reset); document.addEventListener('visibilitychange', reset);
  document.addEventListener('contextmenu', function (e) { e.preventDefault(); });
  document.addEventListener('selectstart', function (e) { e.preventDefault(); });
  document.addEventListener('dragstart', function (e) { e.preventDefault(); });
})();
"""

MANIFEST = {
    'name': TITLE, 'short_name': 'Web after AI', 'start_url': './', 'scope': './',
    'display': 'fullscreen', 'display_override': ['fullscreen', 'standalone'], 'orientation': 'landscape',
    'background_color': '#05080F', 'theme_color': '#05080F',
    'icons': [{'src': 'icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any'},
              {'src': 'icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}],
}


def make_icons(folder):
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(folder, exist_ok=True)
    for size in (180, 192, 512):
        img = Image.new('RGB', (size, size), (11, 16, 32))
        d = ImageDraw.Draw(img)
        pad = size * 0.14
        d.rounded_rectangle([pad, pad, size - pad, size - pad], radius=size * 0.18, outline=(61, 217, 255), width=max(3, size // 40))
        try:
            font = ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf', int(size * 0.46))
        except Exception:
            font = ImageFont.load_default()
        d.text((size / 2, size / 2), 'W', font=font, fill=(230, 236, 248), anchor='mm')
        img.save(os.path.join(folder, 'icon-%d.png' % size))


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'html', 'auto'))
    for name in ('base.css', 'templates.css', 'diagram.css', 'base.js', 'web-graph.js'):
        shutil.copy(os.path.join(SRC, name), os.path.join(OUT, 'html', name))
    with io.open(os.path.join(OUT, 'html', 'base.js'), 'a', encoding='utf8', newline=LF) as f:
        f.write(FORWARD)
    pages = sorted(glob.glob(os.path.join(SRC, 'auto', '*.html')))
    for p in pages:
        t = io.open(p, encoding='utf8').read().replace('../../../assets/', '../../assets/')
        t = re.sub(r'("\.\./(?:base|templates|diagram)\.(?:css|js))"', lambda m: m.group(1) + '?v=' + BUILD + '"', t)
        mv = re.search(r'data-video="([^"]+)"', t)
        if mv and os.path.exists(os.path.join(ROOT, 'videos', mv.group(1))):
            t = t.replace('<div class="vplay"></div>', '<video class="vvid" src="../../videos/%s" controls playsinline preload="metadata"></video>' % mv.group(1))
            t = t.replace('</head>', '<style>.vframe .vvid{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;border-radius:28px;background:#000}</style></head>')
        io.open(os.path.join(OUT, 'html', 'auto', os.path.basename(p)), 'w', encoding='utf8', newline=LF).write(t)
    for sub in ('screenshots', 'videos'):
        d = os.path.join(ROOT, 'assets', sub)
        if os.path.isdir(d):
            shutil.copytree(d, os.path.join(OUT, 'assets', sub))
    # Only the clips a slide names; never the raw recordings in videos/raw.
    used = set()
    for p in glob.glob(os.path.join(OUT, 'html', 'auto', '*.html')):
        used.update(re.findall(r'data-video="([^"]+)"', io.open(p, encoding='utf8').read()))
    vd = os.path.join(ROOT, 'videos')
    os.makedirs(os.path.join(OUT, 'videos'), exist_ok=True)
    for name in sorted(used):
        src = os.path.join(vd, name)
        if name and os.path.isfile(src):
            shutil.copy(src, os.path.join(OUT, 'videos', name))
    make_icons(os.path.join(OUT, 'icons'))
    io.open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf8', newline=LF).write(json.dumps(MANIFEST, indent=1))
    io.open(os.path.join(OUT, 'index.html'), 'w', encoding='utf8', newline=LF).write(
        PLAYER.replace('__N__', str(len(pages))).replace('__TITLE__', TITLE).replace('__V__', BUILD))
    print('wrote web/ with', len(pages), 'slides; open web/index.html')
main()
