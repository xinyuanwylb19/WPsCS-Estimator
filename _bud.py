##########################################################
# Building carbon flux module.                           #
# Xinyuan Wei                                            #
# 2022/08/19                                              #
##########################################################
import scipy.integrate as integrate
import math

#%%
def bud_CFlux (ty,bud_C,dp1,dp2,dp3,rp1,rp2):

    # ty:      total years
    # bud_C:   annual carbon flows into building carbon pool  
    # dp1:     building disposal rate parameter 1
    # dp2:     building disposal rate parameter 2
    # dp3:     building disposal rate parameter 3 (service life)
    # rp1:     building recycling rate parameter 1
    # rp2:     building recycling rate parameter 2
    
    C_bud=[]   # annual carbon fluxes into building carbon pool
    P_bud=[]   # current building carbon pool size
    D_bud=[]   # annual building carbon disposed
    R_bud=[]   # annual building carbon recycled
    L_bud=[]   # annual building carbon disposed to landfill

    # building disposal rate
    # TSP: time since production
    def bud_dr(TSP):
        part1=dp1/math.exp(math.sqrt(2*math.pi))
        part2=math.exp((-dp2*math.pow((TSP-dp3),2))/dp3)
        return(part1*part2) 
    
    # building carbon pool
    for i in range (ty): 
        acc_A=0   # current building carbon pool size
                
        for j in range (i+1):
            temp_A=0
            yr_C=bud_C.at[j]
            lfr=integrate.quad(bud_dr,0,i+1-j)[0]
            temp_A=temp_A+yr_C*(1-lfr)
            acc_A=acc_A+temp_A
        
        P_bud.append(acc_A)       
    
    # building carbon disposed
    for i in range (ty):
        acc_D=0
    
        for j in range (i+1):
            temp_D=0
            yr_C=bud_C.at[j]
            dfr=bud_dr(i-j+1)
            temp_D=yr_C*dfr
            acc_D=acc_D+temp_D
   
        D_bud.append(acc_D)
        
    # building carbon recycled
    for i in range (ty):
        temp_R=0
        # building carbon recycling rate 
        bdr=rp1+rp2*math.log(i+1)
        #print(bdr)
        
        # annual recycled building carbon 
        temp_R=bdr*D_bud[i]
        
        R_bud.append(temp_R)
        
    # building carbon disposed to landfill
    for i in range (ty):
        temp_L=D_bud[i]-R_bud[i]
        L_bud.append(temp_L)

    # Return:
    # annual carbon fluxes into the building carbon pool
    # building carbon pool size
    # disposed building carbon
    # recycled building carbon
    # disposed building carbon to landfill
    
    return(C_bud,P_bud,D_bud,R_bud,L_bud)

