import json
import glob
import os
import sys
import urllib.request

ignore = [ "./github.json", "./vcmi-1.2.json" ]

for filename in glob.glob(os.path.join('.', '*.json')):
    if filename not in ignore:
        print(f"Opening: {filename}")
        filecontent = open(filename, "r").read()
        modlist = json.loads(filecontent)
        for mod, data in modlist.items():
            url = data["download"]
            print(f"Download {mod}: {url}")
            try:
                response = urllib.request.urlopen(url)
            except:
                print(f"Error: download failed!")
                sys.exit(os.EX_SOFTWARE)
            filesize = round(len(response.read()) / 1024 / 1024, 3)
            print(f"Size: {filesize}")
            data["size"] = filesize

        resultcontent = json.dumps(modlist, indent='\t', separators=(',', ' : '))

        if filecontent != resultcontent:
            open(filename, "w").write(resultcontent)

sys.exit(os.EX_OK)