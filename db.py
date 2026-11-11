import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / 'meetings.db'

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row #row객체 설정
    return conn

def init_db() -> None: # fastapi 연결 후 db 비어있으면 생성
    with get_connection() as conn:
        conn.execute(
            """
            create table if not exists meetings(
                id integer primary key autoincrement,
                title varchar(1000) not null,
                people varchar(1000) not null,
                notes text not null,
                actions text not null,
                result text not null,
                created_at varchar(100) not null
            )
            """
        )
        conn.commit()

def save_meeting(title:str, people:str, notes:str, summary:str, actions:str, result:str) -> int:
    created_at = datetime.now(timezone.utc).isoformat(timespec='seconds')
    with get_connection() as conn:
        cursor = conn.execute(
            """
            insert into meetings (title,people,notes,summary,actions,result,created_at) values (?,?,?,?,?,?,?)
            """, (title, people,notes,summary,actions,result,created_at)
        )
        conn.commit()
        return int(cursor.lastrowid)