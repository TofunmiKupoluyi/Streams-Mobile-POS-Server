def parseHttpRequest(req):
    splitReq = req.split("\n")
    reqDict = {}
    for line in splitReq[1:]:
        # splitting into key value
        keyValueArray = line.split(":")

        # if it is a key value pair (normal header)
        if len(keyValueArray) > 1:
            # For normal headers
            key = keyValueArray[0]
            # Removing any preceding whitespace before the value and also the \r
            value = keyValueArray[1].lstrip().replace("\r","")
            inner = {key: value}
            reqDict.update(inner)
        
        elif len(keyValueArray) > 0:
            if not keyValueArray[0] == "\n":
                inner = {"reqContent": keyValueArray[0]}
                reqDict.update(inner)
    
    return reqDict