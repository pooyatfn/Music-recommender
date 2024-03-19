CREATE_REQUEST_TABLE_IN_DBAAS = """
        CREATE TABLE IF NOT EXISTS Request (
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            song_id TEXT DEFAULT NULL
        )
        """

INSERT_DATA_INTO_REQUEST_TABLE = """
            INSERT INTO Request (email)
            VALUES (%s)
            RETURNING id, email, status, song_id;
            """
