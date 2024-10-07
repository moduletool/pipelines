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

CREATE TABLE flow_function (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flow_id INTEGER,
    function_id INTEGER,
    FOREIGN KEY (flow_id) REFERENCES flows(id),
    FOREIGN KEY (function_id) REFERENCES functions(id)
);

CREATE TABLE flow_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flow_id INTEGER,
    value TEXT,
    type TEXT,
    FOREIGN KEY (flow_id) REFERENCES flows(id)
);