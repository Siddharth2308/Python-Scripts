import firebase_admin
from firebase_admin import credentials

cred  = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection('employee').document('empdoc')
doc_ref.set({
    'name' : 'Siddharhth',
    'Lname' : 'Kulkarni',
    'age' : 19
})
