# timer_tools

Collection of timers to use in the classroom.

This repository now includes a user-friendly Streamlit timer for classroom presentation. It supports:
- separate minute and second inputs
- a very large display
- a sound alarm when the timer finishes
- a visual flash on completion
- fullscreen support for display use

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

Then open the local Streamlit URL shown in the terminal.
