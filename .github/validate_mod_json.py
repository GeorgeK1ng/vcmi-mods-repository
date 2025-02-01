import jstyleson
import glob
import os
import sys
import urllib.request

from ignore_json import ignore

error = False

for filename in glob.glob(os.path.join('.', '*.json')):
    if filename not in ignore:
        print(f"Opening: {filename}")
        filecontent = open(filename, "r").read()
        
        try:
            modlist = jstyleson.loads(filecontent)
        except Exception as err:
            error = True
            print(f"❌ Error reading JSON file {filename}: {err}")
            continue

        for mod, data in modlist.items():
            url = data["mod"].replace(" ", "%20")
            print(f"{mod}: {url}")
            try:
                response = urllib.request.urlopen(url)
                print(f"✅ Download successful")
            except Exception as err:
                error = True
                print(f"❌ Download failed: {err}")
                continue

            filecontent = response.read()

            try:
                jstyleson.loads(filecontent)
                print(f"✅ JSON valid")
            except Exception as err:
                error = True
                print(f"❌ JSON invalid:")
                print(str(err))
                continue
if error:
    sys.exit(os.EX_SOFTWARE)
else:
    print("Everything is ok!")
    sys.exit(os.EX_OK)
