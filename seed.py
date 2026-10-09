import os
from datetime import date

from dotenv import load_dotenv
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    TIMESTAMP,
    func,
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing from .env file"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String(255),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )

    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )



class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    order_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=False
    )

    amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    status = Column(
        Enum(
            "Completed",
            "Pending",
            "Cancelled"
        ),
        default="Completed"
    )

    transaction_date = Column(
        Date,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )

def seed_database():

    db = SessionLocal()

    try:

        print("Starting database seed...")
        db.query(Transaction).delete()
        db.query(User).delete()

        db.commit()
        users = [
            User(
                name="Admin User",
                email="admin@edabip.com",
                password_hash=hash_password(
                    "Admin@123"
                ),
                is_active=True
            ),

            User(
                name="John Doe",
                email="john@edabip.com",
                password_hash=hash_password(
                    "Password@123"
                ),
                is_active=True
            ),

            User(
                name="Jane Smith",
                email="jane@edabip.com",
                password_hash=hash_password(
                    "Password@123"
                ),
                is_active=True
            ),

            User(
                name="David Kumar",
                email="david@edabip.com",
                password_hash=hash_password(
                    "Password@123"
                ),
                is_active=True
            ),

            User(
                name="Priya Sharma",
                email="priya@edabip.com",
                password_hash=hash_password(
                    "Password@123"
                ),
                is_active=True
            )
        ]

        db.add_all(users)

        db.commit()

        for user in users:
            db.refresh(user)

        print("Users inserted successfully.")
     
        transactions = [

            Transaction(
                user_id=users[0].id,
                order_number="ORD-1001",
                category="Electronics",
                amount=12500.00,
                status="Completed",
                transaction_date=date(
                    2026, 1, 5
                )
            ),

            Transaction(
                user_id=users[1].id,
                order_number="ORD-1002",
                category="Furniture",
                amount=8500.00,
                status="Completed",
                transaction_date=date(
                    2026, 1, 12
                )
            ),

            Transaction(
                user_id=users[2].id,
                order_number="ORD-1003",
                category="Electronics",
                amount=15200.00,
                status="Completed",
                transaction_date=date(
                    2026, 2, 3
                )
            ),

            Transaction(
                user_id=users[3].id,
                order_number="ORD-1004",
                category="Clothing",
                amount=4500.00,
                status="Pending",
                transaction_date=date(
                    2026, 2, 15
                )
            ),

            Transaction(
                user_id=users[4].id,
                order_number="ORD-1005",
                category="Electronics",
                amount=21000.00,
                status="Completed",
                transaction_date=date(
                    2026, 3, 8
                )
            ),

            Transaction(
                user_id=users[0].id,
                order_number="ORD-1006",
                category="Furniture",
                amount=7800.00,
                status="Completed",
                transaction_date=date(
                    2026, 3, 19
                )
            ),

            Transaction(
                user_id=users[1].id,
                order_number="ORD-1007",
                category="Clothing",
                amount=6200.00,
                status="Completed",
                transaction_date=date(
                    2026, 4, 2
                )
            ),

            Transaction(
                user_id=users[2].id,
                order_number="ORD-1008",
                category="Electronics",
                amount=18900.00,
                status="Completed",
                transaction_date=date(
                    2026, 4, 17
                )
            ),

            Transaction(
                user_id=users[3].id,
                order_number="ORD-1009",
                category="Furniture",
                amount=9200.00,
                status="Cancelled",
                transaction_date=date(
                    2026, 5, 6
                )
            ),

            Transaction(
                user_id=users[4].id,
                order_number="ORD-1010",
                category="Clothing",
                amount=5600.00,
                status="Completed",
                transaction_date=date(
                    2026, 5, 21
                )
            ),

            Transaction(
                user_id=users[0].id,
                order_number="ORD-1011",
                category="Electronics",
                amount=24500.00,
                status="Completed",
                transaction_date=date(
                    2026, 6, 4
                )
            ),

            Transaction(
                user_id=users[1].id,
                order_number="ORD-1012",
                category="Furniture",
                amount=11200.00,
                status="Completed",
                transaction_date=date(
                    2026, 6, 18
                )
            ),

            Transaction(
                user_id=users[2].id,
                order_number="ORD-1013",
                category="Clothing",
                amount=6800.00,
                status="Pending",
                transaction_date=date(
                    2026, 7, 3
                )
            ),

            Transaction(
                user_id=users[3].id,
                order_number="ORD-1014",
                category="Electronics",
                amount=19800.00,
                status="Completed",
                transaction_date=date(
                    2026, 7, 15
                )
            ),

            Transaction(
                user_id=users[4].id,
                order_number="ORD-1015",
                category="Furniture",
                amount=13400.00,
                status="Completed",
                transaction_date=date(
                    2026, 8, 9
                )
            ),

            Transaction(
                user_id=users[0].id,
                order_number="ORD-1016",
                category="Clothing",
                amount=7200.00,
                status="Completed",
                transaction_date=date(
                    2026, 8, 22
                )
            ),

            Transaction(
                user_id=users[1].id,
                order_number="ORD-1017",
                category="Electronics",
                amount=27600.00,
                status="Completed",
                transaction_date=date(
                    2026, 9, 5
                )
            ),

            Transaction(
                user_id=users[2].id,
                order_number="ORD-1018",
                category="Furniture",
                amount=10500.00,
                status="Completed",
                transaction_date=date(
                    2026, 9, 18
                )
            ),

            Transaction(
                user_id=users[3].id,
                order_number="ORD-1019",
                category="Clothing",
                amount=4900.00,
                status="Pending",
                transaction_date=date(
                    2026, 9, 25
                )
            ),

            Transaction(
                user_id=users[4].id,
                order_number="ORD-1020",
                category="Electronics",
                amount=22100.00,
                status="Completed",
                transaction_date=date(
                    2026, 10, 1
                )
            )
        ]

        db.add_all(transactions)

        db.commit()

        print(
            "Transactions inserted successfully."
        )

        print("----------------------------------------")
        print("DATABASE SEED COMPLETED")
        print("----------------------------------------")
        print("Users       : 5")
        print("Transactions: 20")
        print("----------------------------------------")
        print("")
        print("Demo Login")
        print("Email   : admin@edabip.com")
        print("Password: Admin@123")
        print("----------------------------------------")

    except Exception as error:

        db.rollback()

        print(
            "SEED ERROR:",
            error
        )

    finally:

        db.close()


if __name__ == "__main__":
    seed_database()