
def removeSameName(string):
    str_arr = string.split('.')
    if len(str_arr) >= 2:
        class_name = str_arr[-1]
        module_name = str_arr[-2]
        if class_name == module_name:
            return string.replace('.{}'.format(class_name),'')
    return string
