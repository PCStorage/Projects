import dpkt
import binascii

f = open('assignment3.pcap','rb')
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
    ethL.append(eth)

    #get IP and add
    ip = eth.data
    ipL.append(ip)

    #get TCP and add
    tcp = ip.data
    tcpL.append(tcp)

    #sort by ports
    if tcp.dport == 80:
        if tcp.sport in ports:
            ports[tcp.sport].append(tcp)
            #ports[tcp.sport] = ports[tcp.sport].append(tcp)
            ets[tcp.sport]  = ts
            Tlen[tcp.sport] =Tlen[tcp.sport]+len(eth)
            Tpacket[tcp.sport]=Tpacket[tcp.sport]+1
            timestamp[tcp.sport].append(ts)
        else:
            Nlist = []
            Nlist.append(tcp)
            ports[tcp.sport]  = Nlist
            sts[tcp.sport]    = ts
            Tlen[tcp.sport]   =len(eth)
            Tpacket[tcp.sport]=1
            XXX = []
            XXX.append(ts)
            timestamp[tcp.sport]=XXX
            
    if tcp.sport == 80:
        if tcp.dport in ports:
            ports[tcp.dport].append(tcp)
            ets[tcp.dport]  = ts
            Tlen[tcp.dport] =Tlen[tcp.dport]+len(eth)
            Tpacket[tcp.dport]=Tpacket[tcp.dport]+1
            timestamp[tcp.dport].append(ts)
            #ports[tcp.dport] = ports[tcp.dport].append(tcp)
        else:
            Nlist = []
            Nlist.append(tcp)
            ports[tcp.dport]  = Nlist
            sts[tcp.dport]    = ts
            Tlen[tcp.dport]   =len(eth)
            Tpacket[tcp.dport]=1
            XXX=[]
            XXX.append(ts)
            timestamp[tcp.dport]=XXX
        
    #counts messages sent from user130.245.145.12
    if ip.src == b'\x82\xf5\x91\x0c':
        i+=1
    '''
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data
    if tcp.dport == 80 and len(tcp.data) > 0:
     http = dpkt.http.Request(tcp.data)
     print (http.uri)
    

Part B Congestion control (30 points)
Using the same assignment2.pcap file and your analysis_pcap_tcp program, answer the
following questions about congestion control
For each TCP flow:


Submit (i) the answers to each question and a brief note about how you estimated each value,
(ii) the program if any you used to answer the two questions.

    Ethernet(
    src='\x00\x1a\xa0kUf',
    dst='\x00\x13I\xae\x84,',
    data=
    IP(
    src='\xc0\xa8\n\n',
    off=16384,
    dst='C\x17\x030',
    sum=25129,
    len=52,
    p=6,
    id=51105,
    data=
    TCP(
    seq=9632694,
    off_x2=128,
    ack=3382015884,
    win=54,
    sum=65372,
    flags=17,
    dport=80,
    sport=56145)))
'''

#a = int(bytes(ip[:1]).hex(),16)
print("Q1")
print("The number of TCP flows initiated from the sender:")
print(i,'\n')

#print(tcpL[0].dport,tcpL[0].sport)
#print(ports.keys())
'''
2  =syn
18 =syn,ack
16 =ack
24 =psh,ack
'''
print("2.a")
for x in ports.keys():
    TCP = ports[x]
    handshake = False
    ii=0
    while handshake == False:
        if TCP[ii].flags == 2:
            if TCP[ii+1].flags == 18:
                if TCP[ii+2].flags == 16:
                    handshake = True
                    
                    print("Port",'\t',x)
                    print("Sequence number:")
                    print(TCP[ii+3].seq,'\t',TCP[ii+4].seq)
                    print("Ack number:")
                    print(TCP[ii+3].ack,'\t',TCP[ii+4].ack)
                    print("Receive Window size:")
                    print(TCP[ii+3].win << TCP[0].opts[-1] ,'\t',TCP[ii+4].win << TCP[0].opts[-1],'\n')
        ii+=1
print("2.b")
for x in sts.keys():
    print("Throughput of port",x)
    print("Total time:",ets[x]-sts[x],'seconds')
    print("Total bytes:",Tlen[x])
    print("Throughput:=",Tlen[x]/(ets[x]-sts[x]),"b/s",'\n')

print("2.c")
for x in Tpacket.keys():
    TCP = ports[x]
    c=0
    loss=0
    while c < len(TCP)-1:
        #print(c)
        if TCP[c].sport != x:
            if TCP[c].ack ==TCP[c+1].ack:
                #print(c,TCP[c].seq,TCP[c].ack)
                loss+=1
        c+=1
        
    print ("Loss rate for port:",x)
    print (loss/Tpacket[x]*100,'%')
