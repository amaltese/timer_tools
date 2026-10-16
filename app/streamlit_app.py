import streamlit as st
from datetime import timedelta
from timers import format_seconds

st.set_page_config(page_title="Classroom Timers", layout="centered")
st.title("Classroom Timers")
st.caption("A small collection of web-accessible timers (runs in the browser).")

TIMER_TYPES = ["Countdown", "Interval (work/break)", "Pomodoro"]
mode = st.selectbox("Timer type", TIMER_TYPES)

if mode == "Countdown":
    minutes = st.number_input("Minutes", min_value=0, max_value=600, value=5, step=1)
    seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1)
    total_seconds = int(minutes) * 60 + int(seconds)
    label = st.text_input("Label (optional)", value="Countdown")
    start = st.button("Start")

    if start and total_seconds > 0:
        html = f"""
        <div style='font-family:sans-serif'>
          <h2>{label}</h2>
          <div id='timer' style='font-size:48px'></div>
          <button id='start'>Start</button>
          <button id='pause'>Pause</button>
          <button id='reset'>Reset</button>
          <audio id='beep' src='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg'></audio>
        </div>
        <script>
          const DURATION = {total_seconds};
          let remaining = DURATION;
          let interval = null;
          const el = document.getElementById('timer');
          const beep = document.getElementById('beep');

          function format(s){{
            const m = Math.floor(s/60).toString().padStart(2,'0');
            const sec = (s%60).toString().padStart(2,'0');
            return `${{m}}:${{sec}}`;
          }}

          function tick(){{
            el.innerText = format(remaining);
            if (remaining <= 0) {{
              clearInterval(interval);
              beep.play();
            }} else {{
              remaining -= 1;
            }}
          }}

          document.getElementById('start').onclick = function(){{
            if (interval) return;
            interval = setInterval(tick, 1000);
          }}
          document.getElementById('pause').onclick = function(){{
            if (interval) {{ clearInterval(interval); interval = null; }}
          }}
          document.getElementById('reset').onclick = function(){{
            if (interval) {{ clearInterval(interval); interval = null; }}
            remaining = DURATION;
            el.innerText = format(remaining);
          }}

          // initialize
          el.innerText = format(remaining);
        </script>
        """
        st.components.v1.html(html, height=300)

elif mode == "Interval (work/break)":
    work_min = st.number_input("Work minutes", min_value=1, max_value=180, value=25)
    break_min = st.number_input("Break minutes", min_value=1, max_value=60, value=5)
    rounds = st.number_input("Rounds", min_value=1, max_value=20, value=4)
    label = st.text_input("Label (optional)", value="Interval")
    start = st.button("Start")
    if start:
        total_work = int(work_min) * 60
        total_break = int(break_min) * 60
        ROUNDS = int(rounds)
        html = f"""
        <div style='font-family:sans-serif'>
          <h2>{label}</h2>
          <div id='phase' style='font-size:22px'></div>
          <div id='timer' style='font-size:48px'></div>
          <div id='round' style='font-size:18px'></div>
          <button id='start'>Start</button>
          <button id='pause'>Pause</button>
          <button id='reset'>Reset</button>
          <audio id='beep' src='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg'></audio>
        </div>
        <script>
          const WORK = {total_work};
          const BREAK = {total_break};
          const ROUNDS = {ROUNDS};
          let round = 1;
          let phase = 'Work';
          let remaining = WORK;
          let interval = null;

          const el = document.getElementById('timer');
          const phaseEl = document.getElementById('phase');
          const roundEl = document.getElementById('round');
          const beep = document.getElementById('beep');

          function format(s){{
            const m = Math.floor(s/60).toString().padStart(2,'0');
            const sec = (s%60).toString().padStart(2,'0');
            return `${{m}}:${{sec}}`;
          }}

          function tick(){{
            el.innerText = format(remaining);
            phaseEl.innerText = phase;
            roundEl.innerText = `Round ${{round}} of ${{ROUNDS}}`;
            if (remaining <= 0) {{
              beep.play();
              if (phase === 'Work') {{
                phase = 'Break';
                remaining = BREAK;
              }} else {{
                if (round >= ROUNDS) {{
                  clearInterval(interval);
                  interval = null;
                  return;
                }}
                round += 1;
                phase = 'Work';
                remaining = WORK;
              }}
            }} else {{
              remaining -= 1;
            }}
          }}

          document.getElementById('start').onclick = function(){{
            if (interval) return;
            interval = setInterval(tick, 1000);
          }}
          document.getElementById('pause').onclick = function(){{
            if (interval) {{ clearInterval(interval); interval = null; }}
          }}
          document.getElementById('reset').onclick = function(){{
            if (interval) {{ clearInterval(interval); interval = null; }}
            round = 1; phase = 'Work'; remaining = WORK;
            el.innerText = format(remaining);
            phaseEl.innerText = phase;
            roundEl.innerText = `Round ${{round}} of ${{ROUNDS}}`;
          }}

          el.innerText = format(remaining);
          phaseEl.innerText = phase;
          roundEl.innerText = `Round ${{round}} of ${{ROUNDS}}`;
        </script>
        """
        st.components.v1.html(html, height=360)

