import json
# https://developers.notion.com/reference/page
class Page(dict):
    def parent(self, parent):
        self["parent"]  = parent
        return self
    def children(self, children):
        self["children"] = children
        return self
    def cover(self,cover):
        self["cover"] = {"type": "external", "external": {"url": cover}}
        return self
    def icon(self,icon):
        self["icon"] = {"type": "emoji", "emoji": icon}
        return self
    def properties(self,properties):
        self["properties"] = properties
        return self