##########################################################
# Paper carbon flux module                               #
# Xinyuan Wei                                            #
# 2022/08/19                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
def pap_CFlux (ty,pap_C,dp1,dp2,dp3,rp1,rp2):
    
    # ty:      total years
    # pap_C:   annual carbon fluxes into paper carbon pool
    # dp1:     paper disposal rate parameter 1
    # dp2:     paper disposal rate parameter 2
    # dp3:     paper disposal rate parameter 3 (service life)
    # rp1:     paper recycling rate parameter 1
    # rp2:     paper recycling rate parameter 2

    
    C_pap=[]     # annual carbon fluxes into paper carbon pool 
    P_pap=[]     # current year, the accumulated paper carbon 
    D_pap=[]     # annual paper carbon disposed 
    R_pap=[]     # annual paper carbon recycled 
    L_pap=[]     # annual paper carbon disposed to landfill 
    
    # paper disposal rate 
    # TSD: time since production
    def pap_dr(TSP):
        part1=dp1/math.exp(math.sqrt(2*math.pi))
        part2=math.exp(-dp2*math.pow((TSP-dp3),2)/dp3)
        return(part1*part2)
             
    # accumulated paper carbon
    for i in range (ty): 
        # Current year, the accumulated paper carbon (Carbon Pool).
        acc_A=0
            
        if i<=dp3:
            for j in range (i+1):
                temp_A=0
                yr_C=pap_C[j]
                lfr=integrate.quad(pap_dr,0,i+1-j)[0]
                temp_A=temp_A+yr_C*(1-lfr)
                acc_A=acc_A+temp_A
        
        if i>dp3:
           for j in range (int(dp3)):
               temp_A=0
               yr_C=pap_C[int(i-dp3+j)]
               lfr=integrate.quad(pap_dr,0,dp3-j)[0]
               temp_A=temp_A+yr_C*(1-lfr)
               acc_A=acc_A+temp_A
 
        P_pap.append(acc_A)       
    
    # paper carbon disposed
    for i in range (ty):
        acc_D=0
    
        if i<=dp3:
            for j in range (i+1):
                temp_D=0
                yr_C=pap_C[j]
                dfr=pap_dr(i-j+1)
                temp_D=yr_C*dfr
                acc_D=acc_D+temp_D
                
        if i>dp3:
           for j in range (int(dp3)):
               temp_D=0
               yr_C=pap_C[int(i-dp3+j)]
               dfr=pap_dr(dp3-j+1)
               temp_D=yr_C*dfr
               acc_D=acc_D+temp_D
            
        D_pap.append(acc_D)
        
    # paper carbon recycled 
    for i in range (ty):
        temp_R=0
        # paper recycling rate 
        prr=rp1+rp2*math.log(i+1)
        
        # annual recycled papern 
        temp_R=prr*D_pap[i]
        
        R_pap.append(temp_R)
        
    # paper carbon disposed to landfill 
    for i in range (ty):
        temp_L=D_pap[i]-R_pap[i]
        L_pap.append(temp_L)
    
    # Return:
    # annual carbon fluxes into the paper carbon pool
    # paper carbon pool size
    # disposed paper carbon
    # recycled paper carbon
    # disposed paper carbon to landfill
    
    return(C_pap,P_pap,D_pap,R_pap,L_pap)
