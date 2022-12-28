import sqlite3

def create_db() -> None:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS notify(channel_id INTEGER PRIMARY KEY,to_notify INTEGER DEFAULT 0);")

    conn.commit()
    conn.close()

def change_notify_status(channel:int) -> bool:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM notify WHERE channel_id IN (?)'
    cursor.execute(query, (channel,))

    channels = cursor.fetchall()
    is_enabled = False
    if not channels:
        query = 'INSERT INTO notify (channel_id, to_notify) VALUES (?, ?)'
        cursor.execute(query, (channel, 1))
        conn.commit()
        is_enabled = True
    else:
        notif = not bool(channels[0][1])
        query = 'UPDATE notify SET to_notify = (?) WHERE channel_id = (?)'
        cursor.execute(query, (notif, channel))
        conn.commit()
        is_enabled = notif  

    cursor.close()
    conn.close()
    return is_enabled

def get_channels_to_notify() -> list[int]:
    conn = sqlite3.connect('./database.db')
    cursor = conn.cursor()

    query = 'SELECT channel_id FROM notify WHERE to_notify = 1'
    cursor.execute(query)
    channels = cursor.fetchall()

    cursor.close()
    conn.close()

    return [channel[0] for channel in channels]

if __name__ == "__main__":
    pass
