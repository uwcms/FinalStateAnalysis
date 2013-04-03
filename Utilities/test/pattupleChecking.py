#!/usr/bin/python3

'''
File: pattupleChecking.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Scans specified users' [webhome]/tuples.txt, tallies up who is using what (and how much overlap exists between users), and spits out the list of unused samples.
'''

from FinalStateAnalysis.Utilities.prettytable import PrettyTable
import glob
from RecoLuminosity.LumiDB import argparse
import urllib2


def getMasterSet():
    """Scan /hdfs/store/user/tapas/ 2 deep for all pattuples. Returns set of pattuples (and dict to size if desired)"""
    pattuples=glob.glob('/hdfs/store/user/tapas/*/*')
    temp=set()
    for i in pattuples:
        temp.add(i)
    return temp

def cleanline(line):
    """Remove '//' and trailing / for string matching"""
    line=line.replace("//","/")
    line=line.rstrip("/")
    return line

def getPattuples(user):
    """Return set of pattuples in use by the specified user"""
    tuplesUsed=set()
    #todo: read these from hep.wisc.edu/~user/pattuples.txt
    try:
        response = urllib2.urlopen('http://www.hep.wisc.edu/~'+user+'/tuples.txt')
        for line in response.readlines():
            if line.rstrip() == "":
                continue
            tuplesUsed.add(cleanline(line.rstrip()))
        print user,"has their stuff together!"
    except urllib2.HTTPError:
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
    return x

def unique(user):
    """Returns the list of pattuples unique to that user"""
    tempSet=userSets[user]
    print len(tempSet),"before uniqueing"
    for u in userSets:
        if user in u or "master" in u or "in_use" in u: #don't check overlap with master, in_use lists
            continue
        else:
            tempSet=tempSet.difference(userSets[u])
        print len(tempSet),"after uniqueing",u

    return tempSet

def uniqueNot(user,notUsers):
    """Returns the list of pattuples unique to that user"""
    tempSet=userSets[user]
    print len(tempSet),"before uniqueing"
    for u in userSets:
        if u in notUsers:
            tempSet=tempSet.difference(userSets[u])
        else:
            continue;
    print len(tempSet),"in",user,"not in",notUsers;

    return tempSet

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="%prog -- dump some analysis-level plots and yields")
    parser.add_argument("--size",dest="size",type=bool,default=False,help="Gather size info when getting master list (slow)")
    parser.add_argument("--showNonexistent",dest="showNonexistent",type=bool,default=False,help="Show samples users report as used, but don't seem to exist")
    parser.add_argument("--users",dest="users",nargs="+",type=str,default=['iross','mcepeda','efriis','swanson','ojalvo'],help="Specify user list")

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

    table = makeTable(users)

    print table

    with open('/afs/hep.wisc.edu/user/iross/www/unique_list.txt','w') as f:

        f.write(table.get_string()+"\n\n")

        for user in users:
            print'User:',user.title(),'uses',len(userSets[user]),'samples'
            if args.showNonexistent is True and (userSets['in_use']-userSets['master']) != 0:
                print '---SAMPLES "IN USE", BUT NOT IN MASTER--'
                print userSets[user]-userSets['master']
            if 'master' not in user and 'in_use' not in user:
                uniq=unique(user)
                f.write('-----'+user+" Unique List ("+str(len(uniq))+")-----\n")
                for i in sorted(uniq):
                    f.write(i+'\n')
                f.write('\n')



    userSets['not_in_use']=userSets['master']-userSets['in_use']
    with open('/afs/hep.wisc.edu/user/iross/www/unused_pattuples.txt','w') as f:
        f.write("------------\n"+str(len(userSets['not_in_use']))+" pattuples not in use!\n")
        f.write("------------\n")
        for i in sorted(userSets['not_in_use']):
            f.write(i+"\n")

    #todo: save pickle with the sets
    #todo: shove results into a webpage somewhere
