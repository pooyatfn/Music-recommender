UPDATE_SONG_ID = """
    UPDATE Request
    SET song_id = %s, status = 'ready'
    WHERE id = %s
    RETURNING id, email, status, song_id;
"""
