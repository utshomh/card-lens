import os
import time

UPLOAD_DIR = "uploads"

FILE_EXPIRY = 60  # seconds (1 minutes)

def cleanup_uploads():
    now = time.time()

    for filename in os.listdir(UPLOAD_DIR):

        path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        if os.path.isfile(path):
            age = now - os.path.getmtime(path)

            if age > FILE_EXPIRY:
                os.remove(path)