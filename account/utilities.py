from .models import UserType
from .models import Role

def getUserType(): 
    optionsUserType = [["1", "Select a user type for your account"]]
    for i in UserType.objects.all():
        if(i.idUserType == 1): optionsUserType.append(["persona", i.nameUserType])
        else: optionsUserType.append(["negocio", i.nameUserType])
    return optionsUserType


def getRole(): 
    optionsRole = [["1", "Select a role for your account"]]
    for i in Role.objects.all():
        optionsRole.append([str(i.idRole + 1), i.nameRole]) 
    return optionsRole
