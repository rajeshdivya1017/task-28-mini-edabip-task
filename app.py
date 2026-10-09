import math
import os
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional

from dotenv import load_dotenv

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Query,
    status
)

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import (
    OAuth2PasswordBearer
)

from jose import (
    JWTError,
    jwt
)

from passlib.context import CryptContext

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)

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
    create_engine,
    extract,
    or_
)

from sqlalchemy.orm import (
    Session,
    declarative_base,
    sessionmaker
)


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "development-secret"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
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


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


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
        nullable=False,
        index=True
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
        nullable=False
    )

    transaction_date = Column(
        Date,
        nullable=False
    )

    created_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp()
    )


class SignupRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):

    access_token: str

    token_type: str

    user: UserResponse


class KPIResponse(BaseModel):

    total_revenue: Decimal

    active_users: int

    total_orders: int


class TrendResponse(BaseModel):

    month: str

    revenue: Decimal


class TransactionResponse(BaseModel):

    id: int

    order_number: str

    customer_name: str

    category: str

    amount: Decimal

    status: str

    transaction_date: date


class TransactionListResponse(BaseModel):

    items: list[TransactionResponse]

    total: int

    page: int

    page_size: int

    total_pages: int


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
    password: str
) -> str:

    return pwd_context.hash(
        password
    )


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)


def create_access_token(
    user_id: int
):

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    ),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get(
            "sub"
        )

        if not user_id:
            raise credentials_exception

        user = (
            db.query(User)
            .filter(
                User.id == int(user_id)
            )
            .first()
        )

        if not user:
            raise credentials_exception

        if not user.is_active:

            raise HTTPException(
                status_code=403,
                detail="User account is inactive"
            )

        return user

    except (
        JWTError,
        ValueError
    ):

        raise credentials_exception


app = FastAPI(
    title="EDABIP Mini Enterprise Analytics Dashboard",
    description="Task 28 Analytics Dashboard API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        FRONTEND_URL
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)

@app.get("/")
def root():

    return {
        "message":
        "EDABIP Task 28 API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.post(
    "/api/auth/signup",
    response_model=UserResponse,
    status_code=201
)
def signup(
    payload: SignupRequest,
    db: Session = Depends(get_db)
):

    email = payload.email.lower().strip()

    existing_user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        name=payload.name.strip(),

        email=email,

        password_hash=hash_password(
            payload.password
        ),

        is_active=True
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


@app.post(
    "/api/auth/login",
    response_model=TokenResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    email = payload.email.lower().strip()

    user = (
        db.query(User)
        .filter(
            User.email == email
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        payload.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        user.id
    )

    return {
        "access_token":
            access_token,

        "token_type":
            "bearer",

        "user":
            user
    }

@app.get(
    "/api/auth/me",
    response_model=UserResponse
)
def current_user(
    user: User = Depends(
        get_current_user
    )
):

    return user


@app.get(
    "/api/dashboard/kpis",
    response_model=KPIResponse
)
def dashboard_kpis(
    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    )
):

    total_revenue = (
        db.query(
            func.coalesce(
                func.sum(
                    Transaction.amount
                ),
                0
            )
        )
        .filter(
            Transaction.status ==
            "Completed"
        )
        .scalar()
    )

    total_orders = (
        db.query(Transaction)
        .filter(
            Transaction.status !=
            "Cancelled"
        )
        .count()
    )

    active_users = (
        db.query(User)
        .filter(
            User.is_active == True
        )
        .count()
    )

    return {
        "total_revenue":
            total_revenue,

        "active_users":
            active_users,

        "total_orders":
            total_orders
    }


@app.get(
    "/api/dashboard/trend",
    response_model=list[TrendResponse]
)
def revenue_trend(
    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    )
):

    rows = (
        db.query(
            extract(
                "month",
                Transaction.transaction_date
            ).label("month"),

            func.sum(
                Transaction.amount
            ).label("revenue")
        )
        .filter(
            Transaction.status ==
            "Completed"
        )
        .group_by(
            extract(
                "month",
                Transaction.transaction_date
            )
        )
        .order_by(
            extract(
                "month",
                Transaction.transaction_date
            )
        )
        .all()
    )

    month_names = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ]

    result = []

    for row in rows:

        month_number = int(
            row.month
        )

        result.append({
            "month":
                month_names[
                    month_number
                ],

            "revenue":
                row.revenue
        })

    return result



@app.get(
    "/api/transactions",
    response_model=TransactionListResponse
)
def get_transactions(

    search: Optional[str] = Query(
        default=None
    ),

    category: Optional[str] = Query(
        default=None
    ),

    start_date: Optional[date] = Query(
        default=None
    ),

    end_date: Optional[date] = Query(
        default=None
    ),

    page: int = Query(
        default=1,
        ge=1
    ),

    page_size: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),

    user: User = Depends(
        get_current_user
    )
):

    query = (
        db.query(
            Transaction,
            User.name
        )
        .join(
            User,
            Transaction.user_id ==
            User.id
        )
    )


    if search:

        search_term = (
            f"%{search.strip()}%"
        )

        query = query.filter(
            or_(
                Transaction.order_number.ilike(
                    search_term
                ),

                User.name.ilike(
                    search_term
                ),

                Transaction.category.ilike(
                    search_term
                )
            )
        )


    if category and category != "All":

        query = query.filter(
            Transaction.category ==
            category
        )


    if start_date:

        query = query.filter(
            Transaction.transaction_date
            >= start_date
        )



    if end_date:

        query = query.filter(
            Transaction.transaction_date
            <= end_date
        )

    total = query.count()
    total_pages = max(
        1,
        math.ceil(
            total / page_size
        )
    )

    offset = (
        (page - 1)
        * page_size
    )


    results = (
        query
        .order_by(
            Transaction.transaction_date.desc()
        )
        .offset(offset)
        .limit(page_size)
        .all()
    )


    items = []

    for transaction, customer_name in results:

        items.append({
            "id":
                transaction.id,

            "order_number":
                transaction.order_number,

            "customer_name":
                customer_name,

            "category":
                transaction.category,

            "amount":
                transaction.amount,

            "status":
                transaction.status,

            "transaction_date":
                transaction.transaction_date
        })


    return {
        "items":
            items,

        "total":
            total,

        "page":
            page,

        "page_size":
            page_size,

        "total_pages":
            total_pages
    }



if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )