def getSES():
    SES = [["1", "Please select your SES status"]]
    for i in "123456":
        SES.append([str(int(i) + 1), i])
    return SES

def getType():
    ...