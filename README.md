# Learn FastAPI – Product API

A small FastAPI app that saves products in a MySQL database.

## What you need first

- **Python 3.10 or newer** (check with `python3 --version`)
- **MySQL** running on your computer or on a server
- **Git**

## Steps to run on a new device

### 1. Get the code

```bash
git clone <repo-url>
cd fastapi
```

If you already have the folder, just run `git pull`.

### 2. Make a virtual environment

This keeps the project packages separate from the rest of your computer.

**Mac / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

You will see `(.venv)` at the start of your terminal line when it is on.

### 3. Install the packages

```bash
pip install -r requirements.txt
```

### 4. Make the database

Open MySQL and make an empty database. For example:

```sql
CREATE DATABASE fastapi_db;
```

You do **not** need to make the table. The app makes the `product` table by itself when it starts.

### 5. Make the `.env` file

The `.env` file is **not** in Git (it has your password), so you must make it yourself.

Make a file called `.env` in the project folder and put this inside:

```
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@localhost:3306/fastapi_db
```

Change `USERNAME`, `PASSWORD`, `localhost`, and `fastapi_db` to match your own MySQL.

### 6. Start the app

```bash
fastapi dev main.py
```

Now open your browser:

- App: http://127.0.0.1:8000
- API docs (you can test every endpoint here): http://127.0.0.1:8000/docs

The first time the app starts, it adds 4 sample products if the table is empty.

To stop the app, press `Ctrl + C`.

## Next time you work on it

You only need to do this:

```bash
cd fastapi
git pull
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt   # only if requirements.txt changed
fastapi dev main.py
```

## Endpoints

| Method | Path             | What it does          |
| ------ | ---------------- | --------------------- |
| GET    | `/`              | Say hello             |
| GET    | `/products`      | Get all products      |
| GET    | `/product/{id}`  | Get one product       |
| POST   | `/product`       | Add a new product     |
| PATCH  | `/products/{id}` | Change a product      |
| DELETE | `/products/{id}` | Delete a product      |

## Common problems

- **`KeyError: 'DATABASE_URL'`** – You forgot the `.env` file, or it is in the wrong folder. See step 5.
- **`Can't connect to MySQL server`** – MySQL is not running, or the host/port in `.env` is wrong.
- **`Access denied for user`** – Username or password in `.env` is wrong.
- **`Unknown database`** – You did not make the database yet. See step 4.
- **`command not found: fastapi`** – The virtual environment is not on. Run the `activate` command from step 2.
