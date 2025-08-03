import sqlite3

from app.lib.data_access.short_url_repo import ShortUrlRepo
from app.models.short_url import ShortUrl


class SQLiteRepo(ShortUrlRepo):
    def __init__(self):
        super().__init__()
        with sqlite3.connect("mappings.db") as con:
            con.execute(
                "CREATE TABLE IF NOT EXISTS mappings(short_url_id varchar(255) PRIMARY KEY, long_url varchar(255) NOT NULL)"
            )
            con.commit()

    def get(self, short_url_id: str) -> ShortUrl | None:
        with sqlite3.connect("mappings.db") as con:
            con.row_factory = sqlite3.Row
            result = con.execute(
                "SELECT * FROM mappings WHERE short_url_id=?", (short_url_id,)
            )
            row = result.fetchone()
            if row is not None:
                return ShortUrl(short_url_id=short_url_id, long_url=row["long_url"])
            return None

    def set(self, short_url: ShortUrl) -> bool:
        try:
            with sqlite3.connect("mappings.db") as con:
                con.execute(
                    "INSERT INTO mappings VALUES (?, ?)",
                    (short_url.short_url_id, short_url.long_url),
                )
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return False

    def delete(self, short_url_id: str) -> bool:
        try:
            with sqlite3.connect("mappings.db") as con:
                con.execute(
                    "DELETE FROM mappings WHERE short_url_id=?", (short_url_id,)
                )
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return False

    def update(self, short_url_id: str, short_url: ShortUrl) -> bool:
        if not self.get(short_url_id):
            return False
        if short_url_id != short_url.short_url_id:
            result = self.set(short_url)
            if result:
                return self.delete(short_url_id)
            return result
        try:
            with sqlite3.connect("mappings.db") as con:
                con.execute(
                    "UPDATE mappings SET long_url=? WHERE short_url_id=?",
                    (short_url.long_url, short_url.short_url_id),
                )
                return True
        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")
            return False
