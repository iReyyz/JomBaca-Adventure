# JomBaca Adventure 📚🎮

A gamified Bahasa Melayu reading learning web app for kids.

## Features
- 🔑 Login & Register system with kids user profile
- 🎮 Interactive Mini games (Kenal Huruf, Bina Perkataan, Dengar & Pilih)
- 📅 Daily tasks (Latihan harian)
- 🪙 Points & Coins reward system
- 🏆 Leaderboard (Score sharing)
- ⚔️ Battle mode (1 vs 1 real-time match)

## Tech Stack
- **Backend:** Python (Flask, Flask-SQLAlchemy, Flask-Login)
- **Frontend:** HTML5, CSS3 (Modern Responsive UI), JavaScript (Vanilla)
- **Database:** Supabase (PostgreSQL) / SQLite (Local fallback)

## Setup & Local Installation

### 1. Clone repo
```bash
git clone https://github.com/USERNAME/jom-baca-adventure.git
cd jom-baca-adventure
```

### 2. Create virtual environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Windows PowerShell:**
  ```powershell
  .\venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup `.env` file
Copy `.env.example` to `.env` and configure your Database URL and Secret Key:
```env
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your_secret_key_here
```

### 6. Run App
```bash
python app.py
```
Open browser at `http://127.0.0.1:5000`.
