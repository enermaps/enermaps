"""Delete CM outputs files that haven't been accessed recently"""

import os
import sys
from datetime import datetime, timedelta

# Retrieve the root folder of the CM outputs
cm_outputs_dir = os.environ.get("CM_OUTPUTS_DIR", None)
if cm_outputs_dir is None:
    sys.exit(1)


# Find all the files to delete
now = datetime.utcnow()
max_age = timedelta(hours=1)

files_to_delete = []
folders_to_delete = []

for root, dirs, files in os.walk(cm_outputs_dir):
    if files:
        must_delete = True

        fullpaths = [os.path.join(root, filename) for filename in files]

        for fullpath in fullpaths:
            access_time = datetime.utcfromtimestamp(os.path.getatime(fullpath))

            if (now - access_time) < max_age:
                must_delete = False
                break

        if must_delete:
            files_to_delete.extend(
                [
                    fullpath.replace(cm_outputs_dir + os.path.sep, "")
                    for fullpath in fullpaths
                ]
            )
            folders_to_delete.append(root.replace(cm_outputs_dir + os.path.sep, ""))
    elif not dirs:
        folders_to_delete.append(root.replace(cm_outputs_dir + os.path.sep, ""))


# Delete the files and any empty directory left after
os.chdir(cm_outputs_dir)

for filename in files_to_delete:
    os.remove(filename)

for path in folders_to_delete:
    if os.path.exists(path):
        os.removedirs(path)
