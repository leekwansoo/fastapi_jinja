import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# install with "pip install --upgrade google-cloud-datastore"
# Use the application default credentials.
# For help authenticating your client, visit
# https://cloud.google.com/docs/authentication/getting-started

def storeimage(file):
    # Put your local file path 
    filepath = file
    print(filepath)
    bucket = storage.bucket()
  
    blob = bucket.blob(filepath)
    blob.upload_from_filename(
        filepath,
        content_type=None
    )

    imageBlob = bucket.get_blob(filepath)
    
    return (imageBlob)

    
#storeimage("C:\Users\leekw\Desktop\fastapi_jinja\image.py")