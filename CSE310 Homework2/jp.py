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

website = "qq.com"
aroot =['198.41.0.4']
websites =['ns4.google.com.', 'ns1.google.com.', 'ns2.google.com.', 'ns3.google.com.']
'''
f= open("timeoutput.txt","a+")
for line in websites:
    i=0
    Totaltime = 0
    print(line)
    f.write(str(line)+'\n')
    while i <10:
        print(i)
        myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
        start = time.time()
        myAnswers = myResolver.query(website, "A") #Lookup the 'A' record(s) for website
        end = time.time()
        Totaltime = end-start
        f.write(str(Totaltime)+'\n')
        i+=1
f.close()
'''
for x in websites:
    m = dns.message.make_query(x, 'A')
    response = dns.query.udp(m, aroot[0])
    response = response.__str__().split("\n")
    #print(response)
    EX = IPextract(response)
    #print(EX)
    for a in EX:
        responses = dns.query.udp(m, a)
        #print(responses)
        responses = responses.__str__().split("\n")
        EXX = IPextract(responses)
        if EXX !=[]:
            break
print(EX)
print(EXX)
'''    
m = dns.message.make_query(website, 'A')    #ask root
response = dns.query.udp(m, aroot[0])
#print(response)
print('-'*8)
response = dns.query.udp(m, "121.51.160.100")
print(response)
print('-'*8)
m = dns.message.make_query('ns1.google.com', 'A')
response = dns.query.udp(m,  aroot[0])
print(response)

for x in aroot:
    response = dns.query.udp(m, x)          #get response
    print(response)
'''    

'''
myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
myAnswers = myResolver.query(website, "A") #Lookup the 'A' record(s) for website
for rdata in myAnswers: #for each response
    print (rdata) #print the data

'''
