from .models import PropertyType

def getSES():
    SES = [["1", "Please select your SES status"]]
    for i in "123456":
        SES.append([str(int(i) + 1), i])
    return SES

def getTypes():
    types = [["1", "Please select your property type"]]
    for i in PropertyType.objects.all():
        types.append([str(i.id+1), i.name])
    return types

