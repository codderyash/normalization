#Riddhi Prajapati
"""|---------------------------------CANDIDATE KEY AND NORMALISATION----------------------------|"""
def closure(R, FD, S):
    if not (is_subset(S, R)):
        return []
    result = list(S)
    changed = True
    while(changed):
        changed = False
        for fd in FD:
            LHS = fd[0]
            RHS = fd[1]
            if (is_subset(LHS, result)):
                for att in RHS:
                    if (att not in result):
                        result.append(att)
                        changed = True
    return sorted(result)


def is_subset(X, Y):
    '''
    Check if the list is subset of another list
    '''
    return set(X).issubset(set(Y))


def candidate_keys(R, FD):
    result = []
    ck = []
    for att_set in subsets(R): # if r is having 5 att. then 2 pow 5 subsets will be there
        att_closure = closure(R, FD, att_set)
        #[a,c,f]---[a,c,f,e]
        #candidate key--subste of super key
        if (att_closure == R):
            #check if super key then continue
            iis = False
            for key in ck:
                if is_subset(key, att_set):
                    iis = True
            if iis:
                continue
            ck.append(att_set)
    ls_ck = [] 
     #ck is 2d list
       # [[a,c][b,s,d]]
    for i in ck:
        s = ""
        for j in i:
            s += j
        ls_ck.append(s)
    return ls_ck


def subsets(R):
    '''
    Calculate all possible subsets of given list
    Return them in a sorted way (first alphabetic and then length)
    '''
    #r-[a,b,c,d....]
    #a,b,---d,ab,abc,abcd
    #000,001,010,011,100,101,110,111
    #a,b,c,ab,bc,ca,abc
    #0-(non-pick case)
    #1-(pick case)
    
    x = len(R)
    masks = [1 << i for i in range(x)]
    result = []
    for i in range(1, 1 << x):
        r = []
        for mask, ss in zip(masks, R):
            if i & mask:
                r.append(ss)
        result.append(r)
    result.sort()
    result.sort(key=len)
    return result


def prime(ck):
    '''
        takes set of attributes of candidate key and returns set of prime attributes
    '''
    #[ab,cdf]
    pr = set()
    for i in ck:
        for j in i:
            pr.add(j)
    return pr


def non_prime(pr, R):
    '''
        takes prime attributes and R and returns set of non-prime attributes
    '''
    return R.difference(pr)

#--------------------------------------------------starting of code--------------------------------------------------------#
r=input('Enter the attributes:') 
# r = "a,b,c,d,e,f,g,h"
relation = r.split(",")

l = set()
m = set()
r = set()
fds = []
f1 = []
n=input("Enter functional Dependency:")
# n = "ch->g,a->bc,b->cfh,e->a,f->eg"
li = n.split(",")

for i in li:
    li1 = i.split("->")
    fds.append(li1)
    f1.append(li1)

print(fds)
# for fd in fds:
#     for i in range(2):
#         ls = []
#         for j in fd[i]:
#             ls.append(j)
#         fd[i] = ls

ck = candidate_keys(relation, fds)
print("--------------------------------------------------------------------------")
print("----------------------------CANDIDATE KEYS--------------------------------")
print("Candidate keys are :")
for i in ck:
    print(i)
print("--------------------------------------------------------------------------")
print("----------------------------PRIME ATTRIBUTES------------------------------")
pr = prime(ck)
for i in pr:
    print(i)
print("--------------------------------------------------------------------------")
print("--------------------------NON-PRIME ATTRIBUTES----------------------------")
np = non_prime(pr, set(relation))
for i in np:
    print(i)
print("--------------------------------------------------------------------------")


def check(string, cd):
    if (string.find(cd) == -1):
        return 0
    else:
        return 1


def check_bcnf(ck, fd):
    ls_left = []
    ls_right = []
    flag = 0
    for fd in fds:
        sl = "" #convert list in string
        for i in fd[0]:
            sl += i
        ls_left.append(sl)

        sr = "" #convert list in string
        for i in fd[1]:
            sr += i
        ls_right.append(sr)

    for i in ls_left:
        for j in ck:
            if (check(i, j) == 0):
                print("Violating BCNF Condition at {}->{}".format(i, ls_right[ls_left.index(i)]))
                flag = 1
                break
    print("--------------------------------------------------------------------------")
    if flag == 1:
        return False
    else:
        return True


def in_np(s, np):
    for i in s:
        if i in np:
            return 0
    return 1

def check_3nf(ck, fd, R):
    ls_left = []
    ls_right = []
    flag = 0

    pr = prime(ck)
    np = non_prime(pr, set(R))
    #     print(np)
    #     print(pr)

    for fd in fds:
        sl = ""
        for i in fd[0]:
            sl += i
        ls_left.append(sl)

        sr = ""
        for i in fd[1]:
            sr += i
        ls_right.append(sr)
#non prime determines non - prime
    for i in ls_left:
        for j in ck:
            if check(i,j) == 0 and in_np(ls_right[ls_left.index(i)], np) == 0:
                print("Violating 3NF Condition at {}->{}".format(i, ls_right[ls_left.index(i)]))
                flag = 1
                break
    print("--------------------------------------------------------------------------")
    if flag == 1:
        return False
    else:
        return True


def check_2nf(ck, fd, R):
    ls_left = []
    ls_right = []
    flag = 0

    pr = prime(ck)
    np = non_prime(pr, set(R))
    for fd in fds:
        sl = ""
        for i in fd[0]:
            sl += i
        ls_left.append(sl)

        sr = ""
        for i in fd[1]:
            sr += i
        ls_right.append(sr)
     #bgsj
    for i in ls_left:
        for j in i:
            if j in pr and ls_right[ls_left.index(i)] in np:
                print("Violating 2NF Condition at {}->{}".format(i, ls_right[ls_left.index(i)]))
                flag = 1
    print("--------------------------------------------------------------------------")
    if flag == 1:
        return False
    else:
        return True


print("--------------------------------------------------------------------------")

if check_bcnf(ck, fds) == True and len(ck)!=0:
    print("Relation is in BCNF")
elif check_3nf(ck, fds, relation) == True and len(ck)!=0 and check_2nf(ck, fds, relation) == True:
    print("Relation is in 3NF")
elif check_2nf(ck, fds, relation) == True and len(ck)!=0:
    print("Relation is in 2NF")
else:
    print("Relation is in 1NF")