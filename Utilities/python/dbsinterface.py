import subprocess
from xml.dom.minidom import parseString
#from DBSAPI.dbsApi import DbsApi

def get_dbs_info(toFind, requirements):
    "Interface with the DBS API to get the whatever you want of a requirements. ALWAYS RETURN A LIST OF STRINGS"
    args = {}
    args['url']='http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'
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


def get_das_info(query):
    '''Interface with das.py to get the query output.
    Could be done better, but this is time effective.
    Unfortunately the QL is more complicated than the 
    DBS one. '''
    
    das_command = [
        'dasgoclient',
        '--query=%s' % query,
        '--limit=0' 
        ]
    p = subprocess.Popen(
        das_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    out, err = p.communicate()
    das_exitcode = p.wait()
    
    if das_exitcode <> 0:
        raise RuntimeError(
            'das.py crashed with error:\n%s' % \
                err+out ) #sometimes das sends the crash message to stdout
    return [i.strip() for i in out.split('\n') if i.strip()]
