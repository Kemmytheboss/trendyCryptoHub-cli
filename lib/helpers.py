from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.role import Role
from app.models.wallet import Wallet
from app.models.transaction import Transaction
from app.ai.trading_bot import TradingBot

# Ensure all tables exist
Base.metadata.create_all(bind=engine)


# ------------------ CREATE ADMIN ROLE IF MISSING ------------------
def ensure_admin_role():
    db = SessionLocal()
    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()

    if not admin_role:
        admin_role = Role(name="ADMIN")
        db.add(admin_role)
        db.commit()
        print("ADMIN role created.")

    db.close()


ensure_admin_role()


# ------------------ RECORD TRANSACTION ------------------
def record_transaction(db, user_id, tx_type, amount, asset="USDT"):
    tx = Transaction(
        user_id=user_id,
        tx_type=tx_type,
        amount=amount,
        asset=asset
    )
    db.add(tx)
    db.commit()
    return tx


# ------------------ MENU ------------------
def show_main_menu():
    print("\n===== TrendyCryptoHub CLI =====")
    print("0. Exit")
    print("1. Create user")
    print("2. List users")
    print("3. Run backtest (sample)")
    print("4. Get deposit address")
    print("5. Request withdrawal")
    print("6. Approve withdrawal (ADMIN ONLY)")
    print("7. List user transactions")
    print("8. Make user ADMIN")
    print("================================")


# ------------------ CREATE USER ------------------
def create_user_flow():
    db = SessionLocal()

    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    if User.find_by_email(db, email):
        print("❌ User already exists.")
        db.close()
        return

    user = User.create(db, email=email, password=password)

    wallet = Wallet(user_id=user.id)
    wallet.generate_deposit_address()
    db.add(wallet)
    db.commit()

    print(f"✅ User created with ID {user.id}")
    print(f"💼 Wallet deposit address: {wallet.deposit_address}")

    # Record user registration
    record_transaction(db, user.id, "ACCOUNT_CREATE", 0)

    db.close()


# ------------------ LIST USERS ------------------
def list_users_flow():
    db = SessionLocal()
    users = User.get_all(db)

    print("\n===== USERS =====")
    for u in users:
        roles = ", ".join([r.name for r in u.roles]) if u.roles else "None"
        print(f"ID: {u.id} | Email: {u.email} | Roles: {roles}")

    db.close()


# ------------------ GET DEPOSIT ADDRESS ------------------
def get_deposit_address_flow():
    db = SessionLocal()
    user_id = int(input("Enter User ID: "))

    user = User.find_by_id(db, user_id)
    if not user:
        print("❌ User not found.")
        return

    wallet = user.wallets[0]

    if not wallet.deposit_address:
        wallet.generate_deposit_address()
        db.commit()

    print(f"💰 Deposit Address: {wallet.deposit_address}")

    db.close()

# -----------------DEPOSIT FLOW---------------------------
def deposit_funds_flow():
    db = SessionLocal()

    user_id = int(input("Enter User ID: "))
    amount = float(input("Enter deposit amount: "))

    user = User.find_by_id(db, user_id)
    if not user:
        print("❌ User not found.")
        db.close()
        return

    wallet = user.wallets[0]

    success, msg = wallet.deposit(amount)
    db.commit()

    if success:
        print(f"✅ {msg}")
        record_transaction(db, user.id, "DEPOSIT", amount)
    else:
        print(f"❌ Deposit failed")

    db.close()


# ------------------ REQUEST WITHDRAWAL ------------------
def request_withdrawal_flow():
    db = SessionLocal()
    user_id = int(input("Enter User ID: "))
    amount = float(input("Withdrawal Amount: "))
    address = input("Withdrawal Address: ").strip()

    user = User.find_by_id(db, user_id)
    if not user:
        print("❌ User not found.")
        return

    wallet = user.wallets[0]
    success, msg = wallet.request_withdrawal(amount, address)
    db.commit()

    if success:
        print(f"✅ {msg}")
        record_transaction(db, user.id, "WITHDRAW_REQUEST", amount)
    else:
        print(f"❌ {msg}")

    db.close()


# ------------------ APPROVE WITHDRAWAL (ADMIN ONLY) ------------------
def approve_withdrawal_flow():
    db = SessionLocal()

    admin_id = int(input("Enter Admin User ID: "))
    admin = User.find_by_id(db, admin_id)

    if not admin:
        print("❌ Admin user not found.")
        return

    roles = [r.name for r in admin.roles]
    if "ADMIN" not in roles:
        print("❌ NOT AUTHORIZED. ADMIN role required.")
        return

    user_id = int(input("Enter User ID to approve withdrawal for: "))
    user = User.find_by_id(db, user_id)

    if not user:
        print("❌ User not found.")
        return

    wallet = user.wallets[0]

    approved_amount = wallet.withdrawal_amount  # Capture BEFORE reset
    success, msg = wallet.approve_withdrawal()
    db.commit()

    if success:
        print(f"✅ {msg}")
        record_transaction(db, user.id, "WITHDRAW_APPROVED", approved_amount)
    else:
        print(f"❌ {msg}")

    db.close()


# ------------------ LIST USER TRANSACTIONS ------------------
def list_transactions_flow():
    db = SessionLocal()

    user_id = int(input("Enter User ID: "))
    user = User.find_by_id(db, user_id)

    if not user:
        print("❌ User not found.")
        return

    print(f"\n===== TRANSACTIONS FOR USER {user_id} =====")
    for tx in user.transactions:
        print(f"TX#{tx.id} | {tx.tx_type} | Amount: {tx.amount} | Asset: {tx.asset}")

    db.close()


# ------------------ MAKE USER ADMIN ------------------
def make_admin_flow():
    db = SessionLocal()

    user_id = int(input("Enter User ID to promote to ADMIN: "))
    user = User.find_by_id(db, user_id)

    if not user:
        print("❌ User not found.")
        db.close()
        return

    admin_role = db.query(Role).filter(Role.name == "ADMIN").first()

    if admin_role not in user.roles:
        user.roles.append(admin_role)
        db.commit()
        print(f"✅ User {user_id} is now an ADMIN!")
    else:
        print("ℹ User is already ADMIN.")

    db.close()


# ------------------ BACKTEST ------------------
def backtest_flow():
    print("Running sample backtest...")
    bot = TradingBot()

    prices = [
        100, 102, 104, 108, 112, 118, 125, 130, 128, 135,
        140, 145, 150, 155, 160, 162, 165, 170, 175, 178,
        180, 185, 190, 200, 210, 220, 230, 225, 235, 245,
        255, 260, 270, 280, 290, 300, 310, 320, 315, 330,
        345, 360, 370, 380, 390, 405, 420, 410, 430, 450,
        470, 480, 500, 520, 540, 560, 580, 600
    ]

    result = bot.backtest(prices)

    print("\n===== BACKTEST RESULT =====")
    print("Initial Capital:", result["initial_capital"])
    print("Final Value:", result["final_value"])
    print("Return %:", result["total_return_pct"])
    print("Trades:", result["trades"])
