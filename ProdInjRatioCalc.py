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
    
    def __init__(self,\
                NinetyDaysPresInputFileStr=".\input\\NinetyDaysPresInputFile.txt", \
                InjOfmFileStr=".\input\\InjOfmFile.txt",\
                BlockMappingFileInput='.\input\\blocks_mapping.csv',\
                CellsMappingFileInput = '.\input\\cells_mapping.csv'):
        """
        init as init of parrent class BlockInjIndex
        """
        BlockInjIndex.BlockInjIndex.__init__(self, NinetyDaysPresInputFileStr, InjOfmFileStr, BlockMappingFileInput,CellsMappingFileInput )
        
    def prod_skin_calc(self):
        """
        calculation of skin of producers
        """
        table = 1/self.pi_table.T.copy() #corrected 6/15/2017 Aygul
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
        self.prod_skin_table.index = self.prod_skin_table.index.droplevel()
    
    def block_prod_skin_calc(self, blocks_list_for_calc=None):
        """
        calculation of block skin as weighted average of producers skin 
        """
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
        
        
    def block_skins_calc_kh_av(self, blocks_list_for_calc=None):
      if blocks_list_for_calc==None:
         blocks_list_for_calc = self.blocks_list
      
      self.block_inj_skin_table_kh_av = pd.DataFrame()
      self.block_prod_skin_table_kh_av = pd.DataFrame()
      for block in blocks_list_for_calc:
         kh = self.kh_table_blocks[block]
         prods = list((set(self.blocks_dict[block]) - set(self.injectors))&set(self.pi_table.columns))
         injectors = list(set(self.blocks_dict[block]) & set(self.injectors))
         if len(injectors)==0 or len(prods)==0:
            self.block_prod_skin_table_kh_av[block] = np.nan
            self.block_inj_skin_table_kh_av[block] = np.nan
         else:
            #Pres
            some_list = []
            for i in prods:
               if str(type(self.pres_table.get(i))) != "<type 'NoneType'>":
                  some_list.append( self.pres_table[i])
            nPres = pd.DataFrame(some_list)
            Pres = nPres.mean(skipna=True, axis=0)#["Pres"]
            #Pres = Pres [:-1] #since in 90dp one more month 
            #inj skin
            beta_coef = -(pvt.PVTprops.p_avg_D_pat - np.log(2))
            alpha = kh * pvt.PVTprops.krw_prime / pvt.PVTprops.mu_w / pvt.PVTprops.C
            table = (self.bhp_table[injectors].T['avg_BhpInjTopPerfFaily']-Pres[:-1]) / self.inj_table[injectors].T['InjRate']
            block_inj_skins = pd.DataFrame(table.values*alpha, index=table.index, columns=table.columns) + beta_coef
            #prod_skin
            beta_coef = -(pvt.PVTprops.p_avg_D_well - np.log(2))
            Prod_skins = ((1/self.pi_table[prods].T.copy())*alpha+beta_coef).T
            Prod_skins.index = Prod_skins.index.droplevel()
            #block Inj skin average
            liq_rates = self.inj_table[injectors]
            wafs = self.WAF_table_blocks["WAF"][block][injectors]
            wafed_liqs = liq_rates * wafs
            self.block_inj_skin_table_kh_av[block] = \
               pd.DataFrame(block_inj_skins.T.values*wafed_liqs.values, \
                  index =block_inj_skins.T.index.droplevel(), \
                     columns = block_inj_skins.T.columns ).T.sum() /wafed_liqs.T.sum().values
            #was before            (block_inj_skins.T*wafed_liqs).T.sum() / wafed_liqs.T.sum()                 
            self.block_inj_skin_table_kh_av[self.block_inj_skin_table_kh_av>1000]=np.nan
            self.block_inj_skin_table_kh_av.sort_index
            #self.block_inj_skin_table_kh_av.index = self.block_inj_skin_table_kh_av.index.droplevel()
            #block Prod skin average
            skins = Prod_skins #self.prod_skin_table[prods]
            deltaP = Pres - pvt.PVTprops.p_wf_P
            #potential liq rates
            liq_rates = pd.DataFrame((self.pi_table[prods].T.values * deltaP.values).T, \
                           index = self.pi_table[prods].index.droplevel(), \
                           columns=self.pi_table[prods].columns)
            #self.Qliq_table[prods   ]
            wafs = self.WAF_table_blocks["WAF"][block][prods]
            wafed_liqs = liq_rates * wafs
            self.block_prod_skin_table_kh_av[block] = \
                pd.DataFrame(skins.values*wafed_liqs.values,index=wafed_liqs.index, columns=wafed_liqs.columns).T.sum()/ wafed_liqs.T.sum() 
    
     
        
    def pi_ratio_calc(self, blocks_list_for_calc=None):
        """
        calculation of pseudo prodcutivivty injectivity ratio for block
        """
        #self.pi_ratio_table = pd.DataFrame()
        self.block_inj_skin_calc(blocks_list_for_calc)
        self.block_prod_skin_calc(blocks_list_for_calc)
        self.block_skins_calc_kh_av(blocks_list_for_calc)
        self.prod_inj_ratio_table = pd.DataFrame()
        if blocks_list_for_calc==None:
                blocks_list_for_calc = self.blocks_list
        for block in blocks_list_for_calc:
            i_skin = self.block_inj_skin_table_kh_av[block]
            p_skin = self.block_prod_skin_table_kh_av[block]
            k = self.prod_inj_ratio_nominal[block]
            self.prod_inj_ratio_table[block] = k*(pvt.PVTprops.p_avg_D_pat + i_skin)/(pvt.PVTprops.p_avg_D_pat + p_skin)
        return                

if __name__=="__main__":
    """    NinetyDaysPresInputFileStr=".\input\\NinetyDaysPresInputFile.txt", \
    InjOfmFileStr=".\input\\InjOfmFile.txt", BlockMappingFileInput='.\input\\blocks_mapping.csv',\
    CellsMappingFileInput = '.\input\\cells_mapping.csv')"""
    t = ProdInjRatioCalc(".\\feb2017\\NinetyDaysPresInputFile2017.txt", ".\\feb2017\\InjOfmFile2017.txt", ".\\feb2017\\blocks_WS.csv", ".\\feb2017\\cells_WS.csv")
    t.InterpFile = ".\\feb2017\\06 Petrophysical Evaluation results in RGTI form_.csv"
    t.load_data()
    
    