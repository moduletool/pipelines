insert into main.commands (id, func, input, output) values (1, 'SELECT name FROM functions LIMIT 1', 'SELECT input FROM objects WHERE id = 1', 'UPDATE objects SET output=(?) WHERE id = 1');
insert into main.commands (id, func, input, output) values (2, 'SELECT name FROM functions LIMIT 1', 'SELECT input FROM objects WHERE id = 2', 'UPDATE objects SET output=(?) WHERE id = 2');
