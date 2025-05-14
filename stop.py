from pathlib import Path
import subprocess, json

import blinky

Path("stop").touch()

finished = input("Finished? [Enter]")
blinky.write_data(blinky.compile_data())
print("Done!")

with open(Path("data/web.json"), "r") as f:
    web = json.load(f)
print('{:,}'.format(len(blinky.get_seen_domains(web))), "distinct websites so far.")
print('{:,}'.format(len(blinky.get_seen_pages(web))), "web pages so far")

try: subprocess.run("code data/web.json", shell=True) # This is so that the file opens nicely in VSCode for me :)
except: pass
