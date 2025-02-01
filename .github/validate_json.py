import jstyleson
import glob
import os
import sys

from ignore_json import ignore

error = False

for filename in glob.glob(os.path.join('.', '*.json')):
    if filename not in ignore:
        print(f"Opening: {filename}")
        
        with open(filename, "r") as file:
            filecontent = file.read()

        try:
            jstyleson.loads(filecontent)
            print(f"✅ JSON valid")
        except Exception as err:
            error = True
            print(f"❌ JSON invalid in {filename}:")
            print(str(err))

if error:
    sys.exit(os.EX_SOFTWARE)
else:
    print("Everything is ok!")
    sys.exit(os.EX_OK)
