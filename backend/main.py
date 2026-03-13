import firebase_admin
from firebase_admin import credentials, auth
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.user_service import UserService

user_service = UserService()

# 1. Initialize Firebase Admin
cred = credentials.Certificate("hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")
firebase_admin.initialize_app(cred)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

security = HTTPBearer()

# 2. Dependency to verify the Firebase token
async def get_current_user(res: HTTPAuthorizationCredentials = Depends(security)):
    token = res.credentials
    try:
        # Verify the ID token sent from the client-side Firebase SDK
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired Firebase token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 3. Protected Route
@app.get("/users/me")
async def read_user_me(user=Depends(get_current_user)):
    # 'user' contains the decoded UID, email, etc.
    return {"uid": user["uid"], "email": user.get("email")}

# 4. Public Route
@app.get("/")
def home():
    return {"message": "Public Hello World"}

@app.post("/users/signup-sync")
async def sync_user(token_data=Depends(get_current_user)):
    return user_service.register_new_user(token_data)