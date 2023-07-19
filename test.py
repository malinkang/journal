import glob
import os


for file in glob.glob("./content/posts/*.md"):
    new_file = file[file.rindex("/")+1:-3]
    dir = f"./content/posts/2023/{new_file}"
    if(not os.path.exists(dir)):
        os.makedirs(dir)
    os.rename(file,f"{dir}/index.md")