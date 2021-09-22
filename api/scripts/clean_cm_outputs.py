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

to_delete = []

for root, dirs, files in os.walk(cm_outputs_dir):
    for filename in files:
        fullpath = os.path.join(root, filename)
        access_time = datetime.utcfromtimestamp(os.path.getatime(fullpath))

        if (now - access_time) > max_age:
            to_delete.append(fullpath.replace(cm_outputs_dir + os.path.sep, ""))


# Delete the files and any empty directory left after
os.chdir(cm_outputs_dir)

for filename in to_delete:
    os.remove(filename)
    path, _ = os.path.split(filename)
    os.removedirs(path)
