class Properties(dict):
    """https://developers.notion.com/reference/property-value-object"""
    def title(self,title):
        self["title"] = {"title": [{"type": "text", "text": {"content": title}}]}
        return self
    def multi_select(self, property, list):
        multi_select = []
        for item in list:
            multi_select.append({"name": item})
        self[property] = {
            "type": "multi_select",
            "multi_select": multi_select,
        }
        return self
    def rich_text(self, property, text):
        rich_text = []
        rich_text.append({"type": "text", "text": {"content": text}})
        self[property] = {
            "rich_text": rich_text,
        }
        return self
    def status(self,property,status):
        self[property] = {"status": {"name": status}}
        return self
    def select(self, property, name):
        self[property] = {"select": {"name": name}}
        return self
    def date(self, property, start,end):
        self[property] = {"date": {"start": start,"end":end}}
        return self
    def number(self,property,number):
        self[property] = {"number": number}
        return self
