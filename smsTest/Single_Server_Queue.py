import numpy as np
import sys
import random as rn

def genIAT(mean, sd, rows):#generate gaussian inter-arrival time array
    s = np.random.normal(mean,sd,rows)#create array
    s=s-min(s)#remove negative values
    s=[round(num,1) for num in s]#round of to significant numbers
    return s
def genSer(mean, sd,rows):#generate gaussian service time array
    s = np.random.normal(mean,sd,rows)
    s=s-min(s)
    s=[round(num,1) for num in s]
    return s
def genIATIID(delay_cust, rows):#generate IID inter-arrival time
    arr=[]
    for x in range(rows):
        arr.append(round(rn.uniform(0,delay_cust),1))#generate a random delay
    return arr
def genSerIID(max_service_time, rows):
    arr=[]
    for x in range(rows):
        arr.append(round(rn.uniform(0,max_service_time),1))
    return arr
def calArr(iat):#calculate arrival time array from IAT
    ar=[]
    for x in range(len(iat)):
        if x==0:
            ar.append(iat[0])#first arrival is same as iat
        else:
            ar.append(round(iat[x]+ar[x-1],1))#calculate arrival
    #ar.sort()
    return ar
def binarySearchCount(arr, n, time):#used to find queue length at a given time
    left = 0
    right = n - 1
    count = 0
    while (left <= right): 
        mid = int((right + left) / 2)
        if (arr[mid] <= time): 
            count = mid + 1
            left = mid + 1
        else:
            right = mid - 1
     
    return count

num=rn.randint(0,100)#random number of rows/customers
iat=[]
ser=[]

print("Enter 1 for gaussian 2 for IID:")
inp=int(input())
if inp==1:
    print("gaussian")
    print("Enter Mean:")
    mean=int(input())
    print("Enter SD:")
    sd=int(input())
    iat=genIAT(mean,sd,num)#inter-arrival time array
    ser=genSer(mean, sd,num)#service time array
elif inp==2:
    print("IID")
    print("Enter Max time delay between customers:")
    delay_cust=int(input())
    print("Enter Max time of Service:")
    max_serve_time=int(input())
    iat=genIATIID(delay_cust, num)#inter-arrival time array
    ser=genSerIID(max_serve_time, num)#service time array
else:
    sys.exit("Invalid Choice!")

arr=calArr(iat)#arrival time array
delay=[]#array for delay/wait
start_Ser=[]#when a customer is started being served
leave=[]#record exit time of row/customer
que_len=[]#queue length when a customer is being served
cust_Count=0
for x in range(num):
    if x==0:#for first row
        start_Ser.append(arr[0])
        cust_Count+=1
        que_len.append(0)
        leave.append(round(start_Ser[0]+ser[0],1))
        delay.append(0.0)
    else:
        start_Ser.append(round(leave[x-1],1))#start serving when last customer left
        que_len.append(binarySearchCount(#find queue length
            arr[cust_Count:], num-cust_Count, start_Ser[x]))#arr removing those served,length of arr passed, time when started serving 
        cust_Count+=1
        leave.append(round(start_Ser[x]+ser[x],1))#start serving+service time
        dely=(round(start_Ser[x]-arr[x]))#start serving-arrival time
        if dely<0:
            delay.append(0)
        else:
            delay.append(dely)
        
print("ID"+"\tIAT"+"\tArr"+"\tDelay"+"\tStart"+"\tServe"+"\tExit"+"\tQueue")
for i in range(num):
    print(str(i+1)+'\t'+str(iat[i])+'\t'+str(arr[i])+'\t'+str(delay[i])+'\t'
          +str(start_Ser[i])+'\t'+str(ser[i])+'\t'+str(leave[i])
          +'\t'+str(que_len[i]))
Wq=round(sum(delay)/num,2)#average waiting time
print("Average wait time: "+str(Wq))
W=round(sum(leave)/num,2)#average time in system
print("Average time in System: "+str(W))
n=rn.randint(0, num-1)
Pn=round(leave[n]/leave[num-1],2)#prob of time taken by n customers in system
print("Probabilty of "+str(n)+" customers in System: "+str(Pn))
sum_zero=0
for i in range(1,num):
    if que_len[i]==0:
        sum_zero+=(arr[i]-start_Ser[i-1])#currentstart of serve prev
P0=round((sum_zero+arr[0])/leave[num-1],2)#prob of 0 customer in queue
print("Probabilty of Zero in Queue: "+str(P0))
Lq=round(sum(que_len)/num,2) #average Customers in queue
print("Average Customers in Queue: "+str(Lq))
