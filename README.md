# pipelines
 pipelines + data jako plikow CSV/SQL przechowujących dane i informacje o workflows w pipelines, czyli kolejnych procesów wykonywanych przy wykorzystaniu np bashowych  i pythonowych skryuptow

Automatyzer.com

```bash
python -m venv myenv
source myenv/bin/activate
```

```python
python --version
pip list
pip install --upgrade pip
```

```python
pip install cloudflare
pip install python-dotenv
pip list
```

```python
python check_and_remove_domain.py zlece.net
python check_and_remove_domain.py apipong.com
```

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
     -H "Authorization: Bearer mjM7BfYmzhI7HvtxwoTpOEi6_WCKod-rLjTw8A5R" \
     -H "Content-Type: application/json"
```

logowanie na 
pobieranie



stwrz skrypt python, ktory pobierze kolejne linie z pliku CSV pipelines.csv, gdzie kolejno sa kolumny jako zmienne: FUNC, IN, OUT. Func to nazwa uruchamianej komendy bash z parametrami  pobieranymi z query przechowywanym w IN, ktore trzeba wczesniej uruchomic w lokalnej bazie SQLite oraz zapisac wynik funkcji za pomoc query SQL przechowywanym w OUT. Stworz baze SQLITE z przykladowym wierszem oraz przykladowy plik pipelines.csv z przykladowymi funkcjami do uzycia z FUNC



