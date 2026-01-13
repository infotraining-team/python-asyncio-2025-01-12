import asyncio
import json
import httpx
import aiosqlite
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("DB_Archiver")

DB_NAME = "stream_data.db"
URL = "http://127.0.0.1:8000/stream-resume"

async def init_db(db):
    """Creates the table if it doesn't exist."""
    await db.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY,
            x INTEGER,
            y INTEGER,
            received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    await db.commit()

async def get_resume_id(db):
    """Finds the last ID stored in the DB so we can ask the server for new data."""
    async with db.execute("SELECT MAX(id) FROM measurements") as cursor:
        row = await cursor.fetchone()
        # If DB is empty, row[0] is None, so we return 0
        last_id = row[0] if row[0] is not None else 0
        logger.info(f"Database contains data up to ID: {last_id}")
        return last_id

async def archive_stream():
    # 1. Open the Database Connection (keep it open for the session)
    async with aiosqlite.connect(DB_NAME) as db:
        await init_db(db)

        retry_delay = 1

        while True:
            try:
                # 2. Check where we left off
                last_id = await get_resume_id(db)
                connect_url = f"{URL}?last_id={last_id}"

                logger.info(f"Connecting to {connect_url}...")

                async with httpx.AsyncClient(timeout=None) as client:
                    async with client.stream("GET", connect_url) as response:
                        if response.status_code != 200:
                            logger.error(f"Server returned {response.status_code}")
                            await asyncio.sleep(5)
                            continue

                        logger.info("Stream connected. Archiving data...")
                        retry_delay = 1

                        # 3. Process the Stream
                        async for line in response.aiter_lines():
                            if not line: continue

                            try:
                                msg = json.loads(line)

                                # 4. Insert into SQLite Asynchronously
                                await db.execute(
                                    "INSERT INTO measurements (id, x, y) VALUES (?, ?, ?)",
                                    (msg['id'], msg['x'], msg['y'])
                                )
                                # Commit immediately to ensure data safety if crash happens now
                                await db.commit()

                                print(f"Saved Record ID {msg['id']}")

                            except json.JSONDecodeError:
                                pass
                            except aiosqlite.IntegrityError:
                                # Handles rare case of duplicate IDs if server resends data
                                logger.warning(f"Duplicate ID {msg.get('id')} ignored.")

            except (httpx.RequestError, OSError) as e:
                logger.warning(f"Connection lost: {e}. Retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 30)

if __name__ == "__main__":
    try:
        asyncio.run(archive_stream())
    except KeyboardInterrupt:
        logger.info("Archiver stopped.")