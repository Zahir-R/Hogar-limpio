import firebase_admin
from firebase_admin import credentials, auth, firestore

# Configuración (Asegúrate de que el nombre del JSON sea el correcto)
cred = credentials.Certificate("hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def make_admin(email, display_name, password):
    try:
        # 1. Intentar crear el usuario en Firebase Auth
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            print(f"✅ Usuario creado con UID: {user.uid}")
        except Exception as e:
            # Si ya existe, lo obtenemos por email
            user = auth.get_user_by_email(email)
            print(f"ℹ️ El usuario ya existe. UID: {user.uid}")

        # 2. Asignar el Custom Claim de 'admin'
        auth.set_custom_user_claims(user.uid, {"role": "admin"})
        print(f"👑 Rol de 'admin' asignado en Auth Claims.")

        # 3. Registrar o actualizar en Firestore
        db.collection("users").document(user.uid).set({
            "displayName": display_name,
            "email": email,
            "role": "admin",
            "status": "active"
        }, merge=True)
        print(f"🗄️ Registro en Firestore actualizado correctamente.")
        
        print(f"\n🚀 ¡LISTO! {email} ahora es Administrador.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # CAMBIA ESTOS DATOS POR LOS TUYOS
    mi_email = "admin@ejemplo.com"
    mi_nombre = "Administrador"
    mi_password = "12341234"
    
    make_admin(mi_email, mi_nombre, mi_password)