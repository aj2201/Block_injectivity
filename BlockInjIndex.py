#TODO: collect data friom sql db instead of files 

import numpy as np
import pandas as pd
import PVTprops as pvt
import seaborn

MAX_WELLS_COUNT = 964
MAX_MONTHS_COUNT = 240



class BlockInjIndex:
    """
    block injectivity index calculating class
    Atributes:
        pres_table - reservoir pressure estimates pres_table[well][date*]
        bhp_table -BHPs of injectors
        inj_table - injection rates [well][date*]
        kh_table - 
        
        
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
        self.__NinetyInputFile = NinetyDaysPresInputFileStr
        self.__InjOfmFile = InjOfmFileStr
        self.__InterpFile =  '.\input\\06 Petrophysical Evaluation results in RGTI form.csv' #[".\input\\InterpretationSVA.csv", ".\input\\InterpretationUS.csv",".\input\\InterpretationWS.csv"]
        self.__BlockMappingFile = BlockMappingFileInput
        self.__CellMappingFile = CellsMappingFileInput
                
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
        #self.big_blocks = []
        
    def load_inj_rates_PT(self):  #ToDo: use pivot table!
        """
        loading inj rates and bhp from txt file (ofm report):
            @name(), Date, MonthlyWaterInj.VolumeTot, MonthlyWaterInj.Days, avg_BhpInjTopPerfFaily
        """
        df = pd.read_table(self.__InjOfmFile, ",")
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
        df = pd.read_table(self.__NinetyInputFile, ",")
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
        Data file header is
        Field;Well;Layer;Top MD [ m ];Bottom MD [ m ];Thickness MD [ m ];Top TVD [ m ];
        Bottom TVD [ m ];Thickness TVD [ m ];Rt;Porosity [ % ];Liquid permeability [ MilliDarcy ];
        Oil Permeability [ MilliDarcy ];Water Permeability [ MilliDarcy ];So_Log;So_Shf;Fluid;Perforation
        
        Mayak RGTI:
        UWI;UWBI;Well Name;Wellbore Name;Lithostratigraphic Unit;Sublayer Top MD;Sublayer Bottom Md ;
        Sublayer Height MD;Sublayer Top TVD SS;Sub Layer Top TVD;Sublayer Bottom TVD SS;Sub Layer Bottom TVD;
        Sublayer Height TVD;Rt;Porosity;Brine Permeability;Water Permeability;Oil Permeability;
        Oil Saturation;Saturation;If exist perforation;;
        
        """
        
        filename = self.__InterpFile  # for each filed (sva, ws, us)
        df = pd.read_table(filename, ";")#,error_bad_lines=False)
        df['Perforation'] = df['If exist perforation'] =='perforated'
        
        df['kh'] = df['Perforation']*df['Brine Permeability']*df['Sublayer Height TVD']  # add a column with perforated kh of  interval
        self.kh_table = pd.pivot_table(df, values=['kh'], index=['Well Name'], aggfunc=np.sum)
        
           
        
    def blocks_mapping(self, block_name = None):
        """
        loading blocks mapping
        Cell     Well       WAF, and additionally block column
        """
        input_table = pd.read_table(self.__BlockMappingFile, ";")                                       #reading the file 
        #input_table["cell"]
        input_table["block"] = map(lambda s: s[:s.find('-', 4)], input_table["Cell"])                 #making new column with block name
        
        self.WAF_table_blocks = pd.pivot_table(input_table, values=['WAF'], aggfunc=np.max, index=['block', 'Well'])  # creating pivot table to extract blocks with its wells, 
                                                                                           #this table later could be used to estract WAFs       
        self.blocks_list = list(set(input_table["block"]))
        self.blocks_dict = {a : list(set(input_table[input_table["block"]==a]["Well"])) for a in  self.blocks_list}                        # dictionary block name is key, and for each keycorresponds list of its wells
        #adding fields as bocks
        t.blocks_dict["US"] = filter(lambda t: t[:2]=="US",  t.cells_list )
        t.blocks_dict["SVA"] = filter(lambda t: t[:2]=="SV",  t.cells_list )
        t.blocks_dict["WS"] = filter(lambda t: t[:2]=="WS",  t.cells_list )
        t.blocks_list.append("US")
        t.blocks_list.append("WS")
        t.blocks_list.append("SVA")
        
    
    def cells_mapping(self):
        """
        loading cells mapping
        :Injector;Koeff;Producer
        """
        df = pd.read_table(self.__CellMappingFile, ";")
        self.cells_list = list(set(df["Injector"])) #list(pd.pivot_table(df, rows=["Injector"], values=["Koeff"]).axes[0])
        #self.WAF_table = pd.pivot_table(df, rows=["Injector", "Producer"], values=["Koeff"])
        self.cells_dict = { a: list(set(df[df["Injector"]==a]["Producer"]) - set(self.cells_list)) for a in self.cells_list}
        self.koeff_for_cells = pd.pivot_table(df, values=["Koeff"], index=["Injector", "Producer"])
        

        
    def calc_pattern_pres(self):
        """
        for injectors (which are in cells_list)
        pres = mean of neighboring prodcuers 
        """
        
    
    def load_data(self):
        """
        loading data
        """
        if __debug__:
            print "loading data from files:"
            print "\t*", self.__NinetyInputFile
            print "\t*",self.__InjOfmFile
            print "\t*",self.__InterpFile
            print "\t*",self.__BlockMappingFile
            print "\t*",self.__CellMappingFile
        self.load_inj_rates_PT()
        self.load_90dp_PT()
        self.load_kh()
        self.blocks_mapping()
        self.cells_mapping()
        if __debug__: print "data loaded"   
    
    
        
        
    
    def main_calc(self, blocks_list_for_calc=None):
        #self.load_data()
        if __debug__: print "calculating..."
        #calculating injectors pressure as average of neighbor producers 90dp pressure
        inj_Pres_table = pd.DataFrame()
        for injector in self.cells_list:  #cell contain injector and surrounding producers
           neighbors = t.cells_dict.get(injector)  # getting neighbors list
           #neighbors = neighbors[neighbors!=injector]
           neighbors_Pres = pd.DataFrame() #[t.pres_table[i] for i in neighbors and ]) #getting pressures of neighbors
           some_list = []
           for i in neighbors:
               if str(type(t.pres_table.get(i))) != "<type 'NoneType'>":
                   some_list.append( t.pres_table[i])
           neighbors_Pres = pd.DataFrame(some_list)
           injector_Pres = neighbors_Pres.mean(skipna=True, axis=0)  # averaging of non NaN values, i hope that its like to numpy.nanmean (v1.11)
           inj_Pres_table[injector] = injector_Pres  # pressure of injector calculated as average of neighbor producers 90dp pressure
           
        # beta_coef calculating =  -(p_avg_D_pat-LN(2)) where p_avg_D_pat = LN(d/rw)-0.443 = 8.30
        beta_coef = -(pvt.PVTprops.p_avg_D_pat - np.log(2))
        #alpha for each well =  preforated kh*krw/mu_w/C
        alpha_table = t.kh_table * pvt.PVTprops.krw_prime / pvt.PVTprops.mu_w / pvt.PVTprops.C
        alpha_table.columns=['alpha']
        # zero values assign as NAN to avoid misstakes in averaging
        #alpha_table[alpha_table['alpha']==0] = np.nan
        # table = (BHP - Pres) / InjRate
        table = (t.bhp_table.T['avg_BhpInjTopPerfFaily']-inj_Pres_table.T['Pres'] ) / t.inj_table.T['InjRate']
        
        #adding to alpha table NAN values for wells which not presented in RGTI tables 
        #                               (index of alpha_table equal to index of kh_table)
        for b in list(set(list(table.index)) - set(alpha_table.index)):
            alpha_table['alpha'][b] = 0#np.nan
        # change order of alpha table to correct multiplying
        alpha_df = pd.DataFrame([alpha_table['alpha'][well] for well in list(table.index)], list(table.index))
        # inj_index = table * alpha + beta
        self.inj_index = pd.DataFrame(table.values*alpha_df.values, index=table.index, columns=table.columns) + beta_coef
        # deleting from blocks_dict all producers, since for blocks injectivity calculating only injectors requried
        blocks_inj_dict = {a: list(set(t.blocks_dict[a]) & set(t.cells_list)) for a in t.blocks_list}
        # eqclude cells from blocks list 
        big_blocks = list(set(t.blocks_list) - set(t.cells_list))
            
        #sorting list for beauty
        big_blocks.sort()
        for block in big_blocks:
            if len(blocks_inj_dict[block]) > 0:
                self.block_inj_index[block] = pd.DataFrame([self.inj_index.T[injector] for injector in blocks_inj_dict[block]]).median(axis=0, skipna=True)
            else: 
                if __debug__: print block, "is empty [injectors didn't found]"
                self.block_inj_index[block] =  np.nan
        self.block_inj_index[self.block_inj_index>1000]=np.nan
        self.block_inj_index.sort_index
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
        
    def grouped_weighted_avg(self, values, weights, by):
        return (values * weights).groupby(by).sum() / weights.groupby(by).sum()


  
if __name__ == "__main__":
    #if __debug__:
    #    print "Debug"
    t = BlockInjIndex()
    t.load_data()
    t.main_calc()
    SVA_blocks = filter(lambda t: t[:2]=="SV",t.block_inj_index.columns)
    WS_blocks = filter(lambda t: t[:2]=="WS", t.block_inj_index.columns)
    US_blocks = filter(lambda t: t[:2]=="US", t.block_inj_index.columns)
    t.plot_list(WS_blocks)
    #grouped_weighted_avg(values=df.wt, weights=df.value, by=df.index)
