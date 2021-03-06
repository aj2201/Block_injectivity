#TODO: collect data friom sql db instead of files 

import numpy as np
import pandas as pd
import PVTprops as pvt
import seaborn


class BlockInjIndex:
    """
    block injectivity index calculating class
    Inputs:
     From OFM:
        pres_table - reservoir pressure estimates pres_table[well][date*]
        bhp_table -BHPs of injectors
        inj_table - injection rates [well][date*]   
        pi_table 
        Qliq_table 
    From RGTI:
        kh_table - perforated kh for each well
    From wells/blocks/cells mapping files
        WAF_table_blocks 
        koeff_for_cells 
        blocks_dict 
        cells_dict  
        blocks_list 
        cells_list 
        
    As output:
        self.inj_index - skins of injectors
        block_inj_skin_table - skins of blocks
        
    Main funtions:
        load_data - load data from initialaised input files
        self.block_inj_skin_calc - calculating skins of blocks
        
    """

    __author__ = "Aygul.Ibatullina"
    __email__  = "Aygul.Ibatullina@salympetroleum.ru"
    __status__ = "Development"
    __version__ = "1"
    __copyright__ = "Salym Petroleum"

    
    def __init__(self, \
                NinetyDaysPresInputFileStr=".\input\\NinetyDaysPresInputFile.txt", \
                InjOfmFileStr=".\input\\InjOfmFile.txt",\
                BlockMappingFileInput='.\input\\blocks_mapping.csv',\
                CellsMappingFileInput = '.\input\\cells_mapping.csv'):
        """
        class initialization
        args is names of input files 
        """
        self.NinetyInputFile = NinetyDaysPresInputFileStr
        self.InjOfmFile = InjOfmFileStr
        self.InterpFile =  '.\input\\06 Petrophysical Evaluation results in RGTI form.csv' #[".\input\\InterpretationSVA.csv", ".\input\\InterpretationUS.csv",".\input\\InterpretationWS.csv"]
        self.BlockMappingFile = BlockMappingFileInput
        self.CellMappingFile = CellsMappingFileInput
                
        #self.wells = {}
        # self.start_date = "01/09/2006"
        # setting of general tables
        # tables column number equal to months from start_date
        # -1  mean that value no changed during data loading
        self.pres_table = pd.DataFrame()
        self.inj_table = pd.DataFrame()    
        self.bhp_table = pd.DataFrame()  
        self.kh_table = pd.DataFrame()
        self.WAF_table_blocks = pd.DataFrame() 
        self.koeff_for_cells = pd.DataFrame()
        self.block_inj_skin_table = pd.DataFrame()
        self.pi_table = pd.DataFrame()
        self.Qliq_table = pd.DataFrame()
        self.blocks_dict = {}
        self.cells_dict  = {}
        self.blocks_list = []
        self.cells_list = []
        #self.blocks_list_for_calc = []
        
    def inj_rate_filtr(self, x):
        if x > 10:
            return x
        else: return np.nan
        
    def inj_bhp_filtr(self, x):
        if x > 120:
            return x
        else: return np.nan            
        
    def __load_inj_rates_PT(self):  #ToDo: use pivot table!
        """
        loading inj rates and bhp from txt file (ofm report):
            @name(), Date, MonthlyWaterInj.VolumeTot, MonthlyWaterInj.Days, avg_BhpInjTopPerfFaily
        """
        df = pd.read_table(self.InjOfmFile, ",")
        df.columns = map(lambda x: x.replace(" ", ""), df.columns)
        df['Date'] = pd.to_datetime(df['Date'])
        df["avg_BhpInjTopPerfFaily"] = map(self.inj_bhp_filtr, df["avg_BhpInjTopPerfFaily"] )      
        df["InjRate"] = df["MonthlyWaterInj.VolumeTot"] / df["MonthlyWaterInj.Days"] 
        df["InjRate"] = map(self.inj_rate_filtr, df["InjRate"])
        #df["Date"] = self.year_month(df["Date"]) #to avoid porblems with days (last vs first)
        #self.bhp_table = pd.pivot_table(df, values=["avg_BhpInjTopPerfFaily"], rows = ["Date"], cols = ["@name()"])        
        if str(pd.__version__) == '0.6.1':
            self.inj_table = pd.pivot_table(df, values=["InjRate"], cols=["Date"], rows=["@name()"]).T
            self.bhp_table = pd.pivot_table(df, values=["avg_BhpInjTopPerfFaily"], cols=["Date"], rows=["@name()"]).T
        else:
            self.inj_table = pd.pivot_table(df, values=["InjRate"], columns=["Date"], index=["@name()"]).T
            self.bhp_table = pd.pivot_table(df, values=["avg_BhpInjTopPerfFaily"], columns=["Date"], index=["@name()"]).T
            
        self.injectors = list(self.inj_table.columns)
                    
    def __load_90dp_PT(self):
        """
        loading reservoir pressures from txt file (ofm report):
        # @name(), Date,  Ninetydaysplan.Pres, Ninetydaysplan.Pi, Ninetydaysplan.Qgross 
        """
        df = pd.read_table(self.NinetyInputFile, ",")
        df.columns = map(lambda x: x.replace(" ", ""), df.columns)
        df['Date'] = pd.to_datetime(df['Date'])
        df["Pres"] = df["Ninetydaysplan.Pres"]
        df["Pi"] = df["Ninetydaysplan.Pi"] 
        df["Qliq"] = df["Ninetydaysplan.Qgross"]
        #df["Date"] = self.year_month(df["Date"]) #str(dpars.parse(df["Date"]).year()) + str(dpars.parse(df["Date"]).month())
        self.pres_table = (pd.pivot_table(df, values=["Pres"], columns=["Date"], index=["@name()"])).T
        self.pi_table = (pd.pivot_table(df, values=["Pi"], columns=["Date"], index=["@name()"])).T
        self.Qliq_table = (pd.pivot_table(df, values=["Qliq"], columns=["Date"], index=["@name()"])).T
        self.producers = list(self.Qliq_table.columns)
                       
    def __load_kh(self):
        """
        loading petrophisical data
        Data file header is(Mayak RGTI):
        UWI;UWBI;Well Name;Wellbore Name;Lithostratigraphic Unit;Sublayer Top MD;Sublayer Bottom Md ;
        Sublayer Height MD;Sublayer Top TVD SS;Sub Layer Top TVD;Sublayer Bottom TVD SS;Sub Layer Bottom TVD;
        Sublayer Height TVD;Rt;Porosity;Brine Permeability;Water Permeability;Oil Permeability;
        Oil Saturation;Saturation;If exist perforation;;
        """
        filename = self.InterpFile  # for each filed (sva, ws, us)
        if filename[-5:]==".xlsx": df = pd.read_excel(filename)
        else: df = pd.read_table(filename, ";")#,error_bad_lines=False)
        df['Perforation'] = df['If exist perforation'] =='perforated'
        df['kh'] = df['Perforation']*df['Brine Permeability']*df['Sublayer Height TVD']  # add a column with perforated kh of  interval
        self.kh_table = pd.pivot_table(df, values=['kh'], index=['Well Name'], aggfunc=np.sum)
        
    def __blocks_mapping(self, block_name = None):
        """
        loading blocks mapping
        Cell     Well       WAF, and additionally block column
        """
        #reading the file 
        input_table = pd.read_table(self.BlockMappingFile, ";")                                       
         #making new column with block name
        input_table["block"] = map(lambda s: s[:s.find('-', 4)], input_table["Cell"])                
        # # wells = list(set(input_table["Well"].values))
        # # wells = map(str, wells[0:])  #corrected 6/15/2017
        # # df = pd.DataFrame()
        # # df["Well"] = wells
        # # df ["WAF"] = 1
        # # df ["block"] = map(lambda s: s[:s.find('-')], df["Well"])
        # # df["Cell"] = df ["block"] 
        # # input_table = input_table.append(df)
        # creating pivot table to extract blocks with its wells, 
        #this table later could be used to estract WAFs       
        self.WAF_table_blocks = pd.pivot_table(input_table, values=['WAF'], aggfunc=np.max, index=['block', 'Well'])                                                                                             
        cells_WAFs = self.koeff_for_cells.copy()
        cells_WAFs.columns = self.WAF_table_blocks.columns
        cells_WAFs.index.names = self.WAF_table_blocks.index.names
        self.WAF_table_blocks = self.WAF_table_blocks.append(cells_WAFs)
        self.blocks_list = list(set(input_table["block"])) + self.cells_list
        # dictionary block name is key, and for each keycorresponds list of its wells
        self.blocks_dict = {a : list(set(input_table[input_table["block"]==a]["Well"])) for a in  self.blocks_list}                        
        self.blocks_dict.update(self.cells_dict)
        #adding fields as blocks
        #TODO: aweful method! shoul be changed
