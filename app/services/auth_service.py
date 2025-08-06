from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.database.models import User, UserRole
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
)
from app.schemas.auth import UserCreate, UserLogin, Token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = (
            self.db.query(User).filter(User.email == user_data.email).first()
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="该邮箱已被注册，请使用其他邮箱或直接登录。如果您忘记密码，请联系管理员重置",
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            role=UserRole.CLIENT,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_login_error_details(self, email: str, password: str) -> tuple[str, str]:
        """Get specific error details for login failures"""
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            return (
                "EMAIL_NOT_FOUND",
                "该邮箱地址未注册，请先注册账户或检查邮箱地址是否正确",
            )

        if not verify_password(password, user.hashed_password):
            return (
                "INVALID_PASSWORD",
                "密码错误，请重新输入密码。如果忘记密码，请联系管理员重置",
            )

        if not user.is_active:
            return "ACCOUNT_DISABLED", "账户已被停用，请联系管理员激活账户"

        return "UNKNOWN_ERROR", "登录失败，请稍后重试"

    def login_user(self, user_data: UserLogin) -> Token:
        """Login user and return access token"""
        user = self.authenticate_user(user_data.email, user_data.password)
        if not user:
            error_code, error_message = self.get_login_error_details(
                user_data.email, user_data.password
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=error_message
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="账户已被停用，请联系管理员激活账户",
            )

        # Create access token (24 hours expiration)
        access_token_expires = timedelta(hours=24)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires,
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=24 * 60 * 60,  # 24 hours in seconds
        )

    def get_current_user(self, token: str) -> User:
        """Get current user from token"""
        try:
            payload = verify_token(token)
            user_id: str = payload.get("sub") or ""
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="登录令牌无效，请重新登录",
                )
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="登录令牌已过期或无效，请重新登录",
            )

        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户账户不存在或已被删除，请重新登录",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="账户已被停用，请联系管理员",
            )

        return user

    def create_system_user(self, email: str, password: str, name: str) -> User:
        """Create a system user (admin)"""
        # Check if user already exists
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="该邮箱已被注册"
            )

        # Create system user
        hashed_password = get_password_hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            name=name,
            role=UserRole.SYSTEM,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
