# timer_tools

Collection of timers to use in the classroom.

This repository now includes a small Streamlit app that runs browser-based timers (countdown, interval, and Pomodoro). The timers are implemented as embeddable HTML/JavaScript so they run in the visitor's browser and do not block the Streamlit server.

How to run

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Notes
- The timers run client-side inside an HTML component; sound uses an external audio file and requires the browser to allow autoplay for the audio to play reliably.
- This is a minimal starting point; I can add presets, shared (server-side) timers, or a teacher dashboard next.
