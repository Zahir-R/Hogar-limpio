### FRONTEND
```
cd frontend
npm i
cp .env.example .env     # then fill in Firebase values
npm run dev
```

### BACKEND
```
cd backend

# On Windows
venv\Scripts\activate

pip install "fastapi[standard] firebase-admin"
fastapi dev main.py
```

Frontend → http://localhost:3000
Backend  → http://localhost:8000
