
def get_title(result,name):
    if(len(result['properties'][name]['title']) ==0):
        return ""
    return result['properties'][name]['title'][0]['text']['content']

def get_rich_text(result,name):
    if(len(result['properties'][name]['rich_text']) ==0):
        return ""
    return result['properties'][name]['rich_text'][0]['text']['content']

def get_multi_select(result,name):
    return result['properties'][name]['multi_select']

def get_number(result,name):
    return result['properties'][name]['number']

def get_formula(result,name):
    return result['properties'][name]['formula'].get("string")

def get_select(result,name):
    return result['properties'][name]['select'].get("name")


def get_date(result,name):
   return result["properties"][name]["date"]["start"]