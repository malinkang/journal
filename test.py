import os

def remove_tweet_embeds(directory):
    """
    Recursively traverse the given directory and remove lines starting with "{{< tweet"
    from all Markdown (.md) files.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                modified_lines = []
                with open(file_path, "r") as f:
                    for line in f:
                        if not line.startswith("{{< tweet"):
                            modified_lines.append(line)
                with open(file_path, "w") as f:
                    f.writelines(modified_lines)

# Specify the directory to start the search
directory = "/Users/shareit/Dropbox/journal/content"
remove_tweet_embeds(directory)