import os
from alembic.config import Config
from alembic import command

def run_alembic_migrations():
    # Bulunduğun dosyadan göreli yol oluştur
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ini_path = os.path.join(base_dir, 'alembic.ini')

    # Alembic yapılandırmasını yükle
    alembic_cfg = Config(ini_path)

    # Migrasyonları uygula (upgrade to head)
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_alembic_migrations()