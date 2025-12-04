from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.user_role import user_roles
from app.ai.trading_bot import TradingBot

# ensure tables exist
Base.metadata.create_all(bind=engine)

def show_main_menu():
    print('\nPlease select an option:')
    print('0. Exit')
    print('1. Create user')
    print('2. List users')
    print('3. Run backtest (sample)')


def create_user_flow():
    db = SessionLocal()
    email = input('Email: ').strip()
    password = input('Password: ').strip()
    if User.find_by_email(db, email):
        print('User already exists')
        db.close()
        return
    user = User.create(db, email=email, password=password)
    print('Created user with id', user.id)
    db.close()


def list_users_flow():
    db = SessionLocal()
    users = User.get_all(db)
    for u in users:
        print(f"{u.id}: {u.email}")
    db.close()




def backtest_flow():
    print('Running sample backtest...')
    bot = TradingBot()
    prices = [100, 102, 101, 103, 104, 100, 98, 105]
    result = bot.backtest(prices)
    print('Backtest result:')
    print('Initial:', result['initial_capital'])
    print('Final:', result['final_value'])