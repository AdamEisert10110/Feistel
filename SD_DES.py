#Block Size b = 8 bits#Key Size K = 12 bits##Rounds N = 3#8 bit, 2 hex
import pdb
import math
from matplotlib import pyplot as plt

def feistel(message,key,n1):
    x = format(ord(message),"08b")
    L1,R1 = x[0:4],x[4:8]
    L2 = R1
    t = "0b"+R1
    t = int(t,base=2)
    L11 = int(L1,base=2)
    if(n1 == 0):
        m = t ^ key[0] ^ L11
    if(n1==1):
        m = t ^ key[1] ^ L11
    if(n1==2):
        m = t ^ key[2] ^ L11  
    m = format(m,"04b")
    m = L2+m
    m = int(m,base=2)
    return(m)


def feistel_dec(message,key,n1):
    x = format(ord(message),"08b")
    L2,R2 = x[0:4],x[4:8]
    R1 = L2
    t="0b"+L2
    t=int(t,base=2)
    R11 = int(R2,base=2)
    if(n1==2):
        m=t^key[2]^R11
    if(n1==1):
        m=t^key[1]^R11
    if(n1==0):
        m=t^key[0]^R11
    m=format(m,"04b")
    m=m+R1
    m=int(m,base=2)
    return(m)

def key_sched(key):
    k = list(bin(key))
    k1,k2,k3 = "".join(k[2:6]),"".join(k[6:10]),"".join(k[10:14])
    k1,k2,k3 = '0b'+str(k1),'0b'+str(k2),'0b'+str(k3)
    k1,k2,k3 = int(k1,base=2),int(k2,base=2),int(k3,base=2)
    k1_2,k2_2,k3_2 = k1^k2,k2^k3,k3^k1
    return(k1_2,k2_2,k3_2)

def sd_des(message,key):
    m = list(message)
    k = key_sched(int(key))
    encTot,enc = [],[]
    for i in range(len(m)):
        if(i > 0):
            enc = []  
        for ii in range(3):
            if(ii == 0):
                message = m[0]
                temp = feistel(m[i],k,ii)
                enc.append(hex(temp))
            else:
                message = enc[ii-1]
                temp = feistel(chr(int(message,base=16)),k,ii)
                enc.append(hex(temp))
            if(ii==2):
                encTot.append(enc[2])
    return encTot
            
def pre_e(message,key):
    if(key > 4095):
        print("Key size Too Large")
        return 
    else:
        x = sd_des(message,key)
        s = ''.join(chr(int(e,base=16)) for e in x)
        return(x,s)

def sd_des_dec(message,key):
    i=0
    m=list(message)
    k=key_sched(int(key))
    decTot,dec=[],[]
    for i in range(len(m)):
        if(i>0):
            dec=[]
        for ii in range(3):
            if(ii==0):
                message=m[0]
                temp = feistel_dec(m[i],k,2)
                dec.append(hex(temp))
            else:
                message=dec[ii-1]
                temp=feistel_dec(chr(int(message,base=16)),k,2-ii)
                dec.append(hex(temp))
            if(ii==2):
                decTot.append(dec[2])
    return decTot
                
def pre_d(message,key):
    if(key > 4095):
        print("Key size too large")
        return
    else:
        x = sd_des_dec(message,key)
        s = ''.join(chr(int(e,base=16)) for e in x)
        return(x,s)
    
c = pre_e('Hello Friend, its good to see you again.',0xf8c)
p = pre_d(c[1],0xf8c)

print(c[1])
print(p[1])