else:  # Pomodoro
    work_min = st.number_input("Work minutes", min_value=1, max_value=180, value=25)
    short_break = st.number_input("Short break minutes", min_value=1, max_value=60, value=5)
    long_break = st.number_input("Long break minutes", min_value=1, max_value=120, value=15)
    long_after = st.number_input("Long break after how many rounds", min_value=1, max_value=10, value=4)
    rounds = st.number_input("Rounds (total)", min_value=1, max_value=20, value=8)
    label = st.text_input("Label (optional)", value="Pomodoro")
    start = st.button("Start")
    if start:
        WORK = int(work_min) * 60
        SHORT = int(short_break) * 60
        LONG = int(long_break) * 60
        LONG_AFTER = int(long_after)
        ROUNDS = int(rounds)
        html = f"""
        <div style='font-family:sans-serif'>
          <h2>{label}</h2>
          <div id='phase' style='font-size:22px'></div>
          <div id='timer' style='font-size:48px'></div>
          <div id='round' style='font-size:18px'></div>
          <button id='start'>Start</button>
          <button id='pause'>Pause</button>
          <button id='reset'>Reset</button>
          <audio id='beep' src='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg'></audio>
        </div>
        <script>
          const WORK = {WORK};
          const SHORT = {SHORT};
          const LONG = {LONG};
          const LONG_AFTER = {LONG_AFTER};
          const ROUNDS = {ROUNDS};

          let round = 1;
          let phase = 'Work';
          let remaining = WORK;
          let interval = null;

          const el = document.getElementById('timer');
          const phaseEl = document.getElementById('phase');
          const roundEl = document.getElementById('round');
          const beep = document.getElementById('beep');

          function format(s){{
            const m = Math.floor(s/60).toString().padStart(2,'0');
            const sec = (s%60).toString().padStart(2,'0');
            return `${{m}}:${{sec}}`;
          }}

          function tick(){{
            el.innerText = format(remaining);
            phaseEl.innerText = phase;
            roundEl.innerText = `Round ${{round}} of ${{ROUNDS}}`;
            if (remaining <= 0) {{
              beep.play();
              if (phase === 'Work') {{
                // decide break length
                if (round % LONG_AFTER === 0) {{
                  phase = 'Long Break';
                  remaining = LONG;
                }} else {{
                  phase = 'Short Break';
                  remaining = SHORT;
                }}
              }} else {{
                // finished a break
                if (round >= ROUNDS) {{
                  clearInterval(interval);
                  interval = null;
                  return;
                }}
                round += 1;
                phase = 'Work';
                remaining = WORK;
              }}
            }} else {{
              remaining -= 1;
            }}
          }}

          document.getElementById('start').onclick = function(){{
            if (interval) return;
            interval = setInterval(tick, 1000);
          }}
          document.getElementById('pause').onclick = function(){{
            if (interval) {{ clearInterval(interval); interval = null; }}
          }}
          document.getElementById('reset').onclick = function(){{
            if (interval) {{ clearInterval(interval); interval = null; }}
            round = 1; phase = 'Work'; remaining = WORK;
            el.innerText = format(remaining);
            phaseEl.innerText = phase;
            roundEl.innerText = `Round ${{round}} of ${{ROUNDS}}`;
          }}

          el.innerText = format(remaining);
          phaseEl.innerText = phase;
          roundEl.innerText = `Round ${{round}} of ${{ROUNDS}}`;
        </script>
        """
        st.components.v1.html(html, height=380)
