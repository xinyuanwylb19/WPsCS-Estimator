##########################################################
# Exterior use carbon flux module                        #
# Xinyuan Wei                                            #
# 2022/08/27                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
def exu_CFlux (ty,exu_C,dp1,dp2,dp3):

    # ty:      total years
    # exu_C:   annual carbon fluxes into exterior use carbon pool  
    # dp1:     exterior use disposal rate parameter 1
    # dp2:     exterior use disposal rate parameter 2
    # dp3:     exterior use disposal rate parameter 3 (service life)
    
    C_exu=[] # annual carbon fluxes into exterior use carbon pool 
    P_exu=[] # current exterior use carbon pool size 
    L_exu=[] # annual exterior use carbon disposed to landfill 

    # exterior use disposal rate
    # TSP: time since production
    def exu_dr(TSP):
        part1=dp1/math.exp(math.sqrt(2*math.pi))
        part2=math.exp((-dp2*math.pow((TSP-dp3),2))/dp3)
        return(part1*part2) 
        
    # exterior use carbon pool 
    for i in range (ty): 
        
        acc_A=0     # current exterior use carbon pool size 
            
        for j in range (i+1):
            temp_A=0
            yr_C=exu_C.at[j]
            lfr=integrate.quad(exu_dr,0,i+1-j)[0]
            temp_A=temp_A+yr_C*(1-lfr)
            acc_A=acc_A+temp_A
               
        P_exu.append(acc_A)
    
    # exterior use disposed 
    for i in range (ty):
        acc_D=0
    
        for j in range (i+1):
            temp_D=0
            yr_C=exu_C.at[j]
            dfr=exu_dr(i-j+1)
            temp_D=yr_C*dfr
            acc_D=acc_D+temp_D
        
        L_exu.append(acc_D)


    # Return:
    # annual carbon fluxes into the exterior use carbon pool
    # exterior use carbon pool size
    # disposed exterior use carbon to landfill
    return(C_exu,P_exu,L_exu)
'''
import pandas as pd
buid=pd.read_csv("data.csv", sep=',')
buid_C=buid['Building']
results=exu_CFlux(49,buid_C,0.326,0.041,25)
print(results[1])
'''