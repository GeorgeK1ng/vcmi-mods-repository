import jstyleson
import glob
import os
import sys
import urllib.request

from ignore_json import ignore

for filename in glob.glob(os.path.join('.', '*.json')):
    if filename not in ignore:
        print(f"Opening: {filename}")

        with open(filename, "r") as file:
            filecontent = file.read()

        try:
            modlist = jstyleson.loads(filecontent)
        except Exception as err:
            print(f"❌ Error reading JSON file {filename}: {err}")
            sys.exit(os.EX_SOFTWARE)

        for mod, data in modlist.items():
            url = data["download"].replace(" ", "%20")
            print(f"Download {mod}: {url}")

            try:
                response = urllib.request.urlopen(url)
                filecontent = response.read()
                print(f"✅ Download successful")
            except Exception as err:
                print(f"❌ Download failed: {err}")
                sys.exit(os.EX_SOFTWARE)

            filesize = round(len(filecontent) / 1024 / 1024, 3)
            print(f"Size: {filesize} MB")
            data["downloadSize"] = filesize

        resultcontent = json.dumps(modlist, indent='\t', separators=(',', ' : ')) + "\n"

        if filecontent != resultcontent:
            with open(filename, "w") as file:
                file.write(resultcontent)

sys.exit(os.EX_OK)
