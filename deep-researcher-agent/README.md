# Deep Researcher Agent - Ready Project

## Overview (Layman's terms)
The Deep Researcher Agent is a local AI assistant that helps you research documents you provide. 
- You paste or upload documents (papers, notes, articles).
- The system reads them, converts them into numeric summaries (embeddings), and stores them locally.
- When you ask a question, the system finds the most relevant parts and synthesizes an answer using a small text generation model.
- You can export the answer as a Markdown file.

This project runs **locally** (no external search APIs) and demonstrates retrieval + generation workflows.

## Features
- Local embedding generation using `sentence-transformers`.
- Fast similarity search using `faiss` (fallback to in-memory if faiss not available).
- Synthesis using a seq2seq model (`flan-t5-small`) via `transformers`.
- Simple futuristic frontend (single HTML page) for ingestion, querying, and export.

## Quick start (local)
1. Create Python environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # or venv\\Scripts\\activate on Windows
   pip install -r backend/requirements.txt
   ```
2. Run backend:
   ```bash
   cd backend
   python app.py
   ```
3. Open `frontend/index.html` in your browser (or serve it with a static server).

## Notes & Tips
- The first run will download models (sentence-transformers & transformers) which can take time and disk space.
- If `faiss-cpu` installation is problematic on some systems, the code will fall back to an in-memory similarity search (slower but works).
- For better generation quality, you may replace `flan-t5-small` with a larger model if you have GPU and RAM.

## Deployment on Render / Heroku
- Backend: Deploy the `backend` folder as a Python web service; set start command `python app.py`.
- Frontend: Host `frontend/index.html` on GitHub Pages, Netlify or serve from the backend as static files.

## What I delivered
- A ready-to-run repo with backend and a futuristic-styled frontend.
- Ingest/query/export flow implemented.

Good luck — ready to help you customize the UI or add file upload / PDF parsing and a demo script for the hackathon video! 🚀
