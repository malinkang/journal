import glob
import os
file = glob.glob("./content/posts/*.md")
for i in file:
    dir = i[i.rfind("/")+1:i.rfind(".")]
    os.mkdir(f"./content/posts/{dir}")
    os.rename(i,f"./content/posts/{dir}/index.md")