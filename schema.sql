CREATE TABLE functions (
    id INTEGER PRIMARY KEY,
    description TEXT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE flows (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE commands (
    id INTEGER PRIMARY KEY,
    flow_id INTEGER,
    function_id INTEGER,
    FOREIGN KEY (flow_id) REFERENCES flows(id),
    FOREIGN KEY (function_id) REFERENCES functions(id)
);

CREATE TABLE command_objects (
    id INTEGER PRIMARY KEY,
    command_id INTEGER,
    input TEXT,
    output TEXT,
    FOREIGN KEY (command_id) REFERENCES commands(id)
);