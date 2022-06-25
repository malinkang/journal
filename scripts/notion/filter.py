class Filter(dict):
    def __init__(self,property,type,condition,value):
        self["property"] = property
        self[type] = {condition:value}
