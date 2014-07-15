from xml.dom.minidom import parseString
from DBSAPI.dbsApi import DbsApi

def get_dbs_info(toFind, requirements):
    "Interface with the DBS API to get the whatever you want of a requirements. ALWAYS RETURN A LIST OF STRINGS"
    args = {}
    args['url']='https://cmsweb.cern.ch/dbs/prod/global/DBSReader'
    args['version']='DBS_2_0_9'
    args['mode']='POST'
    api = DbsApi(args)
    data = api.executeQuery("find %s where %s" % (toFind, requirements))
    domresults = parseString(data)
    dbs = domresults.getElementsByTagName('dbs')
    result = dbs[0].getElementsByTagName('results')
    rows=result[0].getElementsByTagName('row')
    retList = []
    for row in rows:
        resultXML = row.getElementsByTagName(toFind)[0]
        node=(resultXML.childNodes)[0] #childNodes should be a one element array
        retList.append(str(node.nodeValue))
    return retList
