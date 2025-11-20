# Streamlit Application Module

Everything required to launch the Adaptive Learning demo lives inside this directory.

## Layout

- `main_app.py` – bootstraps the navigation flow and wires all pages/components together.
- `components/` – shared experiences such as the AI tutor panel and analytics dashboard.
- `pages/` – individual Streamlit pages (`landing`, `onboarding`, `roadmap_selection`, `data_engineer_roadmap`).
- `data/tutor_events.json` – persisted demo analytics so charts light up immediately.

## Run the full experience

```bash
streamlit run app/main_app.py
```

## Run a specific page (debugging)

```bash
streamlit run app/pages/landing.py
```

Swap `landing.py` for any other page module as needed.

