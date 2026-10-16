import streamlit as st

st.set_page_config(page_title="Classroom Timer", layout="wide")
st.title("Classroom Timer")
st.write("Enter minutes and seconds, then press Start. Use Presentation Mode for a very large display.")

# Inputs
col1, col2 = st.columns([1, 2])
with col1:
    minutes = st.number_input("Minutes", min_value=0, max_value=600, value=1, step=1, format="%d")
    seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1, format="%d")
    presentation = st.checkbox("Presentation mode (large display)", value=True)
    start = st.button("Start")
    stop = st.button("Stop / Reset")

# compute total seconds
try:
    total_seconds = int(minutes) * 60 + int(seconds)
except Exception:
    total_seconds = 0

# Helper: preview or run component
with col2:
    st.markdown("### Timer display")
    if start and total_seconds > 0:
        # Choose font size depending on presentation mode
        font_px = 220 if presentation else 120
        height = 520 if presentation else 360
        html = f"""
        <div id="root" style="display:flex;align-items:center;justify-content:center;height:100%;width:100%;background:#000;">
          <div id="container" style="text-align:center;padding:10px;color:#111;">
            <div id="label" style="font-size:28px;color:#fff;margin-bottom:6px;">Timer</div>
            <div id="timer" style="font-size:{font_px}px;font-weight:700;color:#fff;letter-spacing:6px;"></div>
            <div style="margin-top:18px;">
              <button id="fullscreen" style="font-size:18px;padding:8px 16px;margin-right:8px;">Fullscreen</button>
              <button id="pause" style="font-size:18px;padding:8px 16px;margin-right:8px;">Pause</button>
              <button id="resume" style="font-size:18px;padding:8px 16px;margin-right:8px;">Resume</button>
              <button id="reset" style="font-size:18px;padding:8px 16px;">Reset</button>
            </div>
            <audio id="beep" src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"></audio>
          </div>
        </div>

        <script>
          const DURATION = {total_seconds};
          let remaining = DURATION;
          let interval = null;
          const timerEl = document.getElementById('timer');
          const container = document.getElementById('container');
          const beep = document.getElementById('beep');

          function format(s) {{
            const m = Math.floor(s/60).toString().padStart(2,'0');
            const sec = (s%60).toString().padStart(2,'0');
            return `${{m}}:${{sec}}`;
          }}

          function updateDisplay() {{
            timerEl.innerText = format(remaining);
          }}

          function onComplete() {{
            // play sound if allowed
            try {{ beep.play().catch(()=>{{}}); }} catch(e){{}}
            // flash background for emphasis
            const origBg = document.body.style.backgroundColor || '';
            let flashes = 0;
            const flashInterval = setInterval(()=>{{
              document.body.style.backgroundColor = (flashes % 2 === 0) ? '#fff176' : origBg;
              flashes += 1;
              if (flashes > 6) {{
                clearInterval(flashInterval);
                document.body.style.backgroundColor = origBg;
              }}
            }}, 300);
            // big DONE indicator
            timerEl.innerText = '00:00';
            document.getElementById('label').innerText = 'TIME!';
          }}

          function tick() {{
            if (remaining <= 0) {{
              clearInterval(interval);
              interval = null;
              onComplete();
              return;
            }}
            remaining -= 1;
            updateDisplay();
          }}

          document.getElementById('pause').onclick = function() {{
            if (interval) {{ clearInterval(interval); interval = null; }}
          }};
          document.getElementById('resume').onclick = function() {{
            if (!interval && remaining > 0) interval = setInterval(tick, 1000);
          }};
          document.getElementById('reset').onclick = function() {{
            if (interval) {{ clearInterval(interval); interval = null; }}
            remaining = DURATION;
            updateDisplay();
            document.getElementById('label').innerText = 'Timer';
          }};
          // Fullscreen support (may be limited by browser/iframe)
          document.getElementById('fullscreen').onclick = function() {{
            const el = document.getElementById('root');
            if (el.requestFullscreen) el.requestFullscreen();
            else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen(); // Safari
            else if (el.msRequestFullscreen) el.msRequestFullscreen();
          }};

          // initialize and auto-start ticking
          updateDisplay();
          if (!interval) interval = setInterval(tick, 1000);
        </script>
        """
        st.components.v1.html(html, height=height)
    else:
        # show static preview with large numerals
        preview_font = 200 if presentation else 120
        preview = f"<div style='display:flex;align-items:center;justify-content:center;height:260px;width:100%;background:#000;'><div style='font-size:{preview_font}px;font-weight:700;color:#fff'>{int(minutes):02d}:{int(seconds):02d}</div></div>"
        st.components.v1.html(preview, height=300)

# global stop/reset behaviour note
if stop:
    st.rerun()
