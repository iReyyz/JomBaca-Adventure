import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.models import db

app = create_app()

from sqlalchemy import text

def init_db():
    print("Menghubungi database Supabase dan mencipta / mengemaskini lajur (tables)...")
    with app.app_context():
        try:
            db.create_all()
            
            # Tambah lajur baru ke jadual users jika belum wujud
            alter_queries = [
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar VARCHAR(50) DEFAULT '👶🏼';",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS exp_boost_until TIMESTAMP WITHOUT TIME ZONE;",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_daily_date VARCHAR(20);"
            ]
            for query in alter_queries:
                db.session.execute(text(query))
            db.session.commit()
            
            print("BERHASIL! Semua jadual dan lajur baru (avatar, exp_boost_until, last_daily_date) telah berjaya dikemaskini dalam Supabase!")
        except Exception as e:
            print(f"Ralat semasa mencipta/mengemaskini jadual: {e}")

if __name__ == '__main__':
    init_db()
