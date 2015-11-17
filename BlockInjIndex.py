#TODO: collect data friom sql db instead of files 

import numpy as np
import pandas as pd
import PVTprops as pvt
import seaborn


class BlockInjIndex:
    """
    block injectivity index calculating class
    Atributes:
        pres_table - reservoir pressure estimates pres_table[well][date*]
        bhp_table -BHPs of injectors
        inj_table - injection rates [well][date*]
        kh_table - perforated kh for each well
                
        
    """

    __author__ = "Aygul.Ibatullina"
    __email__  = "Aygul.Ibatullina@salympetroleum.ru"
    __status__ = "Development"
    __version__ = "1"
    __copyright__ = "Salym Petroleum"

    
    def __init__(self, NinetyDaysPresInputFileStr=".\input\\NinetyDaysPresInputFile.txt", \
    InjOfmFileStr=".\input\\InjOfmFile.txt", BlockMappingFileInput='.\input\\blocks_mapping.csv',\
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
        self.block_inj_index = pd.DataFrame()
        self.pi_table = pd.DataFrame()
        self.Qliq_table = pd.DataFrame()
        self.blocks_dict = {}
        self.cells_dict  = {}
        self.blocks_list = []
        self.cells_list = []
        #self.blocks_list_for_calc = []
        
    def load_inj_rates_PT(self):  #ToDo: use pivot table!
        """
        loading inj rates and bhp from txt file (ofm report):
            @name(), Date, MonthlyWaterInj.VolumeTot, MonthlyWaterInj.Days, avg_BhpInjTopPerfFaily
        """
        df = pd.read_table(self.InjOfmFile, ",")
        df['Date'] = pd.to_datetime(df['Date'])
        df["InjRate"] = df["MonthlyWaterInj.VolumeTot"] / df["MonthlyWaterInj.Days"] 
        #df["Date"] = self.year_month(df["Date"]) #to avoid porblems with days (last vs first)
        #self.bhp_table = pd.pivot_table(df, values=["avg_BhpInjTopPerfFaily"], rows = ["Date"], cols = ["@name()"])        
        if str(pd.__version__) == '0.6.1':
            self.inj_table = pd.pivot_table(df, values=["InjRate"], cols=["Date"], rows=["@name()"]).T
            self.bhp_table = pd.pivot_table(df, values=["avg_BhpInjTopPerfFaily"], cols=["Date"], rows=["@name()"]).T
        else:
            self.inj_table = pd.pivot_table(df, values=["InjRate"], columns=["Date"], index=["@name()"]).T
            self.bhp_table = pd.pivot_table(df, values=["avg_BhpInjTopPerfFaily"], columns=["Date"], index=["@name()"]).T
            
                    
    def load_90dp_PT(self):
        """
        loading reservoir pressures from txt file (ofm report):
        # @name(), Date,  Ninetydaysplan.Pres, Ninetydaysplan.Pi, Ninetydaysplan.Qgross 
        """
        df = pd.read_table(self.NinetyInputFile, ",")
        df['Date'] = pd.to_datetime(df['Date'])
        df["Pres"] = df["Ninetydaysplan.Pres"]
        df["Pi"] = df["Ninetydaysplan.Pi"] 
        df["Qliq"] = df["Ninetydaysplan.Qgross"]
        #df["Date"] = self.year_month(df["Date"]) #str(dpars.parse(df["Date"]).year()) + str(dpars.parse(df["Date"]).month())
        self.pres_table = (pd.pivot_table(df, values=["Pres"], columns=["Date"], index=["@name()"])).T
        self.pi_table = (pd.pivot_table(df, values=["Pi"], columns=["Date"], index=["@name()"])).T
        self.Qliq_table = (pd.pivot_table(df, values=["Qliq"], columns=["Date"], index=["@name()"])).T
                       
    def load_kh(self):
        """
        loading petrophisical data
        Data file header is(Mayak RGTI):
        UWI;UWBI;Well Name;Wellbore Name;Lithostratigraphic Unit;Sublayer Top MD;Sublayer Bottom Md ;
        Sublayer Height MD;Sublayer Top TVD SS;Sub Layer Top TVD;Sublayer Bottom TVD SS;Sub Layer Bottom TVD;
        Sublayer Height TVD;Rt;Porosity;Brine Permeability;Water Permeability;Oil Permeability;
        Oil Saturation;Saturation;If exist perforation;;
        """
        filename = self.InterpFile  # for each filed (sva, ws, us)
        df = pd.read_table(filename, ";")#,error_bad_lines=False)
        df['Perforation'] = df['If exist perforation'] =='perforated'
        df['kh'] = df['Perforation']*df['Brine Permeability']*df['Sublayer Height TVD']  # add a column with perforated kh of  interval
        self.kh_table = pd.pivot_table(df, values=['kh'], index=['Well Name'], aggfunc=np.sum)
        
    def blocks_mapping(self, block_name = None):
        """
        loading blocks mapping
        Cell     Well       WAF, and additionally block column
        """
        #reading the file 
        input_table = pd.read_table(self.BlockMappingFile, ";")                                       
         #making new column with block name
        input_table["block"] = map(lambda s: s[:s.find('-', 4)], input_table["Cell"])                
        wells = list(set(input_table["Well"].values))
        wells = map(str, wells[1:])
        df = pd.DataFrame()
        df["Well"] = wells
        df ["WAF"] = 1
        df ["block"] = map(lambda s: s[:s.find('-')], df["Well"])
        df["Cell"] = df ["block"] 
        input_table = input_table.append(df)
        # creating pivot table to extract blocks with its wells, 
        #this table later could be used to estract WAFs       
        self.WAF_table_blocks = pd.pivot_table(input_table, values=['WAF'], aggfunc=np.max, index=['block', 'Well'])                                                                                             
        self.blocks_list = list(set(input_table["block"]))
        # dictionary block name is key, and for each keycorresponds list of its wells
        self.blocks_dict = {a : list(set(input_table[input_table["block"]==a]["Well"])) for a in  self.blocks_list}                        
        #adding fields as bocks
        #TODO: aweful method! shoul be changed
#        self.blocks_dict["US"] = filter(lambda x: x[:2]=="US",  self.cells_list )
#        self.blocks_dict["SVA"] = filter(lambda x: x[:2]=="SV",  self.cells_list )
#        self.blocks_dict["WS"] = filter(lambda x: x[:2]=="WS",  self.cells_list )
#        self.blocks_list.append("US")
#        self.blocks_list.append("WS")
#        self.blocks_list.append("SVA")
        #TODO: adding WAFs for fields
        self.blocks_list.sort()    
    
    def cells_mapping(self):
        """
        loading cells mapping
        :Injector;Koeff;Producer
        """
        df = pd.read_table(self.CellMappingFile, ";")
        self.cells_list = list(set(df["Injector"])) #list(pd.pivot_table(df, rows=["Injector"], values=["Koeff"]).axes[0])
        #self.WAF_table = pd.pivot_table(df, rows=["Injector", "Producer"], values=["Koeff"])
        self.cells_dict = { a: list(set(df[df["Injector"]==a]["Producer"]) - set(self.cells_list)) for a in self.cells_list}
        self.koeff_for_cells = pd.pivot_table(df, values=["Koeff"], index=["Injector", "Producer"])
        

    def nominal_prod_inj_ratio_calc(self):
        """
        nominal p/i ratio 
        is ratio of producers count to injectors count
        """
        wafs = self.WAF_table_blocks.copy()
        wafs.reset_index(inplace=True)
        wafs["isInj"] = [ a in set(self.cells_list) for a in wafs["Well"].values]
        wafs["injectors"] = wafs["WAF"]* (1 - wafs["isInjector"])
        wafs["producers"] = wafs["WAF"]* wafs["isInjector"]
        e = wafs.groupby("block").sum()
        e["P/I"] = e["producers"]/e["injectors"]
        self.prod_inj_ratio = e["P/I"]

    
    def calc_pattern_pres(self):
        """
        for injectors (which are in cells_list)
        pres = mean of neighboring prodcuers 
        """
        
    
    def load_data(self):
        """
        loading input data
        """
        self.load_inj_rates_PT()
        self.load_90dp_PT()
        self.load_kh()
        self.cells_mapping()
        self.blocks_mapping()        
    
    def injectivity_skin_calc(self):
        """
        calculating injectors skin (from steady state flow eq for single well)
        """
        #self.load_data()
        #calculating injectors pressure as average of neighbor producers 90dp pressure
        inj_Pres_table = pd.DataFrame()
        for injector in self.cells_list:  #cell contain injector and surrounding producers
           neighbors = self.cells_dict.get(injector)  # getting neighbors list
           #neighbors = neighbors[neighbors!=injector]
           neighbors_Pres = pd.DataFrame() #[self.pres_table[i] for i in neighbors and ]) #getting pressures of neighbors
           some_list = []
           for i in neighbors:
               if str(type(self.pres_table.get(i))) != "<type 'NoneType'>":
                   some_list.append( self.pres_table[i])
           neighbors_Pres = pd.DataFrame(some_list)
           injector_Pres = neighbors_Pres.mean(skipna=True, axis=0)  # averaging of non NaN values, i hope that its like to numpy.nanmean (v1.11)
           inj_Pres_table[injector] = injector_Pres  # pressure of injector calculated as average of neighbor producers 90dp pressure
           
        # beta_coef calculating =  -(p_avg_D_pat-LN(2)) where p_avg_D_pat = LN(d/rw)-0.443 = 8.30
        beta_coef = -(pvt.PVTprops.p_avg_D_pat - np.log(2))
        #alpha for each well =  preforated kh*krw/mu_w/C
        alpha_table = self.kh_table * pvt.PVTprops.krw_prime / pvt.PVTprops.mu_w / pvt.PVTprops.C
        alpha_table.columns=['alpha']
        # zero values assign as NAN to avoid misstakes in averaging
        #alpha_table[alpha_table['alpha']==0] = np.nan
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
        as rate - weughted average of injectors skin
        """
        self.injectivity_skin_calc()
        blocks_inj_dict = {a: list(set(self.blocks_dict[a]) & set(self.cells_list) & set(self.inj_table.T.index)) for a in self.blocks_list}
        # eqclude cells from blocks list 
        if blocks_list_for_calc==None:
            blocks_list_for_calc = list(set(self.blocks_list) - set(self.cells_list))
        #sorting list for beauty
        blocks_list_for_calc.sort()
        for block in blocks_list_for_calc:
            if len(blocks_inj_dict[block]) > 0:
                #TODO: weight average
                #block_injectors_skins = pd.DataFrame([self.inj_index.T[injector] for injector in blocks_inj_dict[block]])
                injectors = blocks_inj_dict[block]
                block_inj_rates = self.inj_table[injectors]
                block_inj_skins = self.inj_index.T[injectors]
                #assumed that there arent injectors with WAF<1
                self.block_inj_index[block] = (block_inj_skins*block_inj_rates).T.sum() / block_inj_rates.T.sum()
            else: 
                #if __debug__: print block, "is empty [injectors didn't found]"
                self.block_inj_index[block] =  np.nan
        #self.block_inj_index[self.block_inj_index>1000]=np.nan
        self.block_inj_index.sort_index
        self.block_inj_index.index = self.block_inj_index.index.droplevel()
        #the results of calc is self.block_inj_index
    
    def plot_list(self, blocks_list):
        #df = pd.DataFrame({a: self.block_inj_index[a] for a in blocks_list })
        if len(blocks_list)>0:
            df = self.block_inj_index[blocks_list]
        else: 
            df = self.block_inj_index
        plots_number = float(len(df.columns))
        v = int(np.ceil(plots_number ** 0.5))
        h = int(np.ceil(plots_number / v ))
        if plots_number < 4:
            v = int(np.min([3., plots_number]))
            h = 1
        df.plot(subplots=True, layout=(v,h))
    
    def plot_block(self, block_name):
        df = pd.DataFrame(self.block_inj_index[block_name])
        df = df[np.isnan(df)==False]
        df.plot()
    
    def save_as_csv(self, file_name="out.csv"):
        self.block_inj_index.T.to_csv(file_name,sep=';')      

if __name__ == "__main__":
    #if __debug__:
    #    print "Debug"
    t = BlockInjIndex()
    t.load_data()
    t.block_inj_skin_calc()
    
    SVA_blocks = filter(lambda t: t[:2]=="SV",t.block_inj_index.columns)
    WS_blocks = filter(lambda t: t[:2]=="WS", t.block_inj_index.columns)
    US_blocks = filter(lambda t: t[:2]=="US", t.block_inj_index.columns)
    t.plot_list(["SVA"])
    