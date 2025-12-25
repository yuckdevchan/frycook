CREATE TABLE pages (
    id   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    urlNoProtocol  TEXT NOT NULL UNIQUE
    https BOOLEAN NOT NULL
);

CREATE TABLE links (
    from_id INTEGER NOT NULL,
    to_id   INTEGER NOT NULL,
    PRIMARY KEY(from_id, to_id)
);

CREATE INDEX index_from_id ON links(from_id);
CREATE INDEX index_to_id ON links(to_id);
