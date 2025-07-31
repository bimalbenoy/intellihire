from security import get_password_hash, verify_password, create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models import User, Token, UserCreate, Role

router = APIRouter()
@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(form_data: UserCreate ):
    existing_user = await User.find_one(User.email == form_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_pswd = get_password_hash(form_data.password)

    user = User(
        full_name=form_data.full_name,
        email=form_data.email,
        hashed_password=hashed_pswd,
        role=Role.CANDIDATE
    )

    await user.insert()
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.email == form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role.value}
    )

    return {"access_token": access_token, "token_type": "bearer"}
