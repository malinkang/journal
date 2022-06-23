class Children(list):
    def add_heading_2(self, content, link=""):
        self.add_rich_text("heading_2", content, link)
        return self

    def add_bulleted_list_item(self, content, link="aaa"):
        self.add_rich_text("bulleted_list_item", content, link)
        return self

    def add_to_do(self, content, link=""):
        self.add_rich_text("to_do", content, link)
        return self

    """https://developers.notion.com/reference/rich-text"""
    def add_rich_text(self, type, content, link, color="default"):
        self.append(
            {
                "type": type,
                type: {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content,
                                # "link": {"type": "url", "url": link},
                            },
                            "annotations": {
                                "color": color,
                            },
                        }
                    ]
                },
            }
        )
        return self