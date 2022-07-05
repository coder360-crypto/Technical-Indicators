#Name:Ashish Patwa_Roll No:21MF10009
#fisher transform and ADX
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math



def fishertransform(x):
    if(x>0.999):
      x=0.999
    elif(x<(-0.999)):
      x=(-0.999)

    return .5 * math.log((1.0 + x) / (1.0 - x))


def fisherplot():

    df=pd.read_csv("stock_prices.csv")
    highprices= df['High'].to_numpy()
    lowprices= df['Low'].to_numpy()
    step = 10         #size of window for normalizing the price
    size=252       
    rows = size        
    mid = [0]*rows
    a=0.01 #smoothing factor
    for i in range(size):
        mid[i]=((highprices[i]+lowprices[i])/2)
    midf=[0]*252
    signal=[0]*252
    mid=np.array(mid)
    x=y=0
    prevx= 0
    prevj=0
    
    for j in range(step-1,252):
        maxel=-99999999
        minel= 99999999
        for i in range (j,j-step,-1):
            maxel=max(mid[i],maxel)
            minel=min(mid[i],minel)
         
        x = (a * 2 * (((float)((mid[j] - minel)) / (maxel - minel)) - .5)) + ((1 - a) * prevx)
        y = fishertransform(x) 
        midf[j]= y + midf[j-1]*0.5  
        signal[j]=midf[j-1]  
        prevx=x


    midf=np.array(midf)
    signal=np.array(signal)
    signal=np.delete(signal,0)
    midf=np.delete(midf,1)
    #print(midf)
    #print(signal)
    plt.plot(midf,color='r',label='Fisher transform',linewidth=0.5)
    plt.plot(signal,color='b',label='Signal line',linewidth=0.5)
    plt.axhline(y = 0,color='black',linewidth=0.2)
    #plt.ylim(-2,2)
    #plt.xlim(-1,260)
    plt.title("FISHER TRANSFORM")
    plt.legend()
    plt.show()
    

def adxin():
    df=pd.read_csv("stock_prices.csv")
    high= df['High'].to_numpy()
    low= df['Low'].to_numpy()
    close=df['Close'].to_numpy()
    truerange=[]
    podm=[]
    nedm=[]
    truerange.append(0)
    podm.append(0)
    nedm.append(0)
    for i in range (1,252):
       truerange.append(max(abs(high[i]-low[i]),abs(high[i]-close[i-1]),abs(low[i]-close[i])))
       if (high[i]-high[i-1]) > (low[i-1]-low[i]):
        podm.append(high[i]-high[i-1])
       else:
        podm.append(0)
       
       if low[i-1]-low[i] > high[i]-high[i-1]:
        nedm.append(low[i-1]-low[i])
       else:
        nedm.append(0)

    podm=np.array(podm)
    nedm=np.array(nedm)
    truerange=np.array(truerange)
    spodm=podm
    snedm=nedm
    strr=truerange
    step=15          #time interval for smoothing  
    meanp=0
    meann=0
    meantr=0
    for i in range(1,1+step):
       meanp+=(podm[i])
       meann+=(nedm[i])
       meantr+=(truerange[i])
       strr[i-1]=0
       spodm[i-1]=0
       snedm[i-1]=0
    
    strr[step]=(meantr)
    spodm[step]=(meanp)
    snedm[step]=(meann)
    meann/=step
    meanp/=step
    meantr/=step

    for i in range (1+step,252):
        spodm[i]=spodm[i-1]-(spodm[i-1]/step)+podm[i]
        snedm[i]=snedm[i-1]-(snedm[i-1]/step)+nedm[i]
        strr[i]=strr[i-1]-(strr[i-1]/step)+strr[i]

    pdi=[]
    ndi=[]
    dx=[0]*252
    adx=[0]*252
    pdi.append(0)
    ndi.append(0)
    #print(strr)
    for i in range (1,252):
        if strr[i]!=0:
            pdi.append((float)(spodm[i]/strr[i])*100)
            ndi.append((float)(snedm[i]/strr[i])*100)
        else :
            pdi.append(0)
            ndi.append(0)
       
    for i in range(step,252):
        dx[i]=((abs(pdi[i]-ndi[i])/(pdi[i]+ndi[i])))*100

    for i in range ((2*step),252):
        for j in range (i, i-step , -1):
            adx[i]+=(dx[j])
        adx[i]/=step
        

    #print(adx)
    #print(podm)
    pdi=np.array(pdi)
    ndi=np.array(ndi)
    adx=np.array(adx)
    remo1=[]
    remo=[]
    for i in range (step):
        remo.append(i)
        if(i<(step/2)):
            remo1.append(i)

    #print(remo) 
    #print(remo1) 
    remo=np.array(remo)
    remo1=np.array(remo1)
    pdi=np.delete(pdi,remo1)
    ndi=np.delete(ndi,remo1)
    adx=np.delete(adx,remo)
    plt.plot(pdi,color='green',label='+DI',linewidth=1.5)
    plt.plot(ndi,color='red',label='-DI',linewidth=1.5)
    plt.plot(adx,color='blue',label='ADX',linewidth=1.5)
    plt.xlim(0,260)
    #print(dx)
    #print(adx)
    plt.title("Average Directional Index")
    plt.legend()
    plt.show()



def main():
    fisherplot()
    adxin()
    #you can change the time window and smoothing factor to analyse the differences between peaks due to change in moving averages.

main()






