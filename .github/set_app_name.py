import io
import os
import re

NAME_FILE = ".github/app_name.txt"
MANIFEST = "android/app/src/main/AndroidManifest.xml"


def main():
    name = ""
    if os.path.exists(NAME_FILE):
        with io.open(NAME_FILE, encoding="utf-8") as handle:
            name = handle.read().strip()
    if not name:
        print("No app name supplied; keeping the default label.")
        return
    if not os.path.exists(MANIFEST):
        print("AndroidManifest.xml not found; skipping.")
        return
    safe = (
        name.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    with io.open(MANIFEST, encoding="utf-8") as handle:
        source = handle.read()
    patched = re.sub(r'android:label="[^"]*"', 'android:label="%s"' % safe, source, count=1)
    with io.open(MANIFEST, "w", encoding="utf-8") as handle:
        handle.write(patched)
    print("App label set to: %s" % name)


main()
