##########################################################
# Home application carbon flux module                    #
# Xinyuan Wei                                            #
# 2022/08/19                                             #
##########################################################
import scipy.integrate as integrate
import math

#%%
def hma_CFlux (ty,hma_C,dp1,dp2,dp3,rp1,rp2):
    
    # ty:      total years
    # hma_C:   annual carbon fluxes into home application carbon pool
    # dp1:     home application disposal rate parameter 1 
    # dp2:     home application disposal rate parameter 2 
    # dp3:     home application disposal rate parameter 3 (service life)
    # rp1:     home application recycling rate parameter 1
    # rp2:     home application recycling rate parameter 2
    
    C_hma=[] # annual carbon fluxes into home application carbon pool 
    P_hma=[] # current home application carbon pool size 
    D_hma=[] # annual home application carbon disposed 
    R_hma=[] # annual home application carbon recycled 
    L_hma=[] # annual home application carbon disposed to landfill 
    
    # home application disposal rate 
    # TSD: time since production
    def hma_dr(TSP):
        part1=dp1/math.exp(math.sqrt(2*math.pi))
        part2=math.exp((-dp2*math.pow((TSP-dp3),2))/dp3)
        return(part1*part2)
             
    # home application carbon pool 
    for i in range (ty): 
        acc_A=0     # current home application carbon pool size 
            
        for j in range (i+1):
            temp_A=0
            yr_C=hma_C.at[j]
            lfr=integrate.quad(hma_dr,0,i+1-j)[0]
            temp_A=temp_A+yr_C*(1-lfr)
            acc_A=acc_A+temp_A
        
        P_hma.append(acc_A)       
    
    # home application carbon disposed 
    for i in range (ty):
        acc_D=0
    
        for j in range (i+1):
            temp_D=0
            yr_C=hma_C.at[j]
            dfr=hma_dr(i-j+1)
            temp_D=yr_C*dfr
            acc_D=acc_D+temp_D


        D_hma.append(acc_D)
        
    # home application carbon recycled 
    for i in range (ty):
        # home application recycling rate 
        har=rp1+rp2*math.log(i+1)
        
        # annual recycled home application 
        temp_R=D_hma[i]*har
        R_hma.append(temp_R)

    # home application carbon disposed to landfill 
    for i in range (ty):
        temp_L=D_hma[i]-R_hma[i]
        L_hma.append(temp_L) 

    # Return:
    # annual carbon fluxes into the home application carbon pool
    # home application carbon pool size
    # disposed home application carbon
    # recycled home application carbon
    # disposed home application carbon to landfill

    return(C_hma,P_hma,D_hma,R_hma,L_hma)