import os
import json

import firebase_admin
from firebase_admin import credentials, firestore

cred_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if cred_json:
    cred = credentials.Certificate(json.loads(cred_json))
else:
    cred = credentials.Certificate(
        "hogarlimpio-dffeb-firebase-adminsdk-fbsvc-a0be160afb.json"
    )

firebase_admin.initialize_app(cred)
db = firestore.client()