'''
(1) Print the first five congestion window sizes
(or till the end of the flow, if there are less than
five congestion windows). The congestion window is estimated at the sender.
What is the size
of the initial congestion window.
You need to estimate the congestion window size empirically
since the information is not available in the packet.
Comment on how the congestion window
size grows. Remember that your estimation may not be perfect,
but that is ok. Congestion
window sizes are estimated per RTT.
'''
print("Part B Congestion control")
print("1")
for x in Tpacket.keys():
    print("Congestion Window for Port",x)
    TCP = ports[x]
    c=3
    cwin =0
    timer=0
    slots=[]
    cd=0
    aack=0
    n=0
    '''
    recieving=0
    sending =0
    '''
    while c < len(TCP)-1:
        
        if TCP[c].sport != x :
            '''
            recieving+=1
            if sending !=0:
                print('s',sending)
            sending=0
            #print('rec',recieving)
            '''
            if len(slots) == 0:
                slots.append(cwin)
            
            else:
                if aack>=slots[n]:
                    #print(aack,slots[n])
                    aack=0
                    n+=1
                    slots.append(cwin)
                    cwin=0
            aack+=1
            '''
            #print(TCP[c].seq,TCP[c].ack,cwin)
            if cwin > 1:
                timer+=1
                print("Congestion Window",timer,"size =",cwin)
            '''    
            if len(slots)==5:
                break
            
        
        if TCP[c].sport == x:
            '''
            sending+=1
            #print('s',sending)
            if recieving != 0:
                print('rec',recieving)
            recieving=0
            '''
            #slots.append(cwin)
            cwin+=1
            #print(TCP[c].seq,TCP[c].ack,cwin)
        #print(n,cwin,aack)
        c+=1
    print(slots)
print("2")
'''
(2) Compute the number of times a retransmission occurred due to
triple duplicate ack and the
number of time a retransmission occurred due to timeout.
fast retransmission are stuck between dup ack
'''
#43498 2 fast re 1 re
#43500 4 fast re 19 re
#0 for 43502
for x in Tpacket.keys():
    print("Port",x)
    ackL = []
    TCP = ports[x]
    TS  = timestamp[x]
    '''
syn =x
xyn ack = y +1
seq x+1 y+1
    '''
    rtt=2*(TS[1]-TS[0])
    retransmission =0
    RT=[]
    c=4
    ack = TCP[1].ack
    count=0
    TripleA =0
    dupt=0
    
    while c < len(TCP)-1:
        #sending
        if TCP[c].sport == x:
            #print(TCP[c].seq,"seq")
            #add number to sequence checker
            if TCP[c].seq == TCP[c-1].ack:
                if count >= 3:
                    TripleA+=1
                else:
                    rt = TS[c]-dupt
                    if rt > 2*rtt:
                        retransmission+=1
            else:    
                RT.append(c)
        #return
        if TCP[c].sport != x:
            #print(TCP[c].ack)
            #not a duplicate
            if TCP[c].ack!=ack:
                count =1
                #update new value for next check
                ack=TCP[c].ack
                #rtt = time now -time send
                rt = TS[c]-TS[RT[0]]
                dupt=TS[RT[0]]
                RT.pop(0)
                if rt > 2*rtt:
                    #print(rt, rtt)
                    retransmission+=1 
                rtt = (0.875*rtt)+(0.125*rt)
            if TCP[c].ack==ack:
                rt = TS[c]-dupt
                if rt > 2*rtt:
                    #print(rt, rtt)
                    retransmission+=1 
                #rtt = (0.875*rtt) + (0.125*rt)
                count +=1
                #print(count,TCP[c-1].ack)
        c+=1
    print("Num of timeout retransmission:",retransmission,"Num of triple ack:",TripleA)
    # 1st port c=2839 -retransmisiion
    '''
    while c < len(TCP)-1:

        if TCP[c].sport == 80 and TCP[c].flags != 17 and TCP[c+1].sport != 80:
            if TCP[c].ack == TCP[c+1].seq:
                print(c,TCP[c+1].seq-TCP[0].seq)
            #print (TCP[c].seq,TCP[c+1].seq)
                retransmission+=1
        if TCP[c].sport == 80:
            ackL.append(TCP[c].ack)
            #print(TCP[c].ack)
        c+=1
    print("Number of retransmission:",retransmission)

    place =0
    count = 1
    c = 0
    TPA =0
    while c < len(ackL)-1:
        if place == ackL[c]:
            count+=1
        if place != ackL[c]:
            place = ackL[c]
            if count >=3:
                print(place,count)
                #print("Triple Ack")
                TPA +=1
            count=1
        #print(place,count)
        c+=1
    print("Total Number of Triple Acks = ",TPA)
'''
f.close()
