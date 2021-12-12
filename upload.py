from firebase_admin import credentials, initialize_app, storage
# Init firebase with your credentials
cred = credentials.Certificate('firebaseConfig': {
    'apiKey': 'AIzaSyA7NZyZU1tv1Wferm--zCmZrj-FgFr1wu8',
    'authDomain': 'cobra-7bc16.firebaseapp.com',
    'projectId': 'cobra-7bc16',
    'storageBucket': 'cobra-7bc16.appspot.com',
    'messagingSenderId': '473609632318',
    'appId': '1:473609632318:web:a0a22ec85ff3aeb3adaf6f',
    'measurementId': 'G-GJYD4RE2V8'
  })
initialize_app(cred, {'storageBucket': 'cobra-7bc16.appspot.com/IMG-DOCT'})

# Put your local file path
fileName = "splash-2732x2732-2.png"
bucket = storage.bucket()
blob = bucket.blob(fileName)
blob.upload_from_filename(fileName)

# Opt : if you want to make public access from the URL
blob.make_public()

print("your file url", blob.public_url)