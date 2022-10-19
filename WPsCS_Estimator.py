####################################################################
# Wood products carbon storage estimator (WPsCS Estimator v1.0)    #
# Developed by Xinyuan Wei                                         #
# Updated 2022/08/20                                               #
# Version 1.0                                                      #
####################################################################
import base64
import tkinter
import tkinter.simpledialog
import pandas as pd
import os

import _bio as bio
import _pap as pap
import _bud as bud
import _exu as exu
import _hma as hma
import _ldf as ldf

from tkinter import messagebox
from PIL import Image, ImageTk
#from image import *
#%%
# define interface 
class MainForm: 

    def __init__(self): # window
        self.root=tkinter.Tk() 
        self.root.title("WPsCS Estimator v1.0" )
        self.root.geometry("850x950")
        
        # ----- Input label -----
        label_input=tkinter.Label(self.root,text="Input data",
                                  justify="left",height="3",
                                  font=("Century Gothic",12))
        # ----- Input data-----
        self.text_input=tkinter.Text(self.root,width=20,height=1,
                                     font=("Century Gothic",12))
        self.text_input.insert("current","Data_WPs.csv")

        # ----- Output label -----
        label_output=tkinter.Label(self.root,text="Result",justify="left",
                                   height="3",font=("Century Gothic",12))
        # ----- Output result-----
        self.text_output=tkinter.Text(self.root,width=20,height=1,
                                      font=("Century Gothic",12))
        self.text_output.insert("current","WPCS_Results.csv")
        
        # ----- Run button-----
        self.button=tkinter.Button(self.root,text="Run",fg="black",
                                   width="5",bg="cyan",height="1",
                                   font=("Century Gothic",12))
        self.button.bind("<Button-1>",lambda event:self.event_handle(event))

#        with open('logo.jpg', 'wb') as w:
#          w.write(base64.b64decode(logo_jpg))

        img=Image.open('logo.jpg')
        reimg=img.resize((250,130), Image.ANTIALIAS)
        logo=ImageTk.PhotoImage(reimg)
        label_logo=tkinter.Label(image=logo)
        label_logo.image=logo
        label_logo.place(x=600, y=820)

#%%
        # ----- Biofuel and biochar -----
        # combustion efficiency
        label_bb=tkinter.Label(self.root,text="Biofuel and biochar parameters",
                               justify="left",height="3",
                               font=("Times",16))
        
        label_ce=tkinter.Label(self.root,text="Combustion Efficiency (%)",
                               justify="left",height="1",
                               font=("Century Gothic",12))
        
        self.text_ce=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_ce.insert("current",96.0)

        # charcoal decay
        label_charcoal=tkinter.Label(self.root,text="Charcoal decay rate",
                                     justify="left",height="1",
                                     font=("Century Gothic",12))
        
        label_char_dc1=tkinter.Label(self.root,text="\u03C1",justify="left",
                                     font=("Century Gothic",12))                                  
        self.text_char_dc1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_char_dc1.insert("current",0.007)
        
        label_char_dc2=tkinter.Label(self.root,text="\u03C3",justify="left",
                                     font=("Century Gothic",12))
        self.text_char_dc2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_char_dc2.insert("current", 0.0003)

