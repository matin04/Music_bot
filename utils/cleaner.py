import os
import time


def delete_file(path):

    if path and os.path.exists(path):

        try:
            os.remove(path)

        except:
            pass

def delete_old_files(folder, hours=24):

    now = time.time()

    for filename in os.listdir(folder):

        file_path = os.path.join(folder, filename)

        if not os.path.isfile(file_path):
            continue

        file_age = now - os.path.getmtime(file_path)

        if file_age > hours * 3600:

            try:
                os.remove(file_path)

            except:
                pass