CREATE TABLE functions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE flows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input TEXT,
    output TEXT
);

CREATE TABLE commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flow_id INTEGER,
    function_id INTEGER,
    FOREIGN KEY (flow_id) REFERENCES flows(id),
    FOREIGN KEY (function_id) REFERENCES functions(id)
);

CREATE TABLE command_objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command_id INTEGER,
    input TEXT,
    output TEXT,
    FOREIGN KEY (command_id) REFERENCES commands(id)
);