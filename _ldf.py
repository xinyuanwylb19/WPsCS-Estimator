##########################################################
# Landfill carbon flux module                            #
# Xinyuan Wei                                            #
# 2022/08/20                                             #
##########################################################
import math
import scipy.integrate as integrate

#%%
def ldf_CFlux(ty,lf_pap,lf_bud,lf_exu,lf_hma,
              pap1,pap2,bud1,bud2,exu1,exu2,hma1,hma2):
    
    # ty:         total years
    # lf_pap:     annual paper carbon disposed to landfill
    # pa1:        paper in landfill decay parameter 1
    # pa2:        paper in landfill decay parameter 2
    
    C_lf=[]       # annual carbon fluxes into landfill
    P_lf=[]       # landfill carbon pool size
    D_lf=[]       # decayed landfill carbon
    
    Plf_pap=[]    # landfill paper carbon pool size 
    Dlf_pap=[]    # Decayed landfill paper carbon 
    
    Plf_bud=[]    # landfill building carbon pool size 
    Dlf_bud=[]    # decayed landfill building carbon 

    Plf_exu=[]    # landfill exterior use carbon pool size 
    Dlf_exu=[]    # decayed landfill exterior use carbon 
    
    Plf_hma=[]    # landfill home application carbon pool size 
    Dlf_hma=[]    # decayed landfill home application carbon 
 
    # landfill paper decay rate 
    def lpap_d(TSD):
        part1=math.log(TSD)*pap1
        part2=pap2*math.sqrt(2*math.pi)
        return(part1/part2)

    # landfill building decay rate 
    def lbud_d(TSD):
        part1=math.log(TSD)*bud1
        part2=bud2*math.sqrt(2*math.pi)
        return(part1/part2)

    # landfill exterior use decay rate 
    def lexu_d(TSD):
        part1=math.log(TSD)*exu1
        part2=exu2*math.sqrt(2*math.pi)
        return(part1/part2)
    
    # landfill home application decay rate 
    def lhma_d(TSD):
        part1=math.log(TSD)*hma1
        part2=hma2*math.sqrt(2*math.pi)
        return(part1/part2)

#%%    
##########################################################
# Landfill paper carbon decay.                           #
##########################################################                
    for i in range (ty): 
        acc_A=0  
        if i<=pap2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_pap[j]
                fr=abs(integrate.quad(lpap_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>pap2:
           for j in range (int(pap2)):
               temp_A=0
               yr_C=lf_pap[int(i-pap2+j)]
               fr=abs(integrate.quad(lpap_d,0,pap2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        Plf_pap.append(acc_A)
        
    # current year, decayed landfill paper carbon      
    for i in range (ty):
        
        if i==0:
            yr_D=lf_pap[i]-Plf_pap     
            
        if i>0:
            yr_D=Plf_pap[i-1]+lf_pap[i]-Plf_pap[i]
            
        Dlf_pap.append(yr_D)

#%% 
##########################################################
# Landfill building carbon decay.                        #
##########################################################                  
    for i in range (ty): 
        acc_A=0  
        if i<=bud2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_bud[j]
                fr=abs(integrate.quad(lbud_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>bud2:
           for j in range (int(bud2)):
               temp_A=0
               yr_C=lf_bud[int(i-bud2+j)]
               fr=abs(integrate.quad(lbud_d,0,bud2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        Plf_bud.append(acc_A)
        
    # current year, decayed landfill building carbon  
    for i in range (ty):
        
        if i==0:
            yr_D=lf_bud[i]-Plf_bud[i]
          
        if i>0:
            yr_D=Plf_bud[i-1]+lf_bud[i]-Plf_bud[i]
   
        Dlf_bud.append(yr_D)

#%% 
##########################################################
# Landfill exterior use carbon decay.                    #
##########################################################                 
    # Landfill exterior use carbon carbon pool.
    for i in range (ty): 
        acc_A=0  
        if i<=exu2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_exu[j]
                fr=abs(integrate.quad(lexu_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>exu2:
           for j in range (int(exu2)):
               temp_A=0
               yr_C=lf_exu[int(i-exu2+j)]
               fr=abs(integrate.quad(lexu_d,0,exu2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      

        Plf_exu.append(acc_A)
        
    # current year, decayed landfill exterior use carbon  
    for i in range (ty):
        
        if i==0:
            yr_D=lf_exu[i]-Plf_exu[i]
              
        if i>0:
            yr_D=Plf_exu[i-1]+lf_exu[i]-Plf_exu[i]
            
        Dlf_exu.append(yr_D)

#%% 
##########################################################
# Landfill home application carbon decay.                 #
##########################################################                 
    for i in range (ty): 
        acc_A=0  
        if i<=hma2:
            for j in range (i+1):
                temp_A=0
                yr_C=lf_hma[j]
                fr=abs(integrate.quad(lhma_d,0,i+1-j)[0])
                temp_A=temp_A+yr_C*(1-fr)
                acc_A=acc_A+temp_A
                
        if i>hma2:
           for j in range (int(hma2)):
               temp_A=0
               yr_C=lf_hma[int(i-hma2+j)]
               fr=abs(integrate.quad(lhma_d,0,hma2-j)[0])
               temp_A=temp_A+yr_C*(1-fr)
               acc_A=acc_A+temp_A      
        
        Plf_hma.append(acc_A)
        
    # current year, decayed landfill home application carbon  
    for i in range (ty):
        
        if i==0:
            yr_D=lf_hma[i]-Plf_hma[i]
        
        if i>0:
            yr_D=Plf_hma[i-1]+lf_hma[i]-Plf_hma[i]
            
        Dlf_hma.append(yr_D)

#%%         
    for i in range (ty):
        temp_C=lf_pap[i]+lf_bud[i]+lf_exu[i]+lf_hma[i]
    
        temp_P=Plf_pap[i]+Plf_bud[i]+Plf_exu[i]+Plf_hma[i]
    
        temp_D=Dlf_pap[i]+Dlf_bud[i]+Dlf_exu[i]+Dlf_hma[i]
        
        C_lf.append(temp_C)
        P_lf.append(temp_P)
        D_lf.append(temp_D)
    
    # Return:
    # annual carbon disposed to landfill
    # landfill carbon pool size
    # annual decayed landfill carbon
    return(C_lf,P_lf,D_lf)