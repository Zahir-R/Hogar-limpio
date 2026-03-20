import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate("hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")
firebase_admin.initialize_app(cred)

uid = "F1IpXW0R3fYSDkdKPX4A6seR2fj2"
auth.set_custom_user_claims(uid, {"role": "admin"})
print(f"Custom claims set for user {uid}")

db = firestore.client()
users_ref = db.collection("users").document(uid)
users_ref.set({"role": "admin"}, merge=True)
print(f"User role updated for user {uid}")
