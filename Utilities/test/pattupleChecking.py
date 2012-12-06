from prettytable import PrettyTable
import glob
import argparse


def getMasterSet():
    """Scan /hdfs/store/user/tapas/ 2 deep for all pattuples. Returns set of pattuples (and dict to size if desired)"""
    pattuples=glob.glob('/hdfs/store/user/tapas/*/*')
    temp=set()
    for i in pattuples:
        temp.add(i)
    return temp

def getPattuples(user):
    """Return set of pattuples in use by the specified user"""
    tuplesUsed=set()
    #todo: read these from hep.wisc.edu/~user/pattuples.txt
    with open(user+'.txt','r') as file:
        for line in file:
            tuplesUsed.add(line.rstrip())
    return tuplesUsed

def makeTable(users):
    """Print out table containing overlap between specified users"""
    tablehead=list(users)
    tablehead.insert(0,'Overlaps')
    x=PrettyTable(tablehead)
    for user in users:
        userOL=[user]
        for user2 in users:
            n=userSets[user].intersection(userSets[user2])
            userOL.append(str(len(n)))
        x.add_row(userOL)
    print x

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="%prog -- dump some analysis-level plots and yields")
    parser.add_argument("--size",dest="size",nargs="1",type=bool,default=False,help="Gather size info when getting master list (slow)")
    parser.add_argument("--showNonexistent",dest="showNonexistent",nargs="1",type=bool,default=False,help="Show samples users report as used, but don't seem to exist")
    parser.add_argument("--users",dest="users",nargs="+",type=str,default=['ian','maria','evan','josh','isobel'],help="Specify user list")

    args=parser.parse_args()

    users=args.users
    userSets={}

    users.insert(0,'master')
    users.append('in_use')
    userSets['in_use']=set()

    for i in users:
        if 'in_use' in i:
            continue
        #todo: grab from user webspace
        if "master" not in i:
            userSets[i]=getPattuples(i)
            userSets['in_use']=userSets['in_use'].union(userSets[i])
        else:
            userSets[i]=getMasterSet()
    for user in users:
        print'User:',user.title(),'uses',len(userSets[user]),'samples'
        if args.showNonexistent is True and (userSets['in_use']-userSets['master']) != 0:
            print '---SAMPLES "IN USE", BUT NOT IN MASTER--'
            print userSets[user]-userSets['master']

    makeTable(users)

    userSets['not_in_use']=userSets['master']-userSets['in_use']
    with open('/afs/hep.wisc.edu/user/iross/www/unused_pattuples.txt','w') as f:
        for i in userSets['not_in_use']:
            f.write(i)

    #todo: save pickle with the sets
    #todo: shove results into a webpage somewhere
