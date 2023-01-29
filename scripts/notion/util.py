
def get_title(result,name):
    if(len(result['properties'][name]['title']) ==0):
        return ""
    return result['properties'][name]['title'][0]['text']['content']