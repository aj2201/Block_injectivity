# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 19:08:39 2015

@author: Aygul.Ibatullina
"""
import numpy as np
import pandas as pd
import BlockInjIndex
import PVTprops as pvt

class ProdInjRatioCalc(BlockInjIndex.BlockInjIndex):
    def __init__(self):
        BlockInjIndex.BlockInjIndex.__init__(self)
        
    def prod_skin_calc(self):
        table = self.pi_table.T.copy()
    #TODO: change input data from actual to potential   
        alpha_table = self.kh_table * pvt.PVTprops.kro_prime / pvt.PVTprops.mu_o / pvt.PVTprops.C
        alpha_table.columns=['alpha']
        for b in list(set(list(table.index)) - set(alpha_table.index)):
            alpha_table['alpha'][b] = 0#np.nan
        # change order of alpha table to correct multiplying
        alpha_df = pd.DataFrame([alpha_table['alpha'][well] for well in list(table.index)], list(table.index))
        beta_coef = -(pvt.PVTprops.p_avg_D_well - np.log(2))
        self.prod_skin_table = pd.DataFrame(table.values*alpha_df.values, index=table.index, columns=table.columns) + beta_coef
        #self.prod_skin_table.columns = "ProdSkin"
        self.prod_skin_table = self.prod_skin_table.T
        
    
    def block_prod_skin_calc(self, blocks_list_for_calc=None):
        self.prod_skin_calc()
        if blocks_list_for_calc==None:
            blocks_list_for_calc = self.blocks_list
        self.block_prod_skin_table = pd.DataFrame()
        for block in blocks_list_for_calc:
            producers = list ( set (self.blocks_dict[block]) - set (self.cells_list)  & set(self.Qliq_table.T.index) )
            skins = self.prod_skin_table[producers]
            liq_rates = self.Qliq_table[producers]
            wafs = self.WAF_table_blocks["WAF"][block][producers]
            wafed_liqs = liq_rates * wafs
            self.block_prod_skin_table[block] = \
                  pd.DataFrame(skins.values*wafed_liqs.values, \
                  index=wafed_liqs.index, columns=wafed_liqs.columns).T.sum()  \
                  / wafed_liqs.T.sum()
        self.block_prod_skin_table.index = self.block_prod_skin_table.index.droplevel()
        
    def pi_ratio_calc(self):
        #self.pi_ratio_table = pd.DataFrame()
        
        return                

if __name__=="__main__":
    t = ProdInjRatioCalc()
    t.load_data()
    t.block_inj_skin_calc()
    t.block_prod_skin_calc()
    SVA_blocks = filter(lambda t: t[:2]=="SV",t.block_inj_skin_table.columns)
    WS_blocks = filter(lambda t: t[:2]=="WS", t.block_inj_skin_table.columns)
    US_blocks = filter(lambda t: t[:2]=="US", t.block_inj_skin_table.columns)
    t.plot_list(["SVA-5"])