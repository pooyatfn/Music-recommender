CHECK_ANY_READY = """
    SELECT * FROM Request
    WHERE status = 'ready';
"""

UPDATE_STATUS = """
    UPDATE Request
    SET status = 'done'
    WHERE id = %s
    RETURNING id, email, status, song_id;
"""
