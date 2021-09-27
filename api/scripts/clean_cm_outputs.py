"""Delete CM outputs files that haven't been accessed recently"""

import os
import sys
from datetime import datetime, timedelta

# Retrieve the root folder of the CM outputs
upload_dir = os.environ.get("UPLOAD_DIR", None)
if upload_dir is None:
    sys.exit(1)

cm_outputs_dir = os.path.join(upload_dir, "cm_output")


# Find all the files to delete
now = datetime.utcnow()
max_age = timedelta(hours=1)

files_to_delete = []
folders_to_delete = []

for root, dirs, files in os.walk(cm_outputs_dir):
    if files:
        for filename in files:
            fullpath = os.path.join(root, filename)
            access_time = datetime.utcfromtimestamp(os.path.getatime(fullpath))

            if (now - access_time) > max_age:
                files_to_delete.append(
                    fullpath.replace(cm_outputs_dir + os.path.sep, "")
                )
                folders_to_delete.append(root.replace(cm_outputs_dir + os.path.sep, ""))
    elif not dirs:
        folders_to_delete.append(root.replace(cm_outputs_dir + os.path.sep, ""))


# Delete the files and any empty directory left after
os.chdir(cm_outputs_dir)

for filename in files_to_delete:
    os.remove(filename)

for path in folders_to_delete:
    os.removedirs(path)
