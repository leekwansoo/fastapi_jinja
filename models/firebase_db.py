import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import cv2
import datetime

from models.firebase_storage import storeimage
# install with "pip install --upgrade google-cloud-datastore"

cred = credentials.Certificate("models/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'fileuploader-28b20.appspot.com'})
db = firestore.client()

# For help authenticating your client, visit
# https://cloud.google.com/docs/authentication/getting-started

def store_userdata():
    doc_ref = db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })

def store_imagedata(file, location):
    #location = storeimage(file)
    filename = file
    content_type = filename.split(".")[1]
    doc_ref = db.collection(u'images').document(filename)
    doc_ref.set({
        u'filename': filename,
        u'content_type': content_type,
        u'date': datetime.datetime.now(),
        u'imagelocation': location
    })

    return()

"""
def store_videodata(file):
    filename = file
    content_type = filename.split(".")[1]
    doc_ref = db.collection(u'videos').document(filename)
    doc_ref.set({
        u'filename': filename,
        u'content_type': content_type,
        u'date': datetime.datetime.now()
    })
    return()
"""
