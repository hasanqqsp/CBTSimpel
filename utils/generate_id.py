import string
import random
def generate_id(Model,field,length):
    str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])
    if not Model.objects.filter(**{field:str}):
        return str
    else:
        generate_id(Model,field,length)

def generate_numeric_code(Model,field,length):
    '''Generate an 10-character Integer'''
    str = ''.join([random.choice(string.digits) for n in range(length)])
    if not Model.objects.filter(**{field:str}):
        return str
        
    else:
        return self.generate_numeric_code()