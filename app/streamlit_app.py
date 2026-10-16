import streamlit as st

st.set_page_config(page_title="Classroom Timer", layout="wide")
st.title("Classroom Timer")
st.write("Choose a timer type, set your time, and use the large display for class presentation.")

left_col, right_col = st.columns([1, 2])

with left_col:
    timer_mode = st.selectbox("Timer type", ["Countdown", "Count Up"], index=0)
    minutes = st.number_input("Minutes", min_value=0, max_value=600, value=1, step=1, format="%d")
    seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1, format="%d")
    presentation_mode = st.checkbox("Presentation mode (large display)", value=True)
    start_button = st.button("Start")

try:
    total_seconds = int(minutes) * 60 + int(seconds)
except Exception:
    total_seconds = 0

with right_col:
    display_font = "min(50vw, 50vh)" if presentation_mode else "220px"
    height_px = 620 if presentation_mode else 420

    html_template = """
    <style>
      html, body {
        margin: 0;
        padding: 0;
        background: #000;
        color: #fff;
        font-family: Arial, sans-serif;
      }
      #timer-root {
        width: 100%;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #000;
      }
      #timer-shell {
        width: 100%;
        text-align: center;
        padding: 20px;
      }
      #timer-label {
        font-size: clamp(18px, 2.8vh, 36px);
        text-transform: uppercase;
        letter-spacing: 0.10em;
        margin-bottom: 10px;
      }
      #timer-value {
        font-size: {display_font};
        line-height: 0.9;
        font-weight: 800;
        letter-spacing: 0.08em;
        white-space: nowrap;
      }
      #controls {
        margin-top: 22px;
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
      }
      #controls button {
        padding: 10px 18px;
        font-size: 18px;
        border-radius: 8px;
        border: 1px solid #fff;
        background: #111;
        color: #fff;
        cursor: pointer;
      }
      .hidden {
        display: none !important;
      }
      .notice {
        color: #ffd54f;
        font-weight: 700;
        margin-bottom: 16px;
        font-size: 16px;
      }
    </style>

    <div id="timer-root">
      <div id="timer-shell">
        <div class="notice">Click "Enable sound" before starting.</div>
        <div id="timer-label">{timer_mode}</div>
        <div id="timer-value">00:00</div>
        <div id="controls">
          <button id="enable-sound">Enable sound</button>
          <button id="start">Start</button>
          <button id="pause">Pause</button>
          <button id="resume">Resume</button>
          <button id="reset">Reset</button>
          <button id="fullscreen">Fullscreen</button>
        </div>
      </div>
    </div>

    <script>
      const MODE = '{timer_mode}';
      const TOTAL_SECONDS = {total_seconds};
      let remaining = TOTAL_SECONDS;
      let elapsed = 0;
      let intervalId = null;
      let audioCtx = null;
      let finished = false;
      let alarmInterval = null;

      const valueEl = document.getElementById('timer-value');
      const labelEl = document.getElementById('timer-label');
      const rootEl = document.getElementById('timer-root');

      function formatClock(totalSeconds) {
        const mins = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
        const secs = (totalSeconds % 60).toString().padStart(2, '0');
        return `${mins}:${secs}`;
      }

      function updateDisplay() {
        if (MODE === 'Countdown') {
          valueEl.textContent = formatClock(remaining);
        } else {
          valueEl.textContent = formatClock(elapsed);
        }
      }

      function ensureAudio() {
        if (!audioCtx) {
          const AudioCtor = window.AudioContext || window.webkitAudioContext;
          if (!AudioCtor) {
            return null;
          }
          audioCtx = new AudioCtor();
        }
        if (audioCtx.state === 'suspended') {
          audioCtx.resume();
        }
        return audioCtx;
      }

      function _playBeepOnce(freq=880, duration=0.25) {
        const ctx = ensureAudio();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        gain.gain.value = 0.0001;
        osc.connect(gain);
        gain.connect(ctx.destination);
        const now = ctx.currentTime;
        gain.gain.exponentialRampToValueAtTime(0.2, now + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
        osc.start(now);
        osc.stop(now + duration + 0.02);
      }

      function playAlarm() {
        if (alarmInterval) {
          clearInterval(alarmInterval);
          alarmInterval = null;
        }

        const pattern = [880, 660, 880];
        let index = 0;
        alarmInterval = setInterval(() => {
          if (index >= pattern.length) {
            index = 0;
          }
          _playBeepOnce(pattern[index], 0.35);
          index += 1;
        }, 500);
      }

      function playTest() {
        _playBeepOnce(1000, 0.12);
      }

      function flashComplete() {
        const flashEl = document.createElement('div');
        flashEl.style.position = 'fixed';
        flashEl.style.top = '0';
        flashEl.style.left = '0';
        flashEl.style.width = '100vw';
        flashEl.style.height = '100vh';
        flashEl.style.zIndex = '2147483647';
        flashEl.style.pointerEvents = 'none';
        document.body.appendChild(flashEl);

        let flashes = 0;
        const interval = setInterval(() => {
          flashEl.style.background = (flashes % 2 === 0) ? '#fff176' : '#ff5252';
          flashEl.style.opacity = '0.95';
          flashes += 1;
          if (flashes > 9) {
            clearInterval(interval);
            flashEl.remove();
          }
        }, 300);
      }

      function finishTimer() {
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
        finished = true;
        if (MODE === 'Countdown') {
          playAlarm();
          flashComplete();
          valueEl.textContent = '00:00';
          labelEl.textContent = 'TIME!';
        } else {
          playAlarm();
          flashComplete();
        }
      }

      function tickCountdown() {
        if (remaining <= 0) {
          finishTimer();
          return;
        }
        remaining -= 1;
        updateDisplay();
        if (remaining <= 0) {
          finishTimer();
        }
      }

      function tickCountUp() {
        elapsed += 1;
        updateDisplay();
      }

      function startTimer() {
        if (intervalId) return;
        ensureAudio();
        if (finished) {
          remaining = TOTAL_SECONDS;
          elapsed = 0;
          finished = false;
          labelEl.textContent = MODE;
        }
        if (MODE === 'Countdown') {
          if (remaining <= 0) {
            remaining = TOTAL_SECONDS;
          }
          labelEl.textContent = 'Countdown';
          updateDisplay();
          intervalId = setInterval(tickCountdown, 1000);
        } else {
          elapsed = 0;
          labelEl.textContent = 'Count Up';
          updateDisplay();
          intervalId = setInterval(tickCountUp, 1000);
        }
      }

      function pauseTimer() {
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
      }

      function resetTimer() {
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
        if (alarmInterval) {
          clearInterval(alarmInterval);
          alarmInterval = null;
        }
        remaining = TOTAL_SECONDS;
        elapsed = 0;
        finished = false;
        labelEl.textContent = MODE;
        updateDisplay();
      }

      document.getElementById('enable-sound').onclick = function() {
        ensureAudio();
        playTest();
        const btn = document.getElementById('enable-sound');
        btn.textContent = 'Sound enabled';
        setTimeout(() => btn.textContent = 'Enable sound', 1500);
      };

      document.getElementById('start').onclick = function() {
        startTimer();
      };
      document.getElementById('pause').onclick = function() {
        pauseTimer();
      };
      document.getElementById('resume').onclick = function() {
        if (intervalId) return;
        if (MODE === 'Countdown') {
          intervalId = setInterval(tickCountdown, 1000);
        } else {
          intervalId = setInterval(tickCountUp, 1000);
        }
      };
      document.getElementById('reset').onclick = function() {
        resetTimer();
      };

      document.getElementById('fullscreen').onclick = function() {
        if (rootEl.requestFullscreen) {
          rootEl.requestFullscreen();
        } else if (rootEl.webkitRequestFullscreen) {
          rootEl.webkitRequestFullscreen();
        } else if (rootEl.msRequestFullscreen) {
          rootEl.msRequestFullscreen();
        }
      };

      updateDisplay();
    </script>
    """

    html = html_template.replace('{display_font}', display_font).replace('{timer_mode}', timer_mode).replace('{total_seconds}', str(total_seconds))
    st.components.v1.html(html, height=height_px)

if start_button:
    st.rerun()
