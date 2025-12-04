TrendyCryptoHub CLI — Phase 3 Project

TrendyCryptoHub-CLI is a command-line application built in Python to simulate basic crypto-hub operations such as user management, wallet tracking, transaction logging, prediction checks, dashboard navigation, and running a local trading backtest engine.

This project is built to satisfy all Phase 3 requirements, including:

A fully functional ORM-based SQLite database

Multiple models with one-to-one, one-to-many, and many-to-many relationships

A complete menu-driven CLI with CRUD operations

Proper organization using OOP principles and Python module structure

Alembic-powered migrations & Pipenv environment

🚀 Project Summary (3 lines)

A CLI-driven crypto hub where users can manage accounts, wallets, transactions, roles, dashboards and basic prediction checks.

Built using Python 3.8, SQLAlchemy ORM, Alembic migrations, and a modular CLI architecture.

Includes a simple trading bot and backtesting engine with sample market data handling.

🧑‍💻 MVP User Stories

As a user, I can create an account

As a user, I can fetch deposit addresses for different networks

As a user, I can check the market feed (mocked API)

As a user, I can view prediction direction for any listed coin

As a user, I can see my dashboard

As a user, I can see social feeds from Reddit

📂 Folder Structure
trendyCryptoHub-cli/
├── Pipfile
├── Pipfile.lock
├── README.md
├── alembic.ini
├── migrations/
│   ├── env.py
│   └── versions/
│       └── 001_create_initial_tables.py
├── app/
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── profile.py
│   │   ├── wallet.py
│   │   ├── transaction.py
│   │   ├── user_role.py
│   │   └── __init__.py
│   ├── ai/
│   │   └── trading_bot.py
│   └── services/
│       ├── data_fetcher.py
│       └── reddit_feed.py
└── lib/
    ├── cli.py
    ├── helpers.py
    ├── debug.py
    └── models/
        └── model_placeholder.py

🧱 Data Model Overview
✔ One-to-One

User → Profile

✔ One-to-Many

User → Wallets

User → Transactions

✔ Many-to-Many

User ⇄ Role
via user_roles association table

🛠 Setup Instructions
1. Install environment (Pipenv)
pipenv install
pipenv shell


OR standard venv:

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. Run Alembic migration
alembic upgrade head


This creates all database tables in:

database.db

3. Start the CLI
python lib/cli.py

🎮 CLI Menu Example
Welcome to TrendyCryptoHub CLI

Please select an option:
1. Create user
2. List users
3. Run backtest
0. Exit


Every menu option triggers functions in lib/helpers.py.

❇️ Models Included

User

Profile

Wallet

Transaction

Role

user_roles (association table)

Each model includes:

create()

get_all()

find_by_id()

optional helpers like find_by_email()

📊 Backtesting Engine

The trading bot implements:

SMA-based BUY/SELL strategy

Trading logs

Equity curve

Return % calculations

🔌 Mock API Services

Located in:

app/services/


data_fetcher.py — fetches sample market feeds

reddit_feed.py — mock Reddit posts

These can be replaced with real APIs later.

🧪 Testing

Use:

python lib/debug.py


Or just run CLI and try all the menu options.

📝 Phase 3 Requirements Checklist
Requirement	Status
2+ models	✅
One-to-one	✅
One-to-many	✅
Many-to-many	✅
ORM CRUD methods	✅
CLI with menus	✅
Input validation	✅
OOP structure	✅
Alembic migrations	✅
README included	✅
📄 License

This project is open for educational and portfolio use.

🧩 Future Enhancements

Real Binance API market data

Sentiment scoring using Reddit feed

Advanced AI predictions

Richer dashboard output

Better transaction analytics