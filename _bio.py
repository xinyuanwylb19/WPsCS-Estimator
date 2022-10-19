##########################################################
# Biofuel/Biochar carbon flux module                     #
# Xinyuan Wei                                            #
# 2022/08/19                                             #
##########################################################

import math

#%%
def bio_CFlux (ty,fuel_C,ce,char_C,dc1,dc2):
    
    # ty:      total years
    # fuel_C:  annual biofuel production
    # ce:      combustion efficiency (%, the rest will be convereted to charcoal) 
    # char_C:  annual biochar production
    # dc1:     charcoal decay parameter 1
    # dc2:     charcoal decay parameter 2
    
    C_char=[]   # annual charcoal production, charcoal from biofuel and biochar
    P_char=[]   # current year, charcoal carbon pool size
    D_char=[]   # decayed charcoal carbon in year i
    
    yr_A=0     # current charcoal carbon pool size  
    
    for i in range (ty):
        
        f_char=fuel_C.at[i]*((100-ce)/100)  # charcoal from biofuel
        yr_C=char_C.at[i]+f_char            # total charcoal production
        yr_A=yr_A+yr_C                      # charcoal carbon pool size  
        
        dr=dc1+dc2*math.log(yr_A)     # pool size-based decay rate
        yr_D=yr_A*dr
        yr_A=yr_A-yr_D
        
        C_char.append(yr_C)
        P_char.append(yr_A)
        D_char.append(yr_D)
    
    # Return:
    # annual charcoal production
    # charcoal carbon pool size
    # annual decayed charcoal
    return(C_char,P_char,D_char)        
    