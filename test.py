import glob
import os


for file in glob.glob("./content/posts/*.md"):
    with open(file, "r", encoding="utf-8") as f:
        result = ""
        for line in f.readlines():
            if line.startswith("{{<aplayer"):
                pass
            else:
                result += f"\n{line}"