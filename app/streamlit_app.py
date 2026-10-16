import streamlit as st

st.set_page_config(page_title="Classroom Timer", layout="wide")

st.title("Classroom Countdown Timer")
st.write("Set minutes and seconds, then start the countdown. In presentation mode the numbers are large and easy to see from across the room.")

col_left, col_right = st.columns([1, 2])

with col_left:
    minutes = st.number_input("Minutes", min_value=0, max_value=600, value=1, step=1, format="%d")
    seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1, format="%d")
    presentation_mode = st.checkbox("Presentation mode (large display)", value=True)
    start = st.button("Start")
    stop = st.button("Stop / Reset")

try:
    total_seconds = int(minutes) * 60 + int(seconds)
except Exception:
    total_seconds = 0

with col_right:
    if start and total_seconds > 0:
        timer_font = "min(50vw, 50vh)" if presentation_mode else "220px"
        height_px = 620 if presentation_mode else 420

        html = f"""
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            background: #000;
          }}
          #timer-root {{
            width: 100%;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #000;
            color: #fff;
            font-family: Arial, sans-serif;
          }}
          #timer-shell {{
            text-align: center;
            width: 100%;
            padding: 20px;
          }}
          #timer-label {{
            font-size: clamp(20px, 3vh, 36px);
            margin-bottom: 12px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }}
          #timer-value {{
            font-size: {timer_font};
            font-weight: 800;
            line-height: 0.9;
            letter-spacing: 0.08em;
            white-space: nowrap;
          }}
          #controls {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
          }}
          #controls button {{
            font-size: 18px;
            padding: 10px 18px;
            cursor: pointer;
            border-radius: 8px;
            border: 1px solid #fff;
            background: #111;
            color: #fff;
          }}
          .hidden-controls {{
            display: none !important;
          }}
        </style>

        <div id="timer-root">
          <div id="timer-shell">
            <div id="timer-label">Timer</div>
            <div id="timer-value">00:00</div>
            <div id="controls">
              <button id="fullscreen">Fullscreen</button>
              <button id="pause">Pause</button>
              <button id="resume">Resume</button>
              <button id="reset">Reset</button>
            </div>
            <audio id="beep" src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"></audio>
          </div>
        </div>

        <script>
          const DURATION = {total_seconds};
          let remaining = DURATION;
          let interval = null;

          const valueEl = document.getElementById('timer-value');
          const labelEl = document.getElementById('timer-label');
          const controlsEl = document.getElementById('controls');
          const beep = document.getElementById('beep');

          function format(seconds) {{
            const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
            const secs = (seconds % 60).toString().padStart(2, '0');
            return `${{minutes}}:${{secs}}`;
          }}

          function updateDisplay() {{
            valueEl.textContent = format(remaining);
          }}

          function onComplete() {{
            try {{ beep.play().catch(() => {{}}); }} catch (err) {{}}

            const flash = document.createElement('div');
            flash.style.position = 'fixed';
            flash.style.top = '0';
            flash.style.left = '0';
            flash.style.width = '100vw';
            flash.style.height = '100vh';
            flash.style.background = '#fff176';
            flash.style.zIndex = '99999';
            flash.style.opacity = '0.95';
            document.body.appendChild(flash);
            setTimeout(() => flash.remove(), 1400);

            valueEl.textContent = '00:00';
            labelEl.textContent = 'TIME!';
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
            if (interval) {{
              clearInterval(interval);
              interval = null;
            }}
          }};

          document.getElementById('resume').onclick = function() {{
            if (!interval && remaining > 0) {{
              interval = setInterval(tick, 1000);
            }}
          }};

          document.getElementById('reset').onclick = function() {{
            if (interval) {{
              clearInterval(interval);
              interval = null;
            }}
            remaining = DURATION;
            updateDisplay();
            labelEl.textContent = 'Timer';
          }};

          document.getElementById('fullscreen').onclick = function() {{
            const root = document.getElementById('timer-root');
            if (root.requestFullscreen) root.requestFullscreen();
            else if (root.webkitRequestFullscreen) root.webkitRequestFullscreen();
            else if (root.msRequestFullscreen) root.msRequestFullscreen();
          }};

          updateDisplay();
          if (!interval) interval = setInterval(tick, 1000);
        </script>
        """
        st.components.v1.html(html, height=height_px)
    else:
        preview_font = "min(30vw, 30vh)" if presentation_mode else "160px"
        preview = f"""
        <div style="display:flex;align-items:center;justify-content:center;height:300px;width:100%;background:#000;color:#fff;font-family:Arial,sans-serif;">
          <div style="font-size:{preview_font};font-weight:800;letter-spacing:0.08em;line-height:0.9;white-space:nowrap;">{int(minutes):02d}:{int(seconds):02d}</div>
        </div>
        """
        st.components.v1.html(preview, height=300)

if stop:
    st.rerun()
