import os
import json
import firebase_admin
from firebase_admin import credentials, auth, firestore

cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if cred_json:
    cred = credentials.Certificate(json.loads(cred_json))
else:
    cred = credentials.Certificate(
        "hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json"
    )

firebase_admin.initialize_app(cred)
db = firestore.client()


def make_admin_by_uid(uid):
    """Set admin role for an existing user by their Firebase UID."""
    try:
        user = auth.get_user(uid)
        auth.set_custom_user_claims(uid, {"role": "admin"})
        print(f"Custom claims set for user {uid} ({user.email})")

        db.collection("users").document(uid).set({"role": "admin"}, merge=True)
        print(f"User role updated in Firestore for {uid}")
        print(f"\n {user.email or uid} ahora es Administrador.")
    except Exception as e:
        print(f"Error: {e}")


def make_admin(email, display_name, password):
    try:
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            print(f"Usuario creado con UID: {user.uid}")
        except Exception as e:
            user = auth.get_user_by_email(email)
            print(f"El usuario ya existe. UID: {user.uid}")

        auth.set_custom_user_claims(user.uid, {"role": "admin"})
        print(f"Rol de 'admin' asignado en Auth Claims.")

        db.collection("users").document(user.uid).set({
            "displayName": display_name,
            "email": email,
            "role": "admin",
            "status": "active"
        }, merge=True)
        print(f"Registro en Firestore actualizado correctamente.")

        print(f"\n¡LISTO! {email} ahora es Administrador.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    email = os.getenv("ADMIN_EMAIL", "admin@ejemplo.com")
    name = os.getenv("ADMIN_NAME", "Administrador")
    password = os.getenv("ADMIN_PASSWORD", "12341234")
    make_admin(email, name, password)
