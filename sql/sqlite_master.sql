insert into main.sqlite_master (type, name, tbl_name, rootpage, sql) values ('table', 'functions', 'functions', 2, 'CREATE TABLE functions (
               id INTEGER PRIMARY KEY,
               name TEXT
           )');
insert into main.sqlite_master (type, name, tbl_name, rootpage, sql) values ('table', 'commands', 'commands', 3, 'CREATE TABLE commands (
            id INTEGER PRIMARY KEY,
            func TEXT,
            input TEXT,
            output TEXT
        )');
insert into main.sqlite_master (type, name, tbl_name, rootpage, sql) values ('table', 'objects', 'objects', 4, 'CREATE TABLE objects (
                id INTEGER PRIMARY KEY,
                func TEXT,
                input TEXT,
                output TEXT
            )');
