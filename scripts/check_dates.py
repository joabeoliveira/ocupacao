import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_db_url():
    db_url = os.getenv('DATABASE_URL')
    if db_url:
        if db_url.startswith('mysql://'):
            db_url = db_url.replace('mysql://', 'mysql+pymysql://')
        return db_url
    # fallback to individual vars (same as app.py)
    DB_HOST = os.getenv('DB_HOST', 'site_nir')
    DB_USER = os.getenv('DB_USER', 'joabeoliveira')
    DB_PASS = os.getenv('DB_PASSWORD', '114211Jo')
    DB_NAME = os.getenv('DB_NAME', 'nir')
    DB_PORT = os.getenv('DB_PORT', '3306')
    return f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

if __name__ == '__main__':
    db_url = get_db_url()
    print('Using DB URL (hidden):', db_url.split('@')[-1])
    engine = create_engine(db_url)
    dates = ['2026-01-05', '2026-05-01']
    with engine.connect() as conn:
        for d in dates:
            cnt = conn.execute(text("SELECT COUNT(*) FROM historico_ocupacao_completo WHERE data_referencia = :d"), {"d": d}).scalar()
            print(f"Count for {d}: {cnt}")
        print('\nSample rows for 2026-01-05:')
        rows = conn.execute(text("SELECT id, data_referencia, prontuario, cns_paciente, nome_paciente FROM historico_ocupacao_completo WHERE data_referencia = :d LIMIT 10"), {"d": '2026-01-05'}).mappings().all()
        for r in rows:
            print(dict(r))

    print('\nDone')
