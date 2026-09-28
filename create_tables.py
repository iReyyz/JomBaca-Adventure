import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.models import db

app = create_app()

def init_db():
    print("Menghubungi database Supabase dan mencipta jadual (tables)...")
    with app.app_context():
        try:
            db.create_all()
            print("BERHASIL! Semua jadual telah berjaya dicipta dalam Supabase!")
        except Exception as e:
            print(f"Ralat semasa mencipta jadual: {e}")

if __name__ == '__main__':
    init_db()