#%%
        # ----- Wood products disposal parameters -----
        label_wps=tkinter.Label(self.root,text="Wood products disposal parameters",
                                justify="left",height="3",
                                font=("Times",16))
                
        label_dp1=tkinter.Label(self.root,text="\u03B1",
                                justify="left",font=("Century Gothic",12))
        label_dp2=tkinter.Label(self.root,text="\u03B2",
                                justify="left",font=("Century Gothic",12))
        label_dp3=tkinter.Label(self.root,text="\u03B3",
                                justify="left",font=("Century Gothic",12)) 
        
        # ----- Building disposal parameter -----
        label_dbud=tkinter.Label(self.root,text="Building",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))       
        
        self.text_bud_dp1=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_bud_dp1.insert("current",0.133) 
        self.text_bud_dp2=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_bud_dp2.insert("current",0.028)
        self.text_bud_dp3=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_bud_dp3.insert("current",80.0)

        # ----- Exterior use disposal parameter -----
        label_dexu=tkinter.Label(self.root,text="Exterior use",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_exu_dp1=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_exu_dp1.insert("current",0.326)
        self.text_exu_dp2=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_exu_dp2.insert("current",0.041)
        self.text_exu_dp3=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_exu_dp3.insert("current",25.0)

        # ----- Home application disposal parameter -----
        label_dhma=tkinter.Label(self.root,text="Home application",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_hma_dp1=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_hma_dp1.insert("current",0.265)
        self.text_hma_dp2=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_hma_dp2.insert("current",0.031)
        self.text_hma_dp3=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_hma_dp3.insert("current",30.0)

        # ----- Newspaper disposal parameter -----
        label_dpapn=tkinter.Label(self.root,text="Newspaper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))
        
        self.text_papn_dp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papn_dp1.insert("current",3.062)
        self.text_papn_dp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papn_dp2.insert("current",0.0)
        self.text_papn_dp3=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papn_dp3.insert("current",2.0)

        # ----- Graphic paper disposal parameter -----
        label_dpapg=tkinter.Label(self.root,text="Graphic paper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))
        
        self.text_papg_dp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papg_dp1.insert("current",1.006)
        self.text_papg_dp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papg_dp2.insert("current",0.0)
        self.text_papg_dp3=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papg_dp3.insert("current",6.0)

        # ----- Packing paper disposal parameter -----
        label_dpapp=tkinter.Label(self.root,text="Packing paper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))
        self.text_papp_dp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papp_dp1.insert("current",6.036)
        self.text_papp_dp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papp_dp2.insert("current",0.0)
        self.text_papp_dp3=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papp_dp3.insert("current",1.0)

        # ----- Household paper disposal parameter -----
        label_dpaph=tkinter.Label(self.root,text="Household paper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))
        self.text_paph_dp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_paph_dp1.insert("current",12.036)
        self.text_paph_dp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_paph_dp2.insert("current",0.0)
        self.text_paph_dp3=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_paph_dp3.insert("current",0.5)
        
#%%
        # ----- Recycling rate -----
        label_recycling=tkinter.Label(self.root,text="Recycling rate parameters",
                                      justify="left",height="3",
                                      font=("Times",16))
        
        label_rp1=tkinter.Label(self.root,text="\u03BB",
                                justify="left",font=("Century Gothic",12))
        label_rp2=tkinter.Label(self.root,text="\u03BC",
                                justify="left",font=("Century Gothic",12))
        
        # ----- Building recycling rate parameter -----
        label_rbud=tkinter.Label(self.root,text="Building",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_bud_rp1=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_bud_rp1.insert("current",0.085)
        self.text_bud_rp2=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_bud_rp2.insert("current",0.015)
        
        # ----- Home application recycling rate parameter -----
        label_rhma=tkinter.Label(self.root,text="Home application",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_hma_rp1=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_hma_rp1.insert("current",0.085)
        self.text_hma_rp2=tkinter.Text(self.root,width=10,height=1,
                                       font=("Century Gothic",12))
        self.text_hma_rp2.insert("current",0.015)
        
        # ----- Newspaper recycling rate parameter -----
        label_rpapn=tkinter.Label(self.root,text="Newspaper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))

        self.text_papn_rp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papn_rp1.insert("current",0.225)
        self.text_papn_rp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papn_rp2.insert("current",0.027)

        # ----- Graphic paper recycling rate parameter -----
        label_rpapg=tkinter.Label(self.root,text="Graphic paper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))

        self.text_papg_rp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papg_rp1.insert("current",0.225)
        self.text_papg_rp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papg_rp2.insert("current",0.027)
        
        # ----- Packing paper recycling rate parameter -----
        label_rpapp=tkinter.Label(self.root,text="Packing paper",
                                  justify="left",height="1",
                                  font=("Century Gothic",12))
        
        self.text_papp_rp1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papp_rp1.insert("current",0.225)
        self.text_papp_rp2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_papp_rp2.insert("current",0.027)
        
#%%
        # ----- Decay parameters for landfills -----
        label_landfills=tkinter.Label(self.root,text="Landfill decay parameters",
                                      justify="left",height="3",
                                      font=("Times",16))
        
        label_ldfp1=tkinter.Label(self.root,text="\u03BE",
                                 justify="left",font=("Century Gothic",12))
        label_ldfp2=tkinter.Label(self.root,text="\u03C9",
                                 justify="left",font=("Century Gothic",12))
        
        # ----- Building decay parameter -----
        label_lbud=tkinter.Label(self.root,text="Building",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))

        self.text_ldf_bdp1 = tkinter.Text(self.root,width=10,height=1,
                                          font=("Century Gothic",12))
        self.text_ldf_bdp1.insert("current",0.997)
        self.text_ldf_bdp2 = tkinter.Text(self.root,width=10,height=1,
                                          font=("Century Gothic",12))
        self.text_ldf_bdp2.insert("current",30)
        
        # ----- Exterior use decay parameter -----
        label_lexu=tkinter.Label(self.root,text="Exterior use",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_ldf_eup1 = tkinter.Text(self.root,width=10,height=1,
                                          font=("Century Gothic",12))
        self.text_ldf_eup1.insert("current",1.178)
        self.text_ldf_eup2 = tkinter.Text(self.root,width=10,height=1,
                                          font=("Century Gothic",12))
        self.text_ldf_eup2.insert("current",20)
        
        # ----- Home application decay parameter -----
        label_lhma=tkinter.Label(self.root,text="Home application",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_ldf_hap1 = tkinter.Text(self.root,width=10,height=1,
                                          font=("Century Gothic",12))
        self.text_ldf_hap1.insert("current",1.329)
        self.text_ldf_hap2 = tkinter.Text(self.root,width=10,height=1,
                                          font=("Century Gothic",12))
        self.text_ldf_hap2.insert("current",15)
        
        # ----- Paper decay parameter -----
        label_lpap=tkinter.Label(self.root,text="Paper",
                                 justify="left",height="1",
                                 font=("Century Gothic",12))
        
        self.text_ldf_pap1=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_ldf_pap1.insert("current",0.821)
        self.text_ldf_pap2=tkinter.Text(self.root,width=10,height=1,
                                        font=("Century Gothic",12))
        self.text_ldf_pap2.insert("current",5)

#%%
        # ----- Input, output, and run button -----
        label_input.grid(row=1,column=1)
        self.text_input.grid(row=1,column=2)
        label_output.grid(row=1,column=3)
        self.text_output.grid(row=1,column=4)
        
        # Run button
        self.button.grid(row=1,column=6)
        
        # ----- Biofuel and biochar -----
        label_bb.grid(row=2,column=2,columnspan=3)
        
        label_ce.grid(row=3,column=1,columnspan=1,sticky="W")
        self.text_ce.grid(row=3,column=3)

        label_charcoal.grid(row=4,column=1,columnspan=1,sticky="W")
        label_char_dc1.grid(row=4,column=2)
        self.text_char_dc1.grid(row=4,column=3)
        label_char_dc2.grid(row=4,column=4)
        self.text_char_dc2.grid(row=4,column=5)
        
        # ----- Wood products disposal parameters -----
        label_wps.grid(row=5,column=2,columnspan=3)
        label_dp1.grid(row=6,column=2)
        label_dp2.grid(row=6,column=3)
        label_dp3.grid(row=6,column=4)
        
        label_dbud.grid(row=7,column=1,sticky="W")
        self.text_bud_dp1.grid(row=7,column=2)
        self.text_bud_dp2.grid(row=7,column=3)
        self.text_bud_dp3.grid(row=7,column=4)
        
        label_dexu.grid(row=8,column=1,sticky="W")
        self.text_exu_dp1.grid(row=8,column=2)
        self.text_exu_dp2.grid(row=8,column=3)
        self.text_exu_dp3.grid(row=8,column=4)
        
        label_dhma.grid(row=9,column=1,sticky="W")
        self.text_hma_dp1.grid(row=9,column=2)
        self.text_hma_dp2.grid(row=9,column=3)
        self.text_hma_dp3.grid(row=9,column=4)
        
        label_dpapn.grid(row=10,column=1,sticky="W")
        self.text_papn_dp1.grid(row=10,column=2)
        self.text_papn_dp2.grid(row=10,column=3)
        self.text_papn_dp3.grid(row=10,column=4)
        
        label_dpapg.grid(row=11,column=1,sticky="W")
        self.text_papg_dp1.grid(row=11,column=2)
        self.text_papg_dp2.grid(row=11,column=3)
        self.text_papg_dp3.grid(row=11,column=4)
        
        label_dpapp.grid(row=12,column=1,sticky="W")
        self.text_papp_dp1.grid(row=12,column=2)
        self.text_papp_dp2.grid(row=12,column=3)
        self.text_papp_dp3.grid(row=12,column=4)
        
        label_dpaph.grid(row=13,column=1,sticky="W")
        self.text_paph_dp1.grid(row=13,column=2)
        self.text_paph_dp2.grid(row=13,column=3)
        self.text_paph_dp3.grid(row=13,column=4)

        # ----- Recycling rate -----
        label_recycling.grid(row=14,column=2,columnspan=3)
        label_rp1.grid(row=15,column=2)
        label_rp2.grid(row=15,column=3)
        
        label_rbud.grid(row=16,column=1,sticky="W") 
        self.text_bud_rp1.grid(row=16,column=2)
        self.text_bud_rp2.grid(row=16,column=3)
        
        label_rhma.grid(row=17,column=1,sticky="W")
        self.text_hma_rp1.grid(row=17,column=2)
        self.text_hma_rp2.grid(row=17,column=3)
        
        label_rpapn.grid(row=18,column=1,sticky="W")
        self.text_papn_rp1.grid(row=18,column=2)
        self.text_papn_rp2.grid(row=18,column=3)

        label_rpapg.grid(row=19,column=1,sticky="W")
        self.text_papg_rp1.grid(row=19,column=2)
        self.text_papg_rp2.grid(row=19,column=3)
        
        label_rpapp.grid(row=20,column=1,sticky="W")
        self.text_papp_rp1.grid(row=20,column=2)
        self.text_papp_rp2.grid(row=20,column=3)
        
        # ----- Decay parameters for landfills -----
        label_landfills.grid(row=21,column=2,columnspan=3)
        label_ldfp1.grid(row=22,column=2)
        label_ldfp2.grid(row=22,column=3)
        
        label_lbud.grid(row=23,column=1,sticky="W")      
        self.text_ldf_bdp1.grid(row=23,column=2)   
        self.text_ldf_bdp2.grid(row=23,column=3)
        
        label_lexu.grid(row=24,column=1,sticky="W")
        self.text_ldf_eup1.grid(row=24,column=2)
        self.text_ldf_eup2.grid(row=24,column=3)
        
        label_lhma.grid(row=25,column=1,sticky="W")
        self.text_ldf_hap1.grid(row=25,column=2)
        self.text_ldf_hap2.grid(row=25,column=3)
        
        label_lpap.grid(row=26,column=1,sticky="W")
        self.text_ldf_pap1.grid(row=26,column=2)
        self.text_ldf_pap2.grid(row=26,column=3)

        self.root.mainloop()

    def event_handle(self,event):
        input_name=self.text_input.get("0.0","end")[:-1]
        output_name=self.text_output.get("0.0","end")[:-1]
        # scenario file
        sc='WP_Data'
        directory=os.getcwd()+chr(92)+sc
        print(directory)

        # read the wood products data
        WP_filename=directory+chr(92)+input_name
        WP_data=pd.read_csv(WP_filename,sep=',')

        # print the time period information
        total_yr=len(WP_data)
        sy=WP_data['Year'].at[0]
        ey=WP_data['Year'].at[total_yr-1]
        print('The time period is ',sy,'-',ey,'.')
        print(total_yr,'years in total.')
        print('')

        ##########################################################
        # Read wood products carbon fluxes parameters            #
        ##########################################################
        # charcoal parameters
        cha_dc1=float(self.text_char_dc1.get("0.0","end"))
        cha_dc2=float(self.text_char_dc2.get("0.0","end"))
        ce=float(self.text_ce.get("0.0","end"))
        
        # building parameters
        bud_dp1=float(self.text_bud_dp1.get("0.0","end"))
        bud_dp2=float(self.text_bud_dp2.get("0.0","end"))
        bud_dp3=float(self.text_bud_dp3.get("0.0","end"))
        bud_rp1=float(self.text_bud_rp1.get("0.0","end"))
        bud_rp2=float(self.text_bud_rp2.get("0.0","end"))

        # exterior use parameters
        exu_dp1=float(self.text_exu_dp1.get("0.0","end"))
        exu_dp2=float(self.text_exu_dp2.get("0.0","end"))
        exu_dp3=float(self.text_exu_dp3.get("0.0","end"))

        # home application parameters
        hma_dp1=float(self.text_hma_dp1.get("0.0","end"))
        hma_dp2=float(self.text_hma_dp2.get("0.0","end"))
        hma_dp3=float(self.text_hma_dp3.get("0.0","end"))
        hma_rp1=float(self.text_hma_rp1.get("0.0","end"))
        hma_rp2=float(self.text_hma_rp2.get("0.0","end"))
        
        # newspaper parameters
        papn_dp1=float(self.text_papn_dp1.get("0.0","end"))
        papn_dp2=float(self.text_papn_dp2.get("0.0","end"))
        papn_dp3=float(self.text_papn_dp3.get("0.0","end"))
        papn_rp1=float(self.text_papn_rp1.get("0.0","end"))
        papn_rp2=float(self.text_papn_rp2.get("0.0","end"))
        
        # graphic paper parameters
        papg_dp1=float(self.text_papn_dp1.get("0.0","end"))
        papg_dp2=float(self.text_papn_dp2.get("0.0","end"))
        papg_dp3=float(self.text_papn_dp3.get("0.0","end"))
        papg_rp1=float(self.text_papn_rp1.get("0.0","end"))
        papg_rp2=float(self.text_papn_rp2.get("0.0","end"))
        
        # packing paper parameters
        papp_dp1=float(self.text_papn_dp1.get("0.0","end"))
        papp_dp2=float(self.text_papn_dp2.get("0.0","end"))
        papp_dp3=float(self.text_papn_dp3.get("0.0","end"))
        papp_rp1=float(self.text_papn_rp1.get("0.0","end"))
        papp_rp2=float(self.text_papn_rp2.get("0.0","end"))
        
        # household paper parameters
        paph_dp1=float(self.text_papn_dp1.get("0.0","end"))
        paph_dp2=float(self.text_papn_dp2.get("0.0","end"))
        paph_dp3=float(self.text_papn_dp3.get("0.0","end"))

        # landfill parameters
        ldf_pap1=float(self.text_ldf_pap1.get("0.0","end"))
        ldf_pap2=float(self.text_ldf_pap2.get("0.0","end"))
        ldf_bdp1=float(self.text_ldf_bdp1.get("0.0","end"))
        ldf_bdp2=float(self.text_ldf_bdp2.get("0.0","end"))
        ldf_eup1=float(self.text_ldf_eup1.get("0.0","end"))
        ldf_eup2=float(self.text_ldf_eup2.get("0.0","end"))
        ldf_hap1=float(self.text_ldf_hap1.get("0.0","end"))
        ldf_hap2=float(self.text_ldf_hap2.get("0.0","end"))

        # ----- Calculating -----
        # pead the products data
        pd_file=directory+chr(92)+input_name
        pd_data=pd.read_csv(pd_file, sep=',')

        char_C=pd_data['Biochar']
        fuel_C=pd_data['Biofuel']
        buid_C=pd_data['Building']
        exus_C=pd_data['Exterior_use']
        hmap_C=pd_data['Home_application']
        papn_C=pd_data['Newspaper']
        papg_C=pd_data['Graphic_paper']
        papp_C=pd_data['Packing_paper']
        paph_C=pd_data['Household_paper']

        # estimate carbon pool size
        # charcoal
        cc_results=bio.bio_CFlux(total_yr,fuel_C,ce,char_C,cha_dc1,cha_dc2)
        
        # building
        bd_results=bud.bud_CFlux(total_yr,buid_C,bud_dp1,bud_dp2,bud_dp3,bud_rp1,bud_rp2)

        # exterior use
        eu_results=exu.exu_CFlux(total_yr,exus_C,exu_dp1,exu_dp2,exu_dp3)

        # home application
        ha_results=hma.hma_CFlux(total_yr,hmap_C,hma_dp1,hma_dp2,hma_dp3,hma_rp1,hma_rp2)
        
        # newspaper
        pn_results=pap.pap_CFlux(total_yr,papn_C,papn_dp1,papn_dp2,papn_dp3,papn_rp1,papn_rp2)

        # graphic paper
        pg_results=pap.pap_CFlux(total_yr,papg_C,papg_dp1,papg_dp2,papg_dp3,papg_rp1,papg_rp2)
        
        # packing paper
        pp_results=pap.pap_CFlux(total_yr,papp_C,papp_dp1,papp_dp2,papp_dp3,papp_rp1,papp_rp2)
        
        # household paper
        ph_results=pap.pap_CFlux(total_yr,paph_C,paph_dp1,paph_dp2,paph_dp3,0,0)

        # estimate landfill carbon pool size        
        lf_bud=bd_results[4]  # building
        lf_exu=eu_results[2]  # exterior Use
        lf_hma=ha_results[4]  # home application
        lf_ppn=pn_results[4]  # newspaper
        lf_ppg=pg_results[4]  # graphic paper
        lf_ppp=pp_results[4]  # packing paper
        lf_pph=pg_results[4]  # household paper
        
        lf_pap=lf_ppn+lf_ppg+lf_ppp+lf_pph # paper

        lf_results=ldf.ldf_CFlux(total_yr,lf_bud,lf_exu,lf_hma,lf_pap,
                                 ldf_bdp1,ldf_bdp2,ldf_eup1,ldf_eup2,
                                 ldf_hap1,ldf_hap2,ldf_pap1,ldf_pap2,)

        cs_results=[]

        for i in range(total_yr):
            temp=[]
            temp.append(WP_data['Year'].at[i])

            # Charcoal,building,exterior use,home application, paper,landfill
            tpap=(round(pn_results[1][i])+round(pg_results[1][i])
                  +round(pp_results[1][i])+round(ph_results[1][i]))
            
            temp.append(round(cc_results[1][i]))  
            temp.append(round(bd_results[1][i]))
            temp.append(round(eu_results[1][i]))
            temp.append(round(ha_results[1][i]))
            temp.append(tpap)
            temp.append(round(lf_results[1][i]))
            
            cs_results.append(temp)
            
        header=['Year','Charcoal','Building','Exterior_use',
                'Home_application','Paper','Landfill']
        df=pd.DataFrame(data=cs_results)
        df.to_csv(directory+chr(92)+output_name,index=False,header=header)

        # notice
        messagebox.showinfo("Notice","Estimation Successful!")

def main():
    MainForm()
if __name__=="__main__":
    main()