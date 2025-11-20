# Renaissance Adaptive Learning Agent (POC)

This repository contains the Streamlit proof-of-concept that I built for the **Renaissance EdTech Platform** and submitted to the **MKTBA Hackathon – Fall 2025**. It showcases an **AI adaptive learning agent** that guides Business Analytics and Data Engineering learners through a branded experience inspired by Renaissance’s design language.

> ⚠️ **POC disclaimer:** This codebase is shared for educational purposes. It is not a production-ready product—there is no Supabase backend, vector database, or external orchestration. Everything runs locally inside Streamlit to demonstrate the concept quickly.

---

## What’s Included

- **Renaissance-themed UI flow**: landing, onboarding, roadmap selection, and a Data Engineer roadmap page (only the Business Analytics → Data Engineer branch is interactive today).
- **Adaptive AI Tutor panel**: lightweight OpenAI-powered interaction with a mock analytics log.
- **Learning analytics panel**: derives insights from sample tutor events stored on disk.
- **Self-contained assets**: logos, hero images, and profile art required for the demo.

---

## Run It Locally

1. **Install Python 3.9+**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Add your OpenAI key (optional but recommended for the tutor panel)**
   ```env
   # .env
   OPENAI_API_KEY=sk-your-key
   ```
4. **Launch Streamlit**
   ```bash
   streamlit run app/main_app.py
   ```

The entire experience runs offline except for OpenAI calls. No databases or third-party services are required to recreate the demo.

---

## Project Structure

```
Hackathon_Fall2025/
├── README.md
├── requirements.txt
├── .env.example
├── app/
│   ├── main_app.py          # Navigation + global state
│   ├── components/          # AI tutor + analytics panels
│   ├── pages/               # Landing, onboarding, roadmap, DE roadmap
│   └── data/tutor_events.json
└── assets/                  # Branding + imagery
```

- `app/data/tutor_events.json` contains pre-populated tutor logs so the analytics tab renders immediately; delete it to reset.
- `assets/` holds all Renaissance-branded visuals referenced by the pages.

---

## Tips for Remixing

- Swap out logos or imagery by replacing files inside `assets/`.
- Adjust roadmap content or copy within the corresponding file in `app/pages/`.
- Extend the tutor or analytics experiences inside `app/components/`; both modules are decoupled from external services.
- If you add other roadmaps, update the state machine in `app/main_app.py`; right now only the Business Analytics → Data Engineer path is wired end-to-end.

---

Thanks for checking out this POC. If you adapt it for other educational initiatives, please credit the original Renaissance EdTech + MKTBA Hackathon submission. 🎓

