from flask_sqlalchemy import SQLAlchemy
from sshtunnel import SSHTunnelForwarder

# SSH credentials
SSH_HOST = '192.168.1.152'
SSH_PORT = 22
SSH_USER = 'jed'
SSH_PASSWORD = 'etx203ax2023'  # 🔐

# Database credentials
DB_USER = 'jed'
DB_PASSWORD = 'password'
DB_NAME = 'billing_history'
REMOTE_DB_HOST = '127.0.0.1'  # Typically localhost if DB is on same server
REMOTE_DB_PORT = 3306

# Create SSH tunnel
server = SSHTunnelForwarder(
    (SSH_HOST, SSH_PORT),
    ssh_username=SSH_USER,
    ssh_password=SSH_PASSWORD,
    remote_bind_address=(REMOTE_DB_HOST, REMOTE_DB_PORT),
    local_bind_address=('127.0.0.1', 10022)  # Use a safe unused port
)

server.start()

# SQLAlchemy DB URI using the local tunnel
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:{server.local_bind_port}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Initialize SQLAlchemy
db = SQLAlchemy()
