import hashlib
import hmac
import secrets
import sqlite3
import time
from pathlib import Path

from app.models.livro import Livro
from app.models.user_account import User_account


class DataRecord:
    """Persistência SQLite e sessões independentes por cliente."""

    def __init__(self, path, username, password):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.path = str(path)
        self.sessions = {}
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY, password_hash TEXT NOT NULL, salt TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL, autor TEXT NOT NULL);
            ''')
            if not db.execute('SELECT 1 FROM users LIMIT 1').fetchone():
                salt = secrets.token_hex(16)
                db.execute('INSERT INTO users VALUES (?, ?, ?)',
                           (username, self.hash_password(password, salt), salt))

    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    @staticmethod
    def hash_password(password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 260000).hex()

    def authenticate(self, username, password):
        with self.connect() as db:
            row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if row:
            user = User_account(**dict(row))
            if hmac.compare_digest(user.password_hash, self.hash_password(password, user.salt)):
                token = secrets.token_urlsafe(32)
                now = time.time()
                self.sessions = {key: value for key, value in self.sessions.items() if value[1] > now}
                self.sessions[token] = (user.username, now + 3600)
                return token
        return None

    def current_user(self, token):
        session = self.sessions.get(token)
        if session and session[1] > time.time():
            return session[0]
        self.sessions.pop(token, None)
        return None

    def logout(self, token):
        self.sessions.pop(token, None)

    def list_books(self):
        with self.connect() as db:
            return [Livro(**dict(row)) for row in db.execute('SELECT * FROM livros ORDER BY id')]

    def create_book(self, titulo, autor):
        with self.connect() as db:
            cursor = db.execute('INSERT INTO livros (titulo, autor) VALUES (?, ?)', (titulo, autor))
            return Livro(cursor.lastrowid, titulo, autor)

    def update_book(self, book_id, titulo, autor):
        with self.connect() as db:
            return db.execute('UPDATE livros SET titulo=?, autor=? WHERE id=?',
                              (titulo, autor, book_id)).rowcount > 0

    def delete_book(self, book_id):
        with self.connect() as db:
            return db.execute('DELETE FROM livros WHERE id=?', (book_id,)).rowcount > 0