#        self.blocks_dict["US"] = filter(lambda x: x[:2]=="US",  self.cells_list )
#        self.blocks_dict["SVA"] = filter(lambda x: x[:2]=="SV",  self.cells_list )
#        self.blocks_dict["WS"] = filter(lambda x: x[:2]=="WS",  self.cells_list )
#        self.blocks_list.append("US")
#        self.blocks_list.append("WS")
#        self.blocks_list.append("SVA")
        self.blocks_list.sort()    
    
    def __cells_mapping(self):
        """
        loading cells mapping
        :Injector;Koeff;Producer
        """
        df = pd.read_table(self.CellMappingFile, ";")
        self.cells_list = list(set(df["Injector"])) #list(pd.pivot_table(df, rows=["Injector"], values=["Koeff"]).axes[0])
        #self.WAF_table = pd.pivot_table(df, rows=["Injector", "Producer"], values=["Koeff"])
        self.cells_dict_prod = { a: list(set(df[df["Injector"]==a]["Producer"]) & set(self.producers)) for a in self.cells_list}
        self.cells_dict = { a: list(df[df["Injector"]==a]["Producer"]) for a in self.cells_list}        
        self.koeff_for_cells = pd.pivot_table(df, values=["Koeff"], index=["Injector", "Producer"])
        

    def __nominal_prod_inj_ratio_calc(self):
        """
        nominal p/i ratio 
        is ratio of producers count to injectors count
        """
        wafs = self.WAF_table_blocks.copy()
        wafs.reset_index(inplace=True)
        wafs["isInj"] = [ a in set(self.injectors) for a in wafs["Well"].values]
        wafs["injectors"] = wafs["WAF"]* (1 - wafs["isInj"])
        wafs["producers"] = wafs["WAF"]* wafs["isInj"]
        e = wafs.groupby("block").sum()
        e["P/I"] = e["producers"]/e["injectors"]
        self.prod_inj_ratio_nominal = e["P/I"]

    def __kh_av_for_cells(self):
        """
        since for calculating of skins for each well 
        pattern kh average need to be used 
        table with averages will be calculated
        """
        df = self.WAF_table_blocks.copy()
        df["well"] = df.index.droplevel(0)
        df["block"] = df.index.droplevel(1)
        df["kh"] = self.kh_table["kh"][df["well"]].values
        df["khWAF"] = df["kh"]*df["WAF"]
        u = df.groupby(level=0).sum()
        u["kh_av"] = u['khWAF']/u['WAF']
        self.kh_table_blocks = u["kh_av"]
        
    def load_data(self):
        """
        loading input data
        """
        self.__load_inj_rates_PT()
        self.__load_90dp_PT()
        self.__load_kh()
        self.__cells_mapping()
        self.__blocks_mapping()        
        self.__nominal_prod_inj_ratio_calc()
        self.__kh_av_for_cells()
    
    def __injectivity_skin_calc(self):
        """
        calculating injectors skin (from steady state flow eq for single well)
        """
        #self.load_data()
        #calculating injectors pressure as average of neighbor producers 90dp pressure
        inj_Pres_table = pd.DataFrame()
        cells_Pres = pd.DataFrame()
                
        #TODO: Pres as PI weighted average
        #calcualting avrage Pres for cells
        for cell in self.cells_list:  #cell contain injector and surrounding producers
           neighbors = self.cells_dict_prod.get(cell)  # getting neighbors list
           #neighbors = neighbors[neighbors!=injector]
           neighbors_Pres = pd.DataFrame() #[self.pres_table[i] for i in neighbors and ]) #getting pressures of neighbors
           some_list = []
           for i in neighbors:
               if str(type(self.pres_table.get(i))) != "<type 'NoneType'>":
                   some_list.append( self.pres_table[i])
           neighbors_Pres = pd.DataFrame(some_list)
           cells_Pres[cell] = neighbors_Pres.mean(skipna=True, axis=0)  # averaging of non NaN values, i hope that its like to numpy.nanmean (v1.11)
                      
        #obtainging injector Pres as cell Pres
        inv_cells_dict = {}
        for cell, wells in self.cells_dict.iteritems():
            for well in set(wells)&set(self.injectors):
                inv_cells_dict.update({well:cell}) #here potential bug! if injector signed for two or more cells only one will be accounted for Pres
        self.injectors = list(set(self.injectors) & set(list(inv_cells_dict.keys())))        
        inj_Pres_table = pd.DataFrame({injector: cells_Pres[inv_cells_dict[injector]] for injector in self.injectors})
        
        # beta_coef calculating =  -(p_avg_D_pat-LN(2)) where p_avg_D_pat = LN(d/rw)-0.443 = 8.30
        beta_coef = -(pvt.PVTprops.p_avg_D_pat - np.log(2))
        #alpha for each well =  preforated kh*krw/mu_w/C
        alpha_table = self.kh_table * pvt.PVTprops.krw_prime / pvt.PVTprops.mu_w / pvt.PVTprops.C
        alpha_table.columns=['alpha']
        # zero values assign as NAN to avoid misstakes in averaging
        # table = (BHP - Pres) / InjRate
        table = (self.bhp_table.T['avg_BhpInjTopPerfFaily']-inj_Pres_table.T['Pres'] ) / self.inj_table.T['InjRate']
        
        #adding to alpha table NAN values for wells which not presented in RGTI tables 
        #                               (index of alpha_table equal to index of kh_table)
        for b in list(set(list(table.index)) - set(alpha_table.index)):
            alpha_table['alpha'][b] = 0#np.nan
        # change order of alpha table to correct multiplying
        alpha_df = pd.DataFrame([alpha_table['alpha'][well] for well in list(table.index)], list(table.index))
        # inj_index = table * alpha + beta
        self.inj_index = pd.DataFrame(table.values*alpha_df.values, index=table.index, columns=table.columns) + beta_coef
        # deleting from blocks_dict all producers, since for blocks injectivity calculating only injectors requried
    
    def block_inj_skin_calc(self, blocks_list_for_calc=None):
        """
        calcualting block injectivity skin
        as rate-weighted average of injectors skin
        """
        self.__injectivity_skin_calc()
        blocks_inj_dict = {a: list(set(self.blocks_dict[a]) & set(self.injectors)) for a in self.blocks_list}
        # eqclude cells from blocks list 
        if blocks_list_for_calc==None:
            blocks_list_for_calc = self.blocks_list
        #sorting list for beauty
        blocks_list_for_calc.sort()
        for block in blocks_list_for_calc:
            if len(blocks_inj_dict[block]) > 0:
                injectors = blocks_inj_dict[block]
                liq_rates = self.inj_table[injectors]
                wafs = self.WAF_table_blocks["WAF"][block][injectors]
                wafed_liqs = liq_rates * wafs
                block_inj_skins = self.inj_index.T[injectors]
                self.block_inj_skin_table[block] = (block_inj_skins*wafed_liqs).T.sum() / wafed_liqs.T.sum()
            else: 
                self.block_inj_skin_table[block] =  np.nan
        self.block_inj_skin_table[self.block_inj_skin_table>1000]=np.nan
        self.block_inj_skin_table.sort_index
        self.block_inj_skin_table.index = self.block_inj_skin_table.index.droplevel()
        #the results of calc is self.block_inj_skin_table
    
    def plot_list(self, blocks_list=[]):
        if len(blocks_list)>0:
            df = self.block_inj_skin_table[blocks_list]
        else: 
            df = self.block_inj_skin_table
        plots_number = float(len(df.columns))
        v = int(np.ceil(plots_number ** 0.5))
        h = int(np.ceil(plots_number / v ))
        if plots_number < 4:
            v = int(np.min([3., plots_number]))
            h = 1
        df.plot(subplots=True, layout=(v,h))
    
    def plot_block(self, block_name):
        df = pd.DataFrame(self.block_inj_skin_table[block_name])
        df = df[np.isnan(df)==False]
        df.plot()  

if __name__ == "__main__":
    t = BlockInjIndex(NinetyDaysPresInputFileStr="./FullInput/90dpfrom2011.txt", InjOfmFileStr ="./FullInput/injOfmfrom2011.txt" )
    t.load_data()
    t.block_inj_skin_calc()
    
    SVA_blocks = filter(lambda t: t[:2]=="SV",t.block_inj_skin_table.columns)
    WS_blocks = filter(lambda t: t[:2]=="WS", t.block_inj_skin_table.columns)
    US_blocks = filter(lambda t: t[:2]=="US", t.block_inj_skin_table.columns)
    #t.plot_list(["SVA"])
    