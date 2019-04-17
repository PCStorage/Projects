#!/usr/bin/python

import sys
import dns.resolver #import the module
import time

def getIP(arg1):
    arg1=arg1.split()
    return arg1[4]

def IPextract(Lresponse):
    listing = []
    on = False
    for line in Lresponse:
        if on == True:
            lines = line.split()
            if lines[3]=='A':
                listing.append(getIP(line))    
        if line == ';ADDITIONAL':
            on = True
    return listing

def runList(result):
    print (result)
    for x in result:
        print (x)
    start = time.time() #start
    response = dns.query.udp(m, x)#ask for x
    end = time.time() # finish
    Totaltime = Totaltime+end-start #total time update
    Xresponse = response.__str__().split("\n") #split lines
    result = IPextract(Xresponse) #get IP to check
    print(result)
    return result

def answerCheck(Lresponse):
    listing = []##
    on = False
    for line in Lresponse:
        if line == ';AUTHORITY': #End of Answer Section
            on = False
        if on == True:
            listing.append(line)    
        if line == ';ANSWER': # Start of Answer Section
            on = True
    return listing

def getSIP(response):
    listing = []##
    on = False
    for line in response:
        if line == ';ADDITIONAL': #End of Answer Section
            on = False
        if on == True:
            listing.append(getIP(line))
        if line == ';AUTHORITY': #End of Answer Section
            on = True
    return listing

aroot =	'198.41.0.4'
broot = '199.9.14.201'
croot = '192.33.4.12'
droot = '199.7.91.13'
eroot = '192.203.230.10'
froot = '192.5.5.241'
groot = '192.112.36.4'
hroot = '198.97.190.53'
iroot = '192.36.148.17'
jroot = '192.58.128.30'
kroot = '193.0.14.129'
lroot = '199.7.83.42'
mroot = '202.12.27.33'

#website = "Twitch.tv"
currentT = time.ctime() # 'Mon Oct 18 13:35:29 2010'
website = sys.argv[1] #imput
IPset ={}
checkset = set()
finalset = set()
Totaltime = 0
answer = []
m = dns.message.make_query(website, 'A')    #ask root
start = time.time() #start
response = dns.query.udp(m, aroot)          #get root dns response
end = time.time() # finish
Totaltime = Totaltime+end-start #total time update
Lresponse = response.__str__().split("\n")  #Line array
result = IPextract(Lresponse)#takes IP from Additional section
#print (response)
for x in result: #check for redundency
    checkset.add(x)
    #print(x)
#print('*'*8+'Authoritative'+'*'*8)
for x in checkset:
    start = time.time() #start
    response = dns.query.udp(m, x)#ask for x
    end = time.time() # finish
    Totaltime = Totaltime+end-start #total time update
    Xresponse = response.__str__().split("\n")
    result = IPextract(Xresponse)
    #print(result)
    if result == []:
        response = getSIP(Xresponse)
        #print(response)
        #print('*****')
        for x in response:
            n = dns.message.make_query(x, 'A')
            start = time.time() #start
            response = dns.query.udp(n, aroot)
            end = time.time() # finish
            Totaltime = Totaltime+end-start #total time update
            response = response.__str__().split("\n")
            #print(response)
            EX = IPextract(response)
            #print(EX)
            for a in EX:
                start = time.time() #start
                responses = dns.query.udp(n, a)
                end = time.time() # finish
                Totaltime = Totaltime+end-start #total time update
                #print(responses)
                responses = responses.__str__().split("\n")
                EXX = IPextract(responses)
                #print(EXX)
                if EXX !=[]:
                    result= EXX
                    break
    for x in result: #check for redundency
        finalset.add(x)
    break
    #print(response)
#for x in finalset:
    #print(x)
#print('*'*8+'HostServer'+'*'*8)
i=1
for x in finalset:
    #print(i)
    #i+=1
    start = time.time()
    response = dns.query.udp(m, x)
    end = time.time()
    Totaltime = Totaltime+end-start
    #print(response)
    Xresponse = response.__str__().split("\n")
    #result = IPextract(Xresponse)
    #print(Xresponse)
    answer = answerCheck(Xresponse)
    if len(answer)!=0:
        break

'''
for line in response.__str__().split("\n"):    if line == ';ADDITIONAL':
'''        
#    print(line)
print("QUESTION SECTION:")
print(Xresponse[5])
print("ANSWER SECTION:")
for x in answer:
    print (x)

print("Query time:"+ str(Totaltime)) 
print("WHEN:", currentT) 
print("MSG SIZE rcvd:", len(Xresponse)) 


f= open("mydig_output.txt","a+")
f.write("QUESTION SECTION:"+'\n')
f.write(Xresponse[5]+'\n')
f.write("ANSWER SECTION:"+'\n')
for x in answer:
    f.write(x+'\n')

f.write("Query time:"+ str(Totaltime)+'\n')
f.write("WHEN:"+str(currentT)+'\n')
f.write("MSG SIZE rcvd:"+str(len(Xresponse))+'\n')
f.close()
'''
f= open("timeoutput.txt","a+")
f.write(str(Totaltime)+'\n')
f.close()
'''
#not allowed code
'''
#myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
#myAnswers = myResolver.query(website, "A") #Lookup the 'A' record(s) for website
#for rdata in myAnswers: #for each response
    #print (rdata) #print the data
'''
