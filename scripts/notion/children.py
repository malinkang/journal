class Children(list):
    def add_block(self,type,content,link = None,color="default"):
        text = Text(content)
        if link is not None:
            link = Link(link)
            text = text.link(link)
        rich_text = RichText(text)
        block  = Block(type,color).add_rich_text(rich_text)
        self.append(block)
        return self


# https://developers.notion.com/reference/block
class Block(dict):
    def __init__(self,type,color):
        self["object"]="block"
        self["type"] = type
        self[type] = {"rich_text":[],"color":color}

    def add_rich_text(self,rich_text):
        self[self["type"]]["rich_text"].append(rich_text)
        return self


class RichText(dict):
    def __init__(self,text,type ="text"):
        self["type"]=type
        self["text"]=text


# https://developers.notion.com/reference/rich-text#link-objects
class Link(dict):
    def __init__(self,link):
        self["type"] = "url"
        self["url"] = link  

# https://developers.notion.com/reference/rich-text#text-objects
class Text(dict):
    def __init__(self,content):
        self["content"] = content  

    def link(self,link):
        self["link"] = link
        return self