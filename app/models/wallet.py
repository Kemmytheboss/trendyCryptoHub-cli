from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
import uuid


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    balance = Column(Float, default=0.0)
    total_deposited = Column(Float, default=0.0)

    deposit_address = Column(String, unique=True, index=True)

    withdrawal_amount = Column(Float, default=0.0)
    withdrawal_address = Column(String, nullable=True)
    withdrawal_pending = Column(Boolean, default=False)

    user = relationship("User", back_populates="wallets")

    # ------------------ DEPOSIT ADDRESS ------------------
    def generate_deposit_address(self):
        """Creates a unique deposit address."""
        address = str(uuid.uuid4())
        self.deposit_address = address
        return address

    # ------------------ DEPOSIT FUNDS ------------------
    def deposit(self, amount):
        """Increase wallet balance and total deposit history."""
        if amount <= 0:
            return False, "Invalid deposit amount"

        self.balance += amount
        self.total_deposited += amount

        return True, f"Deposited {amount} USDT"

    # ------------------ WITHDRAW REQUEST ------------------
    def request_withdrawal(self, amount, address):
        if amount > self.balance:
            return False, "Insufficient balance"

        self.withdrawal_amount = amount
        self.withdrawal_address = address
        self.withdrawal_pending = True

        return True, "Withdrawal request submitted"

    # ------------------ APPROVE WITHDRAWAL ------------------
    def approve_withdrawal(self):
        if not self.withdrawal_pending:
            return False, "No pending withdrawal"

        if self.withdrawal_amount > self.balance:
            return False, "Insufficient balance"

        # Deduct balance
        self.balance -= self.withdrawal_amount

        approved_amount = self.withdrawal_amount
        approved_address = self.withdrawal_address

        # Reset fields
        self.withdrawal_pending = False
        self.withdrawal_amount = 0.0
        self.withdrawal_address = None

        return True, f"Withdrawal of {approved_amount} sent to {approved_address}"
