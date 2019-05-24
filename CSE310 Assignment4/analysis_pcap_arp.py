import dpkt
import binascii

def hextoip(this):
    a=int(this[:2],16)
    b=int(this[2:4],16)
    c=int(this[4:6],16)
    d=int(this[6:8],16)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))
def hextomac(this):
    a=this[:2]
    b=this[2:4]
    c=this[4:6]
    d=this[6:8]
    e=this[8:10]
    f=this[10:12]
    return(a+':'+b+':'+c+':'+d+':'+e+':'+f)
    
f = open('assignment4_my_arp.pcap','rb')
pcap = dpkt.pcap.Reader(f)
#list of ports w/ array
ports   = {}
#list of start time by ports
sts     = {}
#list of end time by ports
ets     = {}
#Total length of packet
Tlen    = {}
#Total num of packet
Tpacket = {}
#list of ports w/ timestamp
timestamp = {}

ethL  = []
ipL   = []
tcpL  = []
i=0

for ts, buf in pcap:
    #get ethernet & add
    
    eth = dpkt.ethernet.Ethernet(buf)
    eth = bytes(eth)
    
    src = eth[:6]
    dst = eth[6:12]
    t = eth[12:14]
    Hardware= eth[14:16]
    Protocol = eth[16:18]
    Hsize = eth[19]
    Psize = eth[20]
    opcode = eth[20:22]
    SMAC = eth[22:28]
    SIP = eth[28:32]
    DMAC = eth[32:38]
    DIP  = eth[38:42]
    #print(t) 
    if t == b'\x08\x06':
        ethL.append(eth)


#eth = hex(eth)
#src = eth.hex()
#print(len(ethL))
for x in ethL:
    if int(x[20:22].hex())== 1:
        print("ARP Request")
    if int(x[20:22].hex()) == 2:
        print("ARP Reply")
    
    print("Destination MAC",hextomac(x[:6].hex()))
    print("Source MAC",hextomac(x[6:12].hex()))
    print("Destination IP",hextoip(x[38:42].hex()))
    print("Source IP",hextoip(x[28:32].hex()))
    print("Type:",x[12:14].hex(),"ARP")
    print("Optcode:",int(x[20:22].hex()))
    print("Hardware type:",x[14:16].hex())
    print("Protocol type:",x[16:18].hex())
    print("Hardware size:",x[18:19].hex())
    print("Protocol size",x[19:20].hex())
    #print(x.hex())
    print('-------------------------')
    

'''
Part B Analyze the ARP (85 points)
Your second task is to write a program ``analysis_pcap_arp” that analyzes the pcap trace for the
ARP packet. This is similar to your previous assignment, but this time you are not allowed to use
any structure. Perform a byte-level programming to read each byte and convert it to the ARP
header element---for example, the sender MAC address, target MAC address, protocol type, etc.
Refer to the ARP message structure in your book to determine the elements of the ARP
message.
Your program does not need to process each packet.
Instead, make sure for each packet you can
determine if the packet is a ARP packet or not,
and if it is an ARP packet then process it further.
Based on your analysis, answer the following questions:
(i)
Print the entire ARP request and
response for one ARP packet exchange
(preferably the one
you show in the screenshot above).
(ii) Based on the ARP messages, tell us the
IP address and MAC address of your router.
Explain
how you determined this.
Submit your well formatted program, answers to (i) and (ii) and a README that explains how to
run your program including details of your program logic for Part B
'''
    

f.close()
