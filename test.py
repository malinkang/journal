import glob
import os
file = glob.glob("./content/posts/2022/*/images/*.png")
for i in file:
    if os.path.isfile(i):
        os.remove(i)