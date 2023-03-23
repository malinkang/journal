
def get_title(result,name):
    if(len(result['properties'][name]['title']) ==0):
        return ""
    return result['properties'][name]['title'][0]['text']['content']

def get_rich_text(result,name):
    if(len(result['properties'][name]['rich_text']) ==0):
        return ""
    return result['properties'][name]['rich_text'][0]['text']['content']


def get_date(result,name):
   return result["properties"][name]["date"]["start"]