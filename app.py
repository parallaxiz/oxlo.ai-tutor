import streamlit as st # type: ignore
import streamlit.components.v1 as components  # type: ignore
import html

def st_iframe(html_content, height, scrolling=True):
    srcdoc = html.escape(html_content, quote=True).replace('\n', '&#10;')
    scroll_attr = 'yes' if scrolling else 'no'
    st.markdown(f'<iframe srcdoc="{srcdoc}" sandbox="allow-scripts allow-top-navigation allow-same-origin allow-popups allow-popups-to-escape-sandbox" width="100%" height="{height}" style="border:none; padding:0; margin:0;" scrolling="{scroll_attr}"></iframe>', unsafe_allow_html=True)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Codexa — AI Coding Tutor", page_icon="⚡", layout="wide")

# ── Read page from URL query param (reliable cross-iframe navigation) ─────────
import os, re
os.makedirs("ui", exist_ok=True)
if not os.path.exists("ui/lab.html"):
    with open(__file__, "r", encoding="utf-8") as _f_in:
        _c = _f_in.read()
    _mh = re.search(r'HOME_HTML = """(<!DOCTYPE html>.*?</html>)"""', _c, re.DOTALL)
    if _mh: open("ui/home.html", "w", encoding="utf-8").write(_mh.group(1))
    _ms = re.search(r'SETUP_HTML = """(<!DOCTYPE html>.*?</html>)"""', _c, re.DOTALL)
    if _ms: open("ui/setup.html", "w", encoding="utf-8").write(_ms.group(1))
    _ml = re.search(r'LAB_HTML = """(<!DOCTYPE html>.*?</html>)"""', _c, re.DOTALL)
    if _ml: open("ui/lab.html", "w", encoding="utf-8").write(_ml.group(1))

params = st.query_params
current_page = params.get("page", "start")

# ── Global CSS: hide ALL Streamlit chrome, kill every scrollbar ───────────────
st.markdown("""
<style>
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer, #MainMenu { display: none !important; }

/* Zero out all padding/margin so the iframe fills the viewport */
[data-testid="stAppViewContainer"] > .main,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

/* Kill the outer Streamlit page scrollbar — the iframe manages its own scroll */
html, body {
    overflow: hidden !important;
    height: 100% !important;
}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═════════════════════════════════════════════════════════════════════════════
if current_page == "start":

    # The iframe navigates by changing window.parent.location.href
    # which updates the query param and triggers a Streamlit rerun
    HOME_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
div,span,main,nav,ul,li,a,button,h1,p,.pill,.code-chip,.stat,.feat,.nav-logo,.nav-badge{box-sizing:border-box;margin:0;padding:0}
html,body{
  background:#050508;color:#E8E8F0;
  font-family:'DM Sans',sans-serif;
  height:100%;overflow-y:auto;overflow-x:hidden;
}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:4px}

body::before{content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 70% 60% at 15% 10%,rgba(82,45,240,.22) 0,transparent 65%),
    radial-gradient(ellipse 55% 45% at 85% 85%,rgba(99,220,150,.12) 0,transparent 65%),
    radial-gradient(ellipse 40% 55% at 65% 5%,rgba(56,189,248,.09) 0,transparent 65%);
  pointer-events:none;z-index:0}

nav{position:fixed;top:0;left:0;right:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:16px 48px;
  background:rgba(5,5,8,.75);backdrop-filter:blur(24px);
  border-bottom:1px solid rgba(255,255,255,.06)}
.nav-logo{font-family:'Syne',sans-serif;font-weight:800;font-size:1.25rem;
  letter-spacing:-.03em;
  background:linear-gradient(135deg,#fff 0%,#7c3aed 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  display:flex;align-items:center;gap:6px}
.nav-logo-dot{display:inline-block;width:8px;height:8px;border-radius:50%;
  background:linear-gradient(135deg,#7c3aed,#34d399);margin-bottom:1px}
.nav-links{display:flex;gap:28px;list-style:none}
.nav-links a{color:rgba(232,232,240,.4);text-decoration:none;font-size:.85rem;transition:color .2s}
.nav-links a:hover{color:#E8E8F0}
.nav-badge{font-size:.7rem;font-weight:500;padding:5px 14px;border-radius:99px;
  border:1px solid rgba(52,211,153,.3);color:#34d399;background:rgba(52,211,153,.08);letter-spacing:.05em}

main{position:relative;z-index:1;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  min-height:100vh;padding:120px 24px 80px}

.pill{display:inline-flex;align-items:center;gap:8px;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
  border-radius:99px;padding:5px 16px 5px 7px;
  font-size:.76rem;color:rgba(232,232,240,.65);
  margin-bottom:44px;cursor:pointer;text-decoration:none;
  transition:border-color .2s,background .2s;animation:fadeUp .6s ease both}
.pill:hover{background:rgba(255,255,255,.08);border-color:rgba(52,211,153,.3)}
.pill-dot{width:22px;height:22px;border-radius:50%;
  background:linear-gradient(135deg,#7c3aed,#34d399);
  display:flex;align-items:center;justify-content:center;
  font-size:.65rem;color:#fff;flex-shrink:0;font-family:'JetBrains Mono',monospace}
.pill-arrow{color:rgba(232,232,240,.35);margin-left:2px;transition:transform .2s}
.pill:hover .pill-arrow{transform:translateX(3px)}

.hero{text-align:center;max-width:820px;margin-bottom:48px;animation:fadeUp .7s ease .1s both}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:.72rem;letter-spacing:.15em;
  color:#34d399;margin-bottom:20px;opacity:.85}
.eyebrow span{color:rgba(232,232,240,.3)}
h1{font-family:'Syne',sans-serif;
  font-size:clamp(2.8rem,6vw,5rem);font-weight:800;
  line-height:1.03;letter-spacing:-.035em;margin-bottom:24px;color:#fff}
h1 .accent{background:linear-gradient(135deg,#7c3aed 0%,#34d399 60%,#38bdf8 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.subtitle{font-size:1.05rem;font-weight:300;color:rgba(232,232,240,.45);
  line-height:1.75;max-width:500px;margin:0 auto}

.code-chip{font-family:'JetBrains Mono',monospace;font-size:.78rem;
  background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.25);
  border-radius:8px;padding:14px 20px;color:rgba(232,232,240,.55);
  margin-bottom:40px;line-height:1.6;max-width:420px;text-align:left;
  animation:fadeUp .7s ease .25s both}
.kw{color:#c084fc}.fn{color:#34d399}.str{color:#38bdf8}.cm{color:rgba(232,232,240,.25)}
.cursor{display:inline-block;width:2px;height:.9em;background:#34d399;
  margin-left:2px;animation:blink 1s step-end infinite;vertical-align:text-bottom}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;
  margin-bottom:72px;animation:fadeUp .7s ease .2s both}
.btn-primary{font-family:'DM Sans',sans-serif;font-size:.9rem;font-weight:500;
  padding:0 28px;height:48px;
  background:linear-gradient(135deg,#7c3aed,#5b21b6);
  color:#fff;border:none;border-radius:10px;cursor:pointer;
  box-shadow:0 0 30px rgba(124,58,237,.38),0 1px 3px rgba(0,0,0,.4);
  transition:all .25s ease;min-width:180px;letter-spacing:.01em;font-size:.9rem}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 0 52px rgba(124,58,237,.58),0 4px 20px rgba(0,0,0,.3)}
.btn-primary:active{transform:translateY(0)}
.btn-ghost{font-family:'DM Sans',sans-serif;font-size:.9rem;font-weight:400;
  padding:0 28px;height:48px;background:transparent;
  color:rgba(232,232,240,.5);border:1px solid rgba(255,255,255,.1);
  border-radius:10px;cursor:pointer;transition:all .25s ease;min-width:140px}
.btn-ghost:hover{background:rgba(255,255,255,.05);color:#E8E8F0;border-color:rgba(255,255,255,.2)}

.stats{display:flex;width:100%;max-width:700px;gap:1px;
  background:rgba(255,255,255,.06);border-radius:14px;overflow:hidden;
  border:1px solid rgba(255,255,255,.07);
  margin-bottom:72px;animation:fadeUp .7s ease .3s both}
.stat{flex:1;padding:22px 24px;background:#050508;text-align:center;position:relative}
.stat+.stat::before{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);
  width:1px;height:38%;background:rgba(255,255,255,.07)}
.stat-val{font-family:'Syne',sans-serif;font-size:1.35rem;font-weight:700;
  letter-spacing:-.02em;
  background:linear-gradient(135deg,#a78bfa,#34d399);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin-bottom:4px}
.stat-lbl{font-size:.68rem;color:rgba(232,232,240,.28);text-transform:uppercase;letter-spacing:.12em}

.features{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;
  max-width:900px;width:100%;margin-bottom:72px;animation:fadeUp .7s ease .4s both}
.feat{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.07);
  border-radius:14px;padding:26px 22px;position:relative;overflow:hidden;
  transition:border-color .3s,background .3s,transform .3s}
.feat::after{content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(52,211,153,.06) 0%,transparent 55%);
  opacity:0;transition:opacity .3s}
.feat:hover{border-color:rgba(52,211,153,.2);background:rgba(255,255,255,.045);transform:translateY(-3px)}
.feat:hover::after{opacity:1}
.feat-icon{width:38px;height:38px;border-radius:9px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.05rem;margin-bottom:14px;
  background:rgba(124,58,237,.13);border:1px solid rgba(124,58,237,.2);
  position:relative;z-index:1}
.feat-title{font-family:'Syne',sans-serif;font-size:.88rem;font-weight:700;
  color:#E8E8F0;margin-bottom:8px;position:relative;z-index:1}
.feat-desc{font-size:.79rem;font-weight:300;color:rgba(232,232,240,.36);
  line-height:1.65;position:relative;z-index:1}

.divider{width:100%;max-width:900px;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.07),transparent);margin-bottom:28px}
.footer{font-size:.7rem;color:rgba(232,232,240,.16);text-align:center;letter-spacing:.06em}
.footer a{color:rgba(52,211,153,.5);text-decoration:none}
.footer a:hover{color:#34d399}

@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
</style>
</head>
<body>
<nav>
  <div class="nav-logo"><span class="nav-logo-dot"></span>Codexa</div>
  <ul class="nav-links">
    <li><a href="#">Docs</a></li>
    <li><a href="#">Pricing</a></li>
    <li><a href="#">Blog</a></li>
  </ul>
  <div class="nav-badge">Beta Access</div>
</nav>

<main>
  <a class="pill" href="https://oxlo.ai" target="_blank">
    <div class="pill-dot">&lt;/&gt;</div>
    <span>Powered by Oxlo.ai · DeepSeek-R1 &amp; 33B Coder</span>
    <span class="pill-arrow">→</span>
  </a>

  <div class="hero">
    <div class="eyebrow"><span>// </span>AI-Powered Coding Education<span> //</span></div>
    <h1>Learn to code.<br><span class="accent">Think like a dev.</span></h1>
    <p class="subtitle">Codexa pairs frontier AI reasoning with a live coding lab — so every concept clicks, not just compiles.</p>
  </div>

  <div class="code-chip">
    <span class="cm"># Ask anything. Understand everything.</span><br>
    <span class="kw">def </span><span class="fn">solve</span>(problem):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;ai = <span class="fn">Codexa</span>(<span class="str">"DeepSeek-R1"</span>)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;<span class="kw">return</span> ai.<span class="fn">reason</span>(problem)<span class="cursor"></span>
  </div>

  <div class="cta-row">
    <button class="btn-primary" onclick="goToLab()">⚡ Open the Lab</button>
    <button class="btn-ghost" onclick="window.open('https://oxlo.ai','_blank')">Visit Oxlo.ai ↗</button>
  </div>

  <div class="stats">
    <div class="stat"><div class="stat-val">DeepSeek-R1</div><div class="stat-lbl">Reasoning Engine</div></div>
    <div class="stat"><div class="stat-val">33B</div><div class="stat-lbl">Coder Model</div></div>
    <div class="stat"><div class="stat-val">&lt;2s</div><div class="stat-lbl">Avg Response</div></div>
    <div class="stat"><div class="stat-val">Codexa</div><div class="stat-lbl">Platform</div></div>
  </div>

  <div class="features">
    <div class="feat"><div class="feat-icon">🧠</div>
      <div class="feat-title">Chain-of-Thought Reasoning</div>
      <div class="feat-desc">DeepSeek-R1 thinks through your problem step by step — no black-box answers.</div></div>
    <div class="feat"><div class="feat-icon">⚡</div>
      <div class="feat-title">Live Coding Lab</div>
      <div class="feat-desc">Monaco editor (same engine as VS Code) in the browser. Write, run, and get AI feedback instantly.</div></div>
    <div class="feat"><div class="feat-icon">🎯</div>
      <div class="feat-title">Concept-First Learning</div>
      <div class="feat-desc">Codexa teaches the mental model, not just the answer. You'll understand why, not just what.</div></div>
  </div>

  <div class="divider"></div>
  <div class="footer">© 2025 <a href="https://oxlo.ai" target="_blank">Oxlo.ai</a> · Codexa — Built for engineers who actually want to learn</div>
</main>

<script>
function goToLab() {
  window.top.location.search = "?page=setup";
}
</script>
</body>
</html>"""

    st_iframe(HOME_HTML, height=st.session_state.get("win_h", 900), scrolling=True)

# ═════════════════════════════════════════════════════════════════════════════
# SETUP / PREFERENCES PAGE
# ═════════════════════════════════════════════════════════════════════════════
elif current_page == "setup":

    SETUP_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<style>
    body { 
        background: #050508; color: #E8E8F0; font-family: 'DM Sans', sans-serif; 
        display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;
    }
    .setup-card {
        background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px; border-radius: 24px; width: 100%; max-width: 500px; text-align: center;
    }
    h2 { font-family: 'Syne', sans-serif; font-size: 2rem; margin-bottom: 8px; }
    p { color: rgba(232, 232, 240, 0.5); margin-bottom: 32px; font-size: 0.9rem; }
    
    .option-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 32px; }
    
    .opt-btn {
        background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px; border-radius: 12px; color: #fff; cursor: pointer; transition: all 0.2s;
        display: flex; flex-direction: column; align-items: center; gap: 8px;
    }
    .opt-btn:hover { background: rgba(124, 58, 237, 0.1); border-color: #7c3aed; }
    .opt-btn.active { background: rgba(124, 58, 237, 0.2); border-color: #7c3aed; box-shadow: 0 0 20px rgba(124, 58, 237, 0.2); }
    .opt-icon { font-size: 1.5rem; }
    .opt-label { font-size: 0.8rem; font-weight: 600; }

    .start-btn {
        width: 100%; padding: 16px; border-radius: 12px; border: none;
        background: linear-gradient(135deg, #7c3aed, #5b21b6);
        color: white; font-weight: 600; cursor: pointer; transition: transform 0.2s;
    }
    .start-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4); }
</style>
</head>
<body>
    <div class="setup-card">
        <h2>Configure your Lab</h2>
        <p>Select your preferred environment to begin.</p>
        
        <div class="option-grid">
            <div class="opt-btn active" onclick="selectLang('python', this)">
                <span class="opt-icon">🐍</span>
                <span class="opt-label">Python</span>
            </div>
            <div class="opt-btn" onclick="selectLang('javascript', this)">
                <span class="opt-icon">🟨</span>
                <span class="opt-label">JavaScript</span>
            </div>
            <div class="opt-btn" onclick="selectLang('cpp', this)">
                <span class="opt-icon">🟦</span>
                <span class="opt-label">C++</span>
            </div>
            <div class="opt-btn" onclick="selectLang('java', this)">
                <span class="opt-icon">☕</span>
                <span class="opt-label">Java</span>
            </div>
        </div>

        <button class="start-btn" onclick="launchLab()">Initialize Environment ⚡</button>
    </div>

    <script>
        let selectedLang = 'python';

        function selectLang(lang, el) {
            selectedLang = lang;
            document.querySelectorAll('.opt-btn').forEach(btn => btn.classList.remove('active'));
            el.classList.add('active');
        }

        function launchLab() {
            var url = new URL(window.parent.location.href);
            url.searchParams.set('page', 'lab');
            url.searchParams.set('lang', selectedLang);
            window.parent.location.href = url.toString();
        }
    </script>
</body>
</html>"""
    # Prefer loading the Setup UI from disk (cleaner than editing this string).
    try:
        with open(os.path.join("ui", "setup.html"), "r", encoding="utf-8") as f:
            SETUP_HTML = f.read()
    except Exception:
        pass
    st_iframe(SETUP_HTML, height=800, scrolling=False)
# ═════════════════════════════════════════════════════════════════════════════
# LAB PAGE — full VS Code-style Monaco editor
# ═════════════════════════════════════════════════════════════════════════════
elif current_page == "lab":

    LAB_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
div,span,main,nav,ul,li,a,button,h1,p,.pill,.code-chip,.stat,.feat,.nav-logo,.nav-badge{box-sizing:border-box;margin:0;padding:0}
html,body{
  background:#0a0a0f;color:#E8E8F0;
  font-family:'DM Sans',sans-serif;
  width:100%;height:100vh;
  overflow:hidden; /* ONE scroll context — the editor handles its own */
}

/* ── Activity bar (leftmost strip, like VS Code) ── */
.activity-bar{
  position:fixed;left:0;top:0;bottom:0;width:48px;
  background:#111118;border-right:1px solid rgba(255,255,255,.05);
  display:flex;flex-direction:column;align-items:center;
  padding:8px 0;gap:4px;z-index:50;
}
.act-btn{width:36px;height:36px;border-radius:8px;border:none;
  background:transparent;cursor:pointer;display:flex;align-items:center;
  justify-content:center;color:rgba(232,232,240,.3);
  transition:all .2s;font-size:1rem}
.act-btn:hover,.act-btn.active{color:#E8E8F0;background:rgba(255,255,255,.06)}
.act-btn.active{color:#a78bfa}
.act-spacer{flex:1}
.act-logo{font-family:'Syne',sans-serif;font-weight:800;font-size:.65rem;
  letter-spacing:-.01em;color:#7c3aed;margin-bottom:4px;writing-mode:vertical-rl;
  text-orientation:mixed;transform:rotate(180deg);letter-spacing:.08em}

/* ── Sidebar panel ── */
.sidebar{
  position:fixed;left:48px;top:0;bottom:0;width:220px;
  background:#0e0e18;border-right:1px solid rgba(255,255,255,.05);
  display:flex;flex-direction:column;overflow:hidden;
  transition:transform .2s ease;z-index:40;
}
.sidebar.hidden{transform:translateX(-220px)}
.sidebar-title{padding:14px 16px 8px;font-size:.65rem;font-weight:500;
  letter-spacing:.12em;text-transform:uppercase;color:rgba(232,232,240,.25);}
.sidebar-section{padding:0 8px;margin-bottom:16px}
.section-label{font-size:.6rem;font-weight:500;letter-spacing:.1em;
  text-transform:uppercase;color:rgba(232,232,240,.2);padding:4px 8px;margin-bottom:4px}

.lang-btn{display:flex;align-items:center;gap:8px;width:100%;
  padding:7px 10px;border-radius:6px;font-size:.76rem;
  color:rgba(232,232,240,.4);cursor:pointer;background:transparent;border:none;
  transition:all .18s;text-align:left;font-family:'DM Sans',sans-serif}
.lang-btn:hover{background:rgba(255,255,255,.05);color:rgba(232,232,240,.75)}
.lang-btn.active{background:rgba(52,211,153,.1);color:#34d399}
.lang-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}

.file-item{display:flex;align-items:center;gap:7px;padding:6px 10px;
  border-radius:6px;font-size:.74rem;font-family:'JetBrains Mono',monospace;
  color:rgba(232,232,240,.38);cursor:pointer;transition:all .18s}
.file-item:hover{background:rgba(255,255,255,.05);color:rgba(232,232,240,.7)}
.file-item.active{background:rgba(124,58,237,.12);color:#c084fc}
.file-ext{font-size:.6rem;opacity:.5}

.sidebar-divider{height:1px;background:rgba(255,255,255,.04);margin:8px 16px}

.ai-shortcut{display:flex;align-items:center;gap:7px;padding:6px 10px;
  border-radius:6px;font-size:.73rem;color:rgba(52,211,153,.5);
  cursor:pointer;transition:all .18s;font-family:'DM Sans',sans-serif}
.ai-shortcut:hover{background:rgba(52,211,153,.08);color:#34d399}
.ai-shortcut-icon{font-size:.75rem;opacity:.7}

/* ── Top tab bar ── */
.tabbar{
  position:fixed;left:268px;right:0;top:0;height:37px;
  background:#0d0d16;border-bottom:1px solid rgba(255,255,255,.06);
  display:flex;align-items:stretch;z-index:30;
  transition:left .2s;
}
.tabbar.full{left:48px}
.editor-tab{display:flex;align-items:center;gap:7px;padding:0 16px;
  font-size:.78rem;font-family:'JetBrains Mono',monospace;
  color:rgba(232,232,240,.4);cursor:pointer;border-right:1px solid rgba(255,255,255,.05);
  position:relative;transition:all .2s;white-space:nowrap}
.editor-tab.active{color:#E8E8F0;background:#0a0a0f}
.editor-tab.active::after{content:'';position:absolute;bottom:0;left:0;right:0;
  height:1px;background:#7c3aed}
.tab-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
.tabbar-right{margin-left:auto;display:flex;align-items:center;gap:8px;padding:0 16px}
.run-btn{display:flex;align-items:center;gap:5px;padding:5px 14px;
  background:linear-gradient(135deg,#16a34a,#15803d);
  color:#fff;border:none;border-radius:6px;cursor:pointer;
  font-size:.75rem;font-weight:500;font-family:'DM Sans',sans-serif;
  transition:all .18s;box-shadow:0 0 14px rgba(22,163,74,.25)}
.run-btn:hover{transform:translateY(-1px);box-shadow:0 0 22px rgba(22,163,74,.4)}
.run-btn:active{transform:translateY(0)}
.back-btn{padding:5px 12px;background:transparent;
  color:rgba(232,232,240,.35);border:1px solid rgba(255,255,255,.07);
  border-radius:6px;cursor:pointer;font-size:.75rem;
  font-family:'DM Sans',sans-serif;transition:all .2s}
.back-btn:hover{color:#E8E8F0;border-color:rgba(255,255,255,.18)}
.toggle-sidebar{padding:5px 10px;background:transparent;
  color:rgba(232,232,240,.3);border:none;border-radius:6px;
  cursor:pointer;font-size:.85rem;transition:color .2s}
.toggle-sidebar:hover{color:rgba(232,232,240,.7)}

/* ── Main editor area ── */
.editor-area{
  position:fixed;
  left:268px;right:320px;top:37px;
  bottom:200px;
  transition:left .2s;
}
.editor-area.full{left:48px}
#monaco-container{width:100%;height:100%}

/* ── Terminal / output ── */
.terminal{
  position:fixed;left:268px;right:320px;
  bottom:0;height:200px;
  background:#060609;
  border-top:1px solid rgba(255,255,255,.06);
  display:flex;flex-direction:column;
  transition:left .2s;
}
.terminal.full{left:48px}
.terminal-header{
  display:flex;align-items:center;justify-content:space-between;
  padding:6px 14px;border-bottom:1px solid rgba(255,255,255,.04);flex-shrink:0;
  background:#080810;
}
.terminal-tabs{display:flex;gap:0}
.term-tab{padding:4px 14px;font-size:.7rem;font-family:'JetBrains Mono',monospace;
  color:rgba(232,232,240,.3);cursor:pointer;border-bottom:1px solid transparent;
  transition:all .18s}
.term-tab.active{color:#E8E8F0;border-bottom-color:#7c3aed}
.term-actions{display:flex;gap:4px}
.term-action{background:transparent;border:none;cursor:pointer;
  color:rgba(232,232,240,.25);font-size:.75rem;padding:3px 7px;
  border-radius:4px;transition:color .18s;font-family:'JetBrains Mono',monospace}
.term-action:hover{color:rgba(232,232,240,.7)}
.terminal-body{flex:1;overflow-y:auto;padding:10px 14px;
  font-family:'JetBrains Mono',monospace;font-size:.75rem;line-height:1.75;
  color:#E8E8F0}
.terminal-body::-webkit-scrollbar{width:3px}
.terminal-body::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:3px}
.t-prompt{color:#34d399}.t-err{color:#f87171}.t-dim{color:rgba(232,232,240,.25)}
.t-success{color:#34d399}.t-warn{color:#fbbf24}

/* ── AI Panel ── */
.ai-panel{
  position:fixed;right:0;top:0;bottom:0;width:320px;
  background:#0b0b14;
  border-left:1px solid rgba(255,255,255,.05);
  display:flex;flex-direction:column;overflow:hidden;
}
.ai-header{padding:10px 14px;border-bottom:1px solid rgba(255,255,255,.05);
  flex-shrink:0;display:flex;align-items:center;justify-content:space-between}
.ai-header-left{display:flex;align-items:center;gap:8px}
.ai-title{font-family:'Syne',sans-serif;font-size:.85rem;font-weight:700;
  color:rgba(232,232,240,.7)}
.ai-model-badge{font-size:.62rem;font-weight:500;padding:2px 8px;
  border-radius:99px;border:1px solid rgba(124,58,237,.3);
  color:#a78bfa;background:rgba(124,58,237,.1);letter-spacing:.04em}
.ai-status{display:flex;align-items:center;gap:5px;font-size:.65rem;
  color:rgba(52,211,153,.6)}
.ai-status-dot{width:5px;height:5px;border-radius:50%;background:#34d399;
  animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}

.ai-messages{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:10px}
.ai-messages::-webkit-scrollbar{width:3px}
.ai-messages::-webkit-scrollbar-thumb{background:rgba(255,255,255,.08);border-radius:3px}

.msg{animation:msgIn .2s ease}
@keyframes msgIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.msg-user{align-self:flex-end}
.msg-user .bubble{background:rgba(124,58,237,.18);border:1px solid rgba(124,58,237,.22);
  color:rgba(232,232,240,.85);border-radius:10px 10px 2px 10px;
  padding:8px 11px;font-size:.78rem;line-height:1.55;max-width:230px}
.msg-ai .bubble{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.06);
  color:rgba(232,232,240,.78);border-radius:10px 10px 10px 2px;
  padding:8px 11px;font-size:.78rem;line-height:1.6;max-width:260px}
.msg-ai .bubble code{font-family:'JetBrains Mono',monospace;font-size:.7rem;
  background:rgba(124,58,237,.15);padding:1px 4px;border-radius:3px;color:#c084fc}
.msg-label{font-size:.6rem;color:rgba(232,232,240,.2);margin-bottom:3px;padding:0 3px}
.msg-label.ai{color:rgba(52,211,153,.45)}

.thinking{display:flex;align-items:center;gap:6px;
  padding:7px 10px;background:rgba(52,211,153,.04);
  border:1px solid rgba(52,211,153,.1);border-radius:8px;
  font-size:.73rem;color:rgba(52,211,153,.6)}
.dots span{display:inline-block;width:4px;height:4px;border-radius:50%;
  background:#34d399;animation:dot 1.2s infinite;margin:0 1px}
.dots span:nth-child(2){animation-delay:.2s}
.dots span:nth-child(3){animation-delay:.4s}
@keyframes dot{0%,80%,100%{opacity:.2;transform:scale(.8)}40%{opacity:1;transform:scale(1)}}

.ai-input-area{padding:10px;border-top:1px solid rgba(255,255,255,.05);flex-shrink:0}
.ai-input-row{display:flex;gap:7px;align-items:flex-end}
.ai-input{flex:1;background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);border-radius:8px;
  padding:8px 11px;color:#E8E8F0;font-size:.78rem;
  font-family:'DM Sans',sans-serif;resize:none;
  min-height:34px;max-height:90px;outline:none;
  transition:border-color .2s;line-height:1.5}
.ai-input:focus{border-color:rgba(124,58,237,.4)}
.ai-input::placeholder{color:rgba(232,232,240,.18)}
.send-btn{width:32px;height:32px;border-radius:7px;
  background:linear-gradient(135deg,#7c3aed,#5b21b6);
  border:none;cursor:pointer;display:flex;align-items:center;
  justify-content:center;flex-shrink:0;transition:all .18s;
  box-shadow:0 0 10px rgba(124,58,237,.28)}
.send-btn:hover{transform:translateY(-1px);box-shadow:0 0 18px rgba(124,58,237,.48)}
.send-btn svg{width:13px;height:13px;fill:#fff}
.ai-hint{font-size:.62rem;color:rgba(232,232,240,.15);text-align:center;
  margin-top:5px;font-family:'JetBrains Mono',monospace}

.question-item{
  font-size:.72rem;
  padding:5px 8px;
  border-radius:6px;
  margin-bottom:4px;
  line-height:1.4;
}
.question-item.current{
  background:rgba(124,58,237,.18);
  border:1px solid rgba(124,58,237,.35);
  color:#e5e7eb;
}
.question-item.completed{
  background:rgba(34,197,94,.12);
  border:1px solid rgba(34,197,94,.3);
  color:rgba(187,247,208,.9);
}
.question-item.locked{
  background:rgba(15,23,42,.7);
  border:1px dashed rgba(148,163,184,.3);
  color:rgba(148,163,184,.6);
}
.question-complete-btn{
  width:100%;
  margin-top:6px;
  padding:6px 8px;
  border-radius:6px;
  border:none;
  cursor:pointer;
  font-size:.72rem;
  font-family:'DM Sans',sans-serif;
  background:linear-gradient(135deg,#22c55e,#16a34a);
  color:#f9fafb;
}
.question-complete-btn:disabled{
  cursor:default;
  background:rgba(15,23,42,.8);
  color:rgba(148,163,184,.8);
}

/* ── Status bar (bottom strip) ── */
.statusbar{position:fixed;left:0;right:0;bottom:0;height:22px;
  background:#1a0a3a;display:flex;align-items:center;
  padding:0 12px;gap:16px;z-index:60;
  /* sits behind terminal — terminal has bottom:0 too, status is visual only */
  pointer-events:none;
}
.sb-item{font-size:.62rem;color:rgba(167,139,250,.6);
  display:flex;align-items:center;gap:4px;font-family:'JetBrains Mono',monospace}
.sb-branch::before{content:'⎇  '}
</style>
</head>
<body>

<!-- ACTIVITY BAR -->
<div class="activity-bar">
  <button class="act-btn active" onclick="toggleSidebar()" title="Explorer">📁</button>
  <button class="act-btn" title="Search">🔍</button>
  <button class="act-btn" title="Extensions">🧩</button>
  <div class="act-spacer"></div>
  <div class="act-logo">CX</div>
</div>

<!-- SIDEBAR -->
<div class="sidebar" id="sidebar">
  <div class="sidebar-title">Explorer</div>

  <div class="sidebar-section">
    <div class="section-label">Language</div>
    <button class="lang-btn active" id="lang-python" onclick="setLang('python','Python','main.py','#3b82f6')">
      <span class="lang-dot" style="background:#3b82f6"></span>Python
    </button>
    <button class="lang-btn" id="lang-javascript" onclick="setLang('javascript','JavaScript','index.js','#eab308')">
      <span class="lang-dot" style="background:#eab308"></span>JavaScript
    </button>
    <button class="lang-btn" id="lang-cpp" onclick="setLang('cpp','C++','main.cpp','#8b5cf6')">
      <span class="lang-dot" style="background:#8b5cf6"></span>C++
    </button>
    <button class="lang-btn" id="lang-java" onclick="setLang('java','Java','Main.java','#f97316')">
      <span class="lang-dot" style="background:#f97316"></span>Java
    </button>
  </div>

  <div class="sidebar-divider"></div>

  <div class="sidebar-section">
    <div class="section-label">Files</div>
    <div class="file-item active" id="snip-hello" onclick="loadSnippet('hello',this)">
      <span>📄</span>hello<span class="file-ext" id="snip-ext">.py</span>
    </div>
    <div class="file-item" id="snip-fibonacci" onclick="loadSnippet('fibonacci',this)">
      <span>📄</span>fibonacci<span class="file-ext" id="snip-ext2">.py</span>
    </div>
    <div class="file-item" id="snip-sorting" onclick="loadSnippet('sorting',this)">
      <span>📄</span>sorting<span class="file-ext" id="snip-ext3">.py</span>
    </div>
    <div class="file-item" id="snip-recursion" onclick="loadSnippet('recursion',this)">
      <span>📄</span>recursion<span class="file-ext" id="snip-ext4">.py</span>
    </div>
    <div class="file-item" id="snip-classes" onclick="loadSnippet('classes',this)">
      <span>📄</span>classes<span class="file-ext" id="snip-ext5">.py</span>
    </div>
  </div>

  <div class="sidebar-divider"></div>

  <div class="sidebar-section">
    <div class="section-label">AI Quick Actions</div>
    <div class="ai-shortcut" onclick="sendAI('Explain this code line by line')">
      <span class="ai-shortcut-icon">✦</span>Explain code
    </div>
    <div class="ai-shortcut" onclick="sendAI('Find bugs in this code and explain them')">
      <span class="ai-shortcut-icon">✦</span>Find bugs
    </div>
    <div class="ai-shortcut" onclick="sendAI('How can I optimize this code?')">
      <span class="ai-shortcut-icon">✦</span>Optimize
    </div>
    <div class="ai-shortcut" onclick="sendAI('What is the time complexity of this code?')">
      <span class="ai-shortcut-icon">✦</span>Complexity
    </div>
  </div>

  <div class="sidebar-divider"></div>

  <div class="sidebar-section">
    <div class="section-label">Questions</div>
    <div id="question-list"></div>
  </div>
</div>

<!-- TAB BAR -->
<div class="tabbar" id="tabbar">
  <div class="editor-tab active">
    <span class="tab-dot" style="background:#3b82f6" id="tab-dot"></span>
    <span id="tab-filename">main.py</span>
  </div>
  <div class="tabbar-right">
    <button class="toggle-sidebar" onclick="toggleSidebar()" title="Toggle sidebar">☰</button>
    <button class="back-btn" onclick="goHome()">← Home</button>
    <button class="run-btn" onclick="runCode()">▶ Run</button>
  </div>
</div>

<!-- EDITOR -->
<div class="editor-area" id="editor-area">
  <div id="monaco-container"></div>
</div>

<!-- TERMINAL -->
<div class="terminal" id="terminal">
  <div class="terminal-header">
    <div class="terminal-tabs">
      <div class="term-tab active">Terminal</div>
      <div class="term-tab" style="cursor:default;opacity:.4">Problems</div>
    </div>
    <div class="term-actions">
      <button class="term-action" onclick="clearTerminal()">⨯ clear</button>
    </div>
  </div>
  <div class="terminal-body" id="term-body">
    <div class="t-dim">Codexa Lab — Monaco Editor · Press <strong>Ctrl+Enter</strong> or click ▶ Run</div>
  </div>
</div>

<!-- AI PANEL -->
<div class="ai-panel">
  <div class="ai-header">
    <div class="ai-header-left">
      <div class="ai-title">AI Tutor</div>
      <div class="ai-model-badge">DeepSeek-R1</div>
    </div>
    <div class="ai-status"><div class="ai-status-dot"></div>online</div>
  </div>
  <div class="ai-messages" id="ai-messages">
    <div class="msg msg-ai">
      <div class="msg-label ai">Codexa AI</div>
      <div class="bubble">Hey! 👋 Welcome to the lab. Write or load some code, hit <code>▶ Run</code>, then ask me anything — I'll explain the logic, spot bugs, and teach you the concepts behind it.</div>
    </div>
    <div class="msg msg-ai">
      <div class="bubble">Try a file from the sidebar, or start fresh. Use <code>Ctrl+Enter</code> to run anytime.</div>
    </div>
  </div>
  <div class="ai-input-area">
    <div class="ai-input-row">
      <textarea class="ai-input" id="ai-input" placeholder="Ask anything..." rows="1"
        onkeydown="handleKey(event)"></textarea>
      <button class="send-btn" onclick="sendMessage()">
        <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2v7z"/></svg>
      </button>
    </div>
    <div class="ai-hint">Ctrl+Enter · powered by oxlo.ai</div>
  </div>
</div>

<!-- Monaco + Lab Logic -->
<script>
// ── State ─────────────────────────────────────────────────────────────────
const urlParams = new URLSearchParams(window.parent.location.search);
var currentLang = urlParams.get('lang') || 'python'; 
var editor; 
var sidebarVisible = true;

var EXTS = {python:'.py',javascript:'.js',cpp:'.cpp',java:'.java'};
var MONO_LANG = {python:'python',javascript:'javascript',cpp:'cpp',java:'java'};

var SNIPPETS = {
  python: {
    hello: 'print("Hello, World!")\n',
    fibonacci: 'def fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:\n        return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))\n',
    sorting: 'def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\narr = [64, 34, 25, 12, 22, 11, 90]\nprint("Before:", arr)\nprint("After: ", bubble_sort(arr))\n',
    recursion: 'def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n\nprint("5! =", factorial(5))\n',
    classes: 'class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        pass\n\nclass Dog(Animal):\n    def speak(self):\n        return f"{self.name} says Woof!"\n\nrex = Dog("Rex")\nprint(rex.speak())\n'
  },
  javascript: {
    hello: 'console.log("Hello, World!");\n',
    fibonacci: 'function fibonacci(n) {\n    if (n <= 0) return 0;\n    if (n === 1) return 1;\n    return fibonacci(n-1) + fibonacci(n-2);\n}\n\nconsole.log(fibonacci(10));\n',
    sorting: 'function bubbleSort(arr) {\n    let n = arr.length;\n    for (let i = 0; i < n; i++) {\n        for (let j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                let temp = arr[j];\n                arr[j] = arr[j + 1];\n                arr[j + 1] = temp;\n            }\n        }\n    }\n    return arr;\n}\n\nlet arr = [64, 34, 25, 12, 22, 11, 90];\nconsole.log("Before:", arr.join(" "));\nconsole.log("After: ", bubbleSort(arr).join(" "));\n',
    recursion: 'function factorial(n) {\n    if (n === 0) return 1;\n    return n * factorial(n-1);\n}\n\nconsole.log("5! = " + factorial(5));\n',
    classes: 'class Animal {\n    constructor(name) {\n        this.name = name;\n    }\n    speak() {}\n}\n\nclass Dog extends Animal {\n    speak() {\n        return `${this.name} says Woof!`;\n    }\n}\n\nlet rex = new Dog("Rex");\nconsole.log(rex.speak());\n'
  },
  cpp: {
    hello: '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}\n',
    fibonacci: '#include <iostream>\n\nint fibonacci(int n) {\n    if (n <= 0) return 0;\n    if (n == 1) return 1;\n    return fibonacci(n-1) + fibonacci(n-2);\n}\n\nint main() {\n    std::cout << fibonacci(10) << std::endl;\n    return 0;\n}\n',
    sorting: '#include <iostream>\n#include <vector>\n\nvoid bubbleSort(std::vector<int>& arr) {\n    int n = arr.size();\n    for (int i = 0; i < n; i++) {\n        for (int j = 0; j < n - i - 1; j++) {\n            if (arr[j] > arr[j + 1]) {\n                std::swap(arr[j], arr[j + 1]);\n            }\n        }\n    }\n}\n\nint main() {\n    std::vector<int> arr = {64, 34, 25, 12, 22, 11, 90};\n    std::cout << "Before: ";\n    for(int x : arr) std::cout << x << " ";\n    std::cout << "\\nAfter:  ";\n    bubbleSort(arr);\n    for(int x : arr) std::cout << x << " ";\n    std::cout << std::endl;\n    return 0;\n}\n',
    recursion: '#include <iostream>\n\nint factorial(int n) {\n    if (n == 0) return 1;\n    return n * factorial(n-1);\n}\n\nint main() {\n    std::cout << "5! = " << factorial(5) << std::endl;\n    return 0;\n}\n',
    classes: '#include <iostream>\n#include <string>\n\nclass Animal {\nprotected:\n    std::string name;\npublic:\n    Animal(std::string n) : name(n) {}\n    virtual void speak() = 0;\n};\n\nclass Dog : public Animal {\npublic:\n    Dog(std::string n) : Animal(n) {}\n    void speak() override {\n        std::cout << name << " says Woof!" << std::endl;\n    }\n};\n\nint main() {\n    Dog rex("Rex");\n    rex.speak();\n    return 0;\n}\n'
  },
  java: {
    hello: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}\n',
    fibonacci: 'public class Main {\n    public static int fibonacci(int n) {\n        if (n <= 0) return 0;\n        if (n == 1) return 1;\n        return fibonacci(n-1) + fibonacci(n-2);\n    }\n    public static void main(String[] args) {\n        System.out.println(fibonacci(10));\n    }\n}\n',
    sorting: 'import java.util.Arrays;\n\npublic class Main {\n    public static void bubbleSort(int[] arr) {\n        int n = arr.length;\n        for (int i = 0; i < n; i++) {\n            for (int j = 0; j < n - i - 1; j++) {\n                if (arr[j] > arr[j + 1]) {\n                    int temp = arr[j];\n                    arr[j] = arr[j + 1];\n                    arr[j + 1] = temp;\n                }\n            }\n        }\n    }\n    public static void main(String[] args) {\n        int[] arr = {64, 34, 25, 12, 22, 11, 90};\n        System.out.print("Before: ");\n        for(int x : arr) System.out.print(x + " ");\n        System.out.println();\n        bubbleSort(arr);\n        System.out.print("After:  ");\n        for(int x : arr) System.out.print(x + " ");\n        System.out.println();\n    }\n}\n',
    recursion: 'public class Main {\n    public static int factorial(int n) {\n        if (n == 0) return 1;\n        return n * factorial(n-1);\n    }\n    public static void main(String[] args) {\n        System.out.println("5! = " + factorial(5));\n    }\n}\n',
    classes: 'class Animal {\n    protected String name;\n    public Animal(String name) {\n        this.name = name;\n    }\n    public void speak() {}\n}\n\nclass Dog extends Animal {\n    public Dog(String name) {\n        super(name);\n    }\n    @Override\n    public void speak() {\n        System.out.println(name + " says Woof!");\n    }\n}\n\npublic class Main {\n    public static void main(String[] args) {\n        Dog rex = new Dog("Rex");\n        rex.speak();\n    }\n}\n'
  }
};

// ── Progressive questions per language ───────────────────────────────────
var QUESTIONS = {
  python: [
    "Write a program that prints 'Hello, World!' to the terminal.",
    "Create a function that adds two numbers and prints the result.",
    "Write a loop that prints the numbers 1 through 10."
  ],
  javascript: [
    "Log 'Hello from JavaScript' to the console.",
    "Write a function add(a, b) that returns their sum.",
    "Use a for loop to log numbers 1 to 10."
  ],
  cpp: [
    "Write a C++ program that prints 'Hello, World!'.",
    "Create a function that returns the square of an integer.",
    "Use a for loop to print the elements of an integer array."
  ],
  java: [
    "Write a Java program with main that prints 'Hello, World!'.",
    "Create a method that concatenates two strings and prints the result.",
    "Use a for loop to print numbers 1 to 10."
  ]
};

var questionProgress = JSON.parse(localStorage.getItem('codexa_question_progress') || '{}');

function getCurrentQuestionIndex(){
  if(!(currentLang in questionProgress)){
    questionProgress[currentLang] = 0;
  }
  return questionProgress[currentLang];
}

function saveQuestionProgress(){
  localStorage.setItem('codexa_question_progress', JSON.stringify(questionProgress));
}

function renderQuestions(){
  var container = document.getElementById('question-list');
  if(!container || !QUESTIONS[currentLang]) return;
  container.innerHTML = '';
  var idx = getCurrentQuestionIndex();
  QUESTIONS[currentLang].forEach(function(q, i){
    var row = document.createElement('div');
    var stateClass = i < idx ? 'completed' : (i === idx ? 'current' : 'locked');
    row.className = 'question-item ' + stateClass;
    row.textContent = (i + 1) + '. ' + q;
    container.appendChild(row);
  });

  var btn = document.createElement('button');
  btn.className = 'question-complete-btn';
  if(idx >= QUESTIONS[currentLang].length - 1){
    btn.textContent = 'All questions completed';
    btn.disabled = true;
  } else {
    btn.textContent = 'Mark current question as done';
    btn.disabled = false;
    btn.onclick = function(){
      var i = getCurrentQuestionIndex();
      if(i < QUESTIONS[currentLang].length - 1){
        questionProgress[currentLang] = i + 1;
        saveQuestionProgress();
        renderQuestions();
      }
    };
  }
  container.appendChild(btn);
}

// ── Monaco init ───────────────────────────────────────────────────────────
require.config({paths:{vs:'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs'}});
require(['vs/editor/editor.main'], function(){
  monaco.editor.defineTheme('codexa', {
    base:'vs-dark', inherit:true,
    rules:[
      {token:'keyword',foreground:'c084fc',fontStyle:'bold'},
      {token:'string', foreground:'34d399'},
      {token:'comment',foreground:'3d3d5c',fontStyle:'italic'},
      {token:'number', foreground:'38bdf8'},
      {token:'type',   foreground:'f472b6'},
    ],
    colors:{
      'editor.background':'#0a0a0f',
      'editor.foreground':'#E8E8F0',
      'editor.lineHighlightBackground':'#11111a',
      'editorLineNumber.foreground':'#252535',
      'editorLineNumber.activeForeground':'#555570',
      'editor.selectionBackground':'#7c3aed2a',
      'editorCursor.foreground':'#34d399',
      'editorIndentGuide.background1':'#15152a',
      'editorWidget.background':'#0e0e1a',
    }
  });

  editor = monaco.editor.create(document.getElementById('monaco-container'),{
    value: SNIPPETS[currentLang].hello,
    language: MONO_LANG[currentLang],
    theme:'codexa',
    fontSize:14,
    fontFamily:"'JetBrains Mono', monospace",
    fontLigatures:true,
    lineHeight:22,
    minimap:{enabled:true, scale:1},
    scrollBeyondLastLine:false,
    smoothScrolling:true,
    cursorBlinking:'smooth',
    cursorSmoothCaretAnimation:'on',
    padding:{top:14,bottom:14},
    automaticLayout:true,
    tabSize:4,
    wordWrap:'off',
    renderLineHighlight:'line',
    scrollbar:{verticalScrollbarSize:4,horizontalScrollbarSize:4},
    suggest:{showKeywords:true},
    quickSuggestions:true,
  });

  document.getElementById('tab-filename').textContent = 'main' + EXTS[currentLang];
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
  var activeLang = document.getElementById('lang-' + currentLang);
  if(activeLang){ activeLang.classList.add('active'); }

  editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, runCode);
  renderQuestions();
});

// ── Sidebar toggle ────────────────────────────────────────────────────────
function toggleSidebar(){
  sidebarVisible = !sidebarVisible;
  var sb = document.getElementById('sidebar');
  var tb = document.getElementById('tabbar');
  var ea = document.getElementById('editor-area');
  var tm = document.getElementById('terminal');
  if(sidebarVisible){
    sb.classList.remove('hidden');
    tb.classList.remove('full');
    ea.classList.remove('full');
    tm.classList.remove('full');
  } else {
    sb.classList.add('hidden');
    tb.classList.add('full');
    ea.classList.add('full');
    tm.classList.add('full');
  }
  if(editor) editor.layout();
}

// ── Language switch ───────────────────────────────────────────────────────
function setLang(lang, label, filename, color){
  currentLang = lang;
  document.querySelectorAll('.lang-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('lang-'+lang).classList.add('active');
  document.getElementById('tab-filename').textContent = filename;
  document.getElementById('tab-dot').style.background = color;
  // update file extensions in sidebar
  var ext = EXTS[lang];
  ['','2','3','4','5'].forEach(function(s){
    var el = document.getElementById('snip-ext'+s);
    if(el) el.textContent = ext;
  });
  renderQuestions();
  if(editor){
    monaco.editor.setModelLanguage(editor.getModel(), MONO_LANG[lang]);
    loadSnippet('hello', document.getElementById('snip-hello'));
  }
}

// ── Snippet load ──────────────────────────────────────────────────────────
function loadSnippet(key, el){
  document.querySelectorAll('.file-item').forEach(f=>f.classList.remove('active'));
  if(el) el.classList.add('active');
  if(editor && SNIPPETS[currentLang] && SNIPPETS[currentLang][key]){
    editor.setValue(SNIPPETS[currentLang][key]);
    editor.setPosition({lineNumber:1, column:1});
  }
}

// ── Run code ──────────────────────────────────────────────────────────────
function runCode(){
  var code = editor ? editor.getValue() : '';
  clearTerminal();
  termLine('$ ' + document.getElementById('tab-filename').textContent, 't-prompt');

  if(currentLang === 'javascript'){
    var logs = [];
    try {
      var fn = new Function('console', code);
      fn({
        log:   function(){ logs.push({t:'out', v:Array.from(arguments).join(' ')}); },
        error: function(){ logs.push({t:'err', v:Array.from(arguments).join(' ')}); },
        warn:  function(){ logs.push({t:'warn',v:Array.from(arguments).join(' ')}); },
      });
      logs.forEach(function(l){
        termLine(l.v, l.t==='err'?'t-err':l.t==='warn'?'t-warn':'');
      });
      termLine('', '');
      termLine('✓  exited with code 0  (' + (Math.random()*80+20).toFixed(0) + 'ms)', 't-success');
    } catch(e) {
      termLine('Uncaught ' + e.toString(), 't-err');
    }
  } else {
    // Simulate for Python / C++ / Java based on content
    var ms = (Math.random()*150+40).toFixed(0);
    setTimeout(function(){
      var lines = simulate(code, currentLang);
      lines.forEach(function(l){ termLine(l.v, l.t); });
      termLine('', '');
      termLine('✓  exited with code 0  (' + ms + 'ms)', 't-success');
    }, parseInt(ms));
  }
}

function simulate(code, lang){
  var out = [];
  if(/hello|Hello/.test(code) && !/fibonacci|fibonacci/.test(code)){
    out.push({v:'Hello, World!',t:''});
    out.push({v:'Welcome to Codexa!',t:''});
  } else if(/fibonacci|Fibonacci/.test(code)){
    var fibs=[0,1,1,2,3,5,8,13,21,34];
    fibs.forEach(function(f,i){ out.push({v:'fib('+i+') = '+f, t:''}); });
  } else if(/bubble|Bubble|bubbleSort/.test(code)){
    if(lang==='python'){
      out.push({v:'Before: [64, 34, 25, 12, 22, 11, 90]',t:''});
      out.push({v:'After:  [11, 12, 22, 25, 34, 64, 90]',t:''});
    } else {
      out.push({v:'Before: 64 34 25 12 22 11 90',t:''});
      out.push({v:'After:  11 12 22 25 34 64 90',t:''});
    }
  } else if(/factorial/.test(code)){
    var facts=[1,1,2,6,24,120,720,5040];
    facts.forEach(function(f,i){ out.push({v:i+'! = '+f, t:''}); });
  } else if(/class|Animal|Dog/.test(code)){
    out.push({v:'Rex says Woof!',t:''});
    out.push({v:'Rex fetches the ball!',t:''});
  } else {
    out.push({v:'[Program executed successfully]',t:'t-success'});
  }
  return out;
}

function termLine(text, cls){
  var body = document.getElementById('term-body');
  var div = document.createElement('div');
  if(cls) div.className = cls;
  div.textContent = text;
  body.appendChild(div);
  body.scrollTop = body.scrollHeight;
}

function clearTerminal(){
  document.getElementById('term-body').innerHTML = '';
}

// ── AI Chat ───────────────────────────────────────────────────────────────
var AI = {
  explain:[
    "Sure! Let me walk through this.\n\nThe function takes input, transforms it, and returns a result. This is the essence of **functional decomposition** — breaking a problem into smaller, single-purpose pieces.\n\nThe loop iterates over each element, applying the logic step by step.",
    "Great question! The core idea here is **iteration** — repeating a block of code for each item. Notice how the condition controls when the loop stops. That's your *termination condition*, and it's critical to avoid infinite loops."
  ],
  bug:[
    "Looking good overall! One thing to watch: in recursive functions, always verify your **base case** terminates correctly. Without it, you'll hit a stack overflow.\n\nAlso check boundary inputs — what happens with `n=0` or an empty list?",
    "The logic looks sound. A common Python gotcha: `=` is assignment, `==` is comparison. Easy to mix up inside conditions. Also verify your loop range — off-by-one errors are the sneakiest bugs."
  ],
  optimize:[
    "Your current approach is correct but could be faster. For Fibonacci, **memoization** (caching already-computed results) turns O(2ⁿ) into O(n):\n\n`from functools import lru_cache` then add `@lru_cache` above the function.",
    "For sorting, Bubble Sort is O(n²) — fine for learning, slow in production. Python's built-in `sorted()` uses **Timsort** at O(n log n), which is much faster on real data."
  ],
  complexity:[
    "Let's analyze:\n\n• **Time complexity**: O(n²) — two nested loops, each iterating up to n times.\n• **Space complexity**: O(1) — sorting in-place, no extra memory proportional to input.\n\nFor n=1000 this means ~1,000,000 operations. Fine for small inputs, slow for large ones.",
    "This recursive solution has:\n\n• **Time**: O(2ⁿ) without memoization — each call branches into two more.\n• **Space**: O(n) on the call stack — each recursive call adds a frame.\n\nWith memoization: O(n) time and O(n) space."
  ],
  default:[
    "That's a fundamental concept in programming! The key mental model: think of every function as a **black box** — input goes in, output comes out. Keep functions small and single-purpose.",
    "Good question! Want me to explain the time complexity of your current approach? Understanding Big O notation is one of the most valuable skills for writing code that scales.",
    "Try running the code and observing the output. Then modify one thing and run it again. **Active experimentation** is the fastest way to build intuition."
  ]
};

function getAIReply(msg){
  var m = msg.toLowerCase();
  if(/explain|what|how|work|mean/.test(m)) return pick(AI.explain);
  if(/bug|error|wrong|fix|issue|crash/.test(m)) return pick(AI.bug);
  if(/optim|faster|better|improve|speed/.test(m)) return pick(AI.optimize);
  if(/complex|big.?o|time|space|efficient/.test(m)) return pick(AI.complexity);
  return pick(AI.default);
}

function pick(arr){ return arr[Math.floor(Math.random()*arr.length)]; }

function sendAI(text){ document.getElementById('ai-input').value=text; sendMessage(); }

var mc = 0;
function sendMessage(){
  var inp = document.getElementById('ai-input');
  var msg = inp.value.trim();
  if(!msg) return;
  inp.value=''; inp.style.height='auto';
  appendMsg(msg,'user');
  var tid = appendThinking();
  setTimeout(function(){
    document.getElementById(tid) && document.getElementById(tid).remove();
    appendMsg(getAIReply(msg),'ai');
  }, 700+Math.random()*700);
}

function appendMsg(text, role){
  var id='m'+(++mc);
  var box=document.getElementById('ai-messages');
  var wrap=document.createElement('div');
  wrap.className='msg msg-'+role; wrap.id=id;
  var lbl=document.createElement('div');
  lbl.className='msg-label'+(role==='ai'?' ai':'');
  lbl.textContent=role==='ai'?'Codexa AI':'You';
  var bub=document.createElement('div');
  bub.className='bubble';
  bub.innerHTML=text.replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\n/g,'<br>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
  wrap.appendChild(lbl); wrap.appendChild(bub);
  box.appendChild(wrap); box.scrollTop=box.scrollHeight;
  return id;
}

function appendThinking(){
  var id='t'+(++mc);
  var box=document.getElementById('ai-messages');
  var div=document.createElement('div');
  div.className='msg msg-ai'; div.id=id;
  div.innerHTML='<div class="thinking">Thinking<div class="dots"><span></span><span></span><span></span></div></div>';
  box.appendChild(div); box.scrollTop=box.scrollHeight;
  return id;
}

function handleKey(e){
  if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){e.preventDefault();sendMessage();}
  var el=e.target; el.style.height='auto';
  el.style.height=Math.min(el.scrollHeight,90)+'px';
}

// ── Navigation ────────────────────────────────────────────────────────────
function goHome(){
  var url=new URL(window.parent.location.href);
  url.searchParams.set('page','start');
  window.parent.location.href=url.toString();
}
</script>
</body>
</html>"""

    # Load the Lab UI from disk (keeps `app.py` cleaner to work with).
    # Edit `ui/lab.html` for Monaco/editor changes.
    try:
        with open(os.path.join("ui", "lab.html"), "r", encoding="utf-8") as f:
            LAB_HTML = f.read()
    except Exception:
        pass

    st_iframe(LAB_HTML, height=800, scrolling=False)

import os
os.makedirs("ui", exist_ok=True)
if not os.path.exists("ui/home.html"):
    with open("ui/home.html", "w", encoding="utf-8") as f:
        f.write(HOME_HTML)
if not os.path.exists("ui/setup.html"):
    with open("ui/setup.html", "w", encoding="utf-8") as f:
        f.write(SETUP_HTML)
if not os.path.exists("ui/lab.html"):
    # `ui/lab.html` is tracked in the repo; if it's missing we can regenerate it
    # by running `python refactor.py`.
    pass