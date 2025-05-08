r"""CableOperations class.

Provides a framework for selecting electrical cables based on various electrical and 
installation parameters. It relies on data stored in an SQLite database and incorporates 
calculations for conductor resistance, derating, and voltage drop to recommend a suitable 
cable that meets the specified requirements. 
"""

import math
import os
import sqlite3
# from importlib import resources 

from numpy import double
import pandas as pd
import numpy as np
from .sqlite_tools import QuaryOutFormat, SqliteTools

class CableOperations():
    
    def __init__(self,db_path:str=None):
        try:
            if db_path is None:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(base_dir, 'elsweedy_cables.db')
                db = SqliteTools(db_path)
            # db = SqliteTools(db_path)
            # if db is None:
            #     raise sqlite3.Error(f"Error connecting to database '{db_path}'")
            # if db_path == None:
            #     db_path = resources.files('electrical_power').joinpath('elsweedy_cables.db')
            #     db = SqliteTools(db_path)
            else:
                db = SqliteTools(db_path)
            db.connect_db()
            # if db.check_table_if_exists('icc') == False:    
            #     raise sqlite3.Error(f"Error could not find Icc table'")
            
            self.icc =db.read_table(table_name= 'icc',out_format=QuaryOutFormat.df) 
            self.installation_method = db.read_table(table_name='installation_method',out_format=QuaryOutFormat.df) 
            self.material_conductor =  db.read_table(table_name='material_conductor',out_format=QuaryOutFormat.df) 
            self.material_isolation = db.read_table(table_name='material_isolation',out_format=QuaryOutFormat.df) 
            self.air_temprature_derating_factors = db.read_table(table_name='air_temprature_derating_factors',out_format=QuaryOutFormat.df) 
            self.ground_temprature_derating_factors = db.read_table(table_name='ground_temprature_derating_factors',out_format=QuaryOutFormat.df) 
            self.burial_depth_derating_factors = db.read_table(table_name='burial_depth_derating_factors',out_format=QuaryOutFormat.df) 
            self.soil_thermal_resistivity_derating_factors = db.read_table(table_name='soil_thermal_resistivity_derating_factors',out_format=QuaryOutFormat.df) 
            self.pvc_rated_temperature_derating_factors = db.read_table(table_name='pvc_rated_temperature_derating_factors',out_format=QuaryOutFormat.df) 
            self.laid_direct_in_ground_derating_factors = db.read_table(table_name='laid_direct_in_ground_derating_factors',out_format=QuaryOutFormat.df) 
            self.grouping_derating_factors = db.read_table(table_name='grouping_derating_factors',out_format=QuaryOutFormat.df) 
            self.voltage_drop = db.read_table(table_name='voltage_drop',out_format=QuaryOutFormat.df)  
            self.size = db.read_table(table_name='size',out_format=QuaryOutFormat.df) 
            self.cu_rho = 1.72 * math.pow(10,-8) # in ohms
            self.al_rho = 2.65 * math.pow(10,-8) # in ohms
            
        except sqlite3.Error as e:
            print(f"Error connecting to database '{db_path}': {e}")  

    def __conductor_resistance__(self,conductor_material='cu',temperature= 20,cable_size=1):
        '''
        Conductor resistance per unit length ohm/m for different temperature values
        
        parameters:
        -----------
            conductor_material : str (default: cu)
                'cu' copper and 'al' for aluminium 
            temperature: float (default: 20)
                ambient temperature  
            cable_size : float (default: 1)
                cable cross sectional area (1/1.5/2.5/4/6/10/16/25/35/50/75/90/120/150/185/240/300) 
        
        Returns:
        --------
            float : conductor resistance in ohms
        '''        
        material_rho = 0
        
        match conductor_material:
            case 'cu':
                material_rho = self.cu_rho
            case 'al':
                material_rho = self.al_rho
            case _:
                pass
        if temperature != 20:
            material_rho = material_rho * (1+0.00393*(temperature-20))
        
        return material_rho / cable_size #( * math.pow(10,-6))
    
    def __air_temprature_derating_factor__(self,ambient_temperature=30,insulationmaterial='pvc'):
        '''
        Air temprature derating factors [Table 3] for Rated Currents at conditions other that specified in D.7
        
        parameters:
        -----------
            ambient_temperature :float (default: 30)
                ambient temperature in degree celisius 
            InsulationMaterial :str (default: pvc)
                sheath insulating material pvc or xlpe 
        
        Returns:
        --------
            float : derating factor for ambient remperature
        '''        
        return self.air_temprature_derating_factors.iloc[(self.air_temprature_derating_factors.temperature-ambient_temperature).abs().idxmin()][insulationmaterial]
    
    def __ground_temprature_derating_factor__(self,ground_temperature=20,insulationmaterial='pvc'):
        '''
        Ground temprature derating factors [Table 4] for Rated Currents at conditions other that specified in D.7
        
        parameters:
        ----------
            ground_temperature : float (default: 20)
                ground temperature in degree celisius 
            InsulationMaterial : str (default: pvc)
                sheath insulating material pvc or xlpe 
        
        Returns:
        --------
            float : derating factor for ground remperature
        '''        
        return self.ground_temprature_derating_factors.iloc[(self.ground_temprature_derating_factors.temperature-ground_temperature).abs().idxmin()][insulationmaterial]
    
    def __burial_depth_derating_factors__(self,
                                        depth=0.5,
                                        installation_method='burried_direct',
                                        cores='single',
                                        cable_size=1):   
        '''
        Burial depth de-rating factors [Table 5] 
        
        parameters:
        ----------
            depth : float (default: 0.5)
                Depth of laying in m 
            installation_method : str (default:burried_direct)
                cable installation method (burried_direct / burried_duct)  
            cores : str (default: single)
                single or multi cores cable (single / multi) 
            cable_size : float (default: 1)
                cable cross sectional area (1/1.5/2.5/4/6/10/16/25/35/50/75/90/120/150/185/240/300) 
        
        Returns:
        --------
            float : derating factor
        '''         
        selected_df = self.burial_depth_derating_factors[(self.burial_depth_derating_factors.installation_method == installation_method) & \
            (self.burial_depth_derating_factors.cores ==  1 if cores =="single" else 3) ]
        
        if cores == 'single':
            selected_df = selected_df[selected_df['size'] == ('less_185' if cable_size <= 15 else 'greater_185')]
        selected_df.reset_index(inplace=True)
        return selected_df.iloc[(selected_df.depth-depth).abs().idxmin()]['factor']
            
    def __Soil_thermal_resistivity_derating_factor__(self,
                                            thermal_resistivity=1, #K.cm/Watt
                                            installation_method='burried_direct'):
        '''
        Soil thermal resistivity[K.m/W] de-rating factors [Table 6] 
        
        parameters:
        -----------
            thermal_resistivity : float (default: 1)
                Ground thermal resistivity in K.cm/Watt 
            installation_method : str (default: 1)
                cable installation method (burried_direct / burried_duct)
        
        Returns:
        --------
            float : derating factor
        '''            
        return self.soil_thermal_resistivity_derating_factors.iloc \
            [(self.soil_thermal_resistivity_derating_factors.soil_thermal_resistivity_Km_to_W-thermal_resistivity).abs().idxmin()][installation_method]

    def __pvc_rated_temperature_derating_factors__(self,temperrature=70, #K.cm/Watt
                                                    installation_method='free_air'):
        '''
        PVC rated temperature de-rating factors [Table 7] 
        
        parameters:
        -----------
            temperature : float (default: 70)
                Type of PVC rated temperature ˚C 
            installation_method : str (default: free_air)
                cable installation method (burried_direct / duct / free_air) 
        
        Returns:
        --------
            float : derating factor
        '''        
        return self.pvc_rated_temperature_derating_factors.iloc \
            [(self.pvc_rated_temperature_derating_factors.temperature-temperrature).abs().idxmin()][installation_method]
            
    def __laid_direct_in_ground_derating_factors__(self,
                                                cores:(str)='single',
                                                circuits_no:(int)=2,
                                                installation_formation:(str)='flat',
                                                spacing:(float)=0):
        '''
        Trefoil or flat formation De-rating factors for three single core cables laid direct in ground [Table 8] and 
        Trefoil formation De-rating factors for multi-core core cables laid direct in ground [Table 9].
        
        parameters:
        -----------
            cores : str (default: single)
                cable cores single or multi core cable 
            circuits_no : int (default: 2)
                number of circuits  
            installation_formation : str (default: flat)
                cable formation flat or trefoil 
            spacing : foat (default: 0 'touching')
                spacing between circuits touching /Spacing = 0.15 m / Spacing = 0.3 m 
        Returns:
        --------
            float : derating factor
        '''        
        
        selected_df = self.laid_direct_in_ground_derating_factors[(self.laid_direct_in_ground_derating_factors.installation_formation == installation_formation) & \
            (self.laid_direct_in_ground_derating_factors.cores == cores) & \
                (self.laid_direct_in_ground_derating_factors.circuits_no == circuits_no)].reset_index()
        
        return selected_df.iloc[(selected_df.spacing-spacing).abs().idxmin()]['factor']
    
    def __grouping_derating_factors__(self,
                                    cores:str='single',
                                    trays_no:int=1,
                                    cables_no:int=1,
                                    installation_method:str='tray_horizontal_touched',
                                    installation_formation:str='flat') -> float:
        '''
        Reduction factors for groups of more than one multi-core cable in air 
        to be applied to the current-carrying capacity for one multi-core cable in free air [Table 10] and 
        reduction factors for groups of more than one circuit of single-core cables (note 2) 
        to be applied to the current carrying capacity for one circuit of single-core cable in free air [Table 11].
        
        Note 1: Values given are averages for the cable types and range of conductor sizes considered. The spread of values is generally less than 5%
        Note 2: Factors apply to single layer groups of cables as shown above and do not apply when cables are installed in more than one layer
        touching each other. Values for such installations may be significantly lower and must be determined by an appropriate method.
        Note 3: Values are given for vertical spacing between trays of 300 mm and at least 20 mm between trays and wall. For closer spacing, the
        factors should be reduced.
        Note 4: Values are given for horizontal spacing between trays of 225 mm with trays mounted back to back. For closer spacing the factors
        should be reduced.
        
        parameters:
        ----------
            cores : str (default: single)
                is the cable single or multi core cable 
            trays_no : int (default: 1)
                number of trays  
            cables_no : int (default: 1)
                number of cables on trays 
            installation_method : str (default: tray_horizontal_spaced)
                cable installation method (tray_horizontal_touched / tray_vertical_touched / tray_horizontal_spaced /tray_vertical_spaced / 
                ladder_touched / ladder_spaced) 
            installation_formation :  str (default: 'flat'')
                formation of single core cables flat or trefoil
            
        
        Returns:
        --------
            float : derating factor
        '''        
        factor = 1
        if cores == 'single': 
                out = self.grouping_derating_factors.loc[(self.grouping_derating_factors.cores == cores) & \
                                        (self.grouping_derating_factors.trays_no == trays_no) & \
                                        (self.grouping_derating_factors.cables_no == cables_no) & \
                                        (self.grouping_derating_factors.installation_method == f'{installation_method}_{installation_formation}'),'factor']
                factor = next(iter(out),1)
                
        else:
            out = self.grouping_derating_factors.loc[(self.grouping_derating_factors.cores == cores) & \
                                    (self.grouping_derating_factors.trays_no == trays_no) & \
                                    (self.grouping_derating_factors.cables_no == cables_no) & \
                                    (self.grouping_derating_factors.installation_method == installation_method),'factor']
            factor = next(iter(out),1)
        return factor
    
    def __voltage_drop__(self,
                        conductor_material:str='cu',
                        insulation_material:str='pvc',
                        cores:str='single',
                        csa:float=1.5,
                        installation_formation:str='flat',
                        armour_type:str='none'):
        '''
            Voltage drop for single core LV cables (0.6/1 kV) [Table 18,19].
            
            parameters:
            -----------
                conductor_material : str (default: cu)
                    'cu' copper and 'al' for aluminium 
                insulation_material : str (default: pvc)
                    conductor insulating material pvc or xlpe 
                cores : str (default: single)
                    cable cores single or multi core cable 
                csa : float (default: 1)
                    cable cross sectional area (1/1.5/2.5/4/6/10/16/25/35/50/75/90/120/150/185/240/300)     
                installation_formation : str (default: flat)
                    cable formation flat or trefoil 
                armour_type : str (default: flat)
                    cable armour type  steal tape armour (sta) ,steal wire armour (swa) ,
                    aluminium tape armour / aluminium wire armour (awa)
            Returns:
            --------
                float : derating factor
            '''       
        selection = ''
        match armour_type:
            case 'none':
                selection = installation_formation
            case 'ata' :
                selection = f'{installation_formation}_ata'
            case 'awa' :
                selection = f'{installation_formation}_awa'
            case _:    
                selection = installation_formation
                    
        out =  self.voltage_drop.loc[(self.voltage_drop.cores == cores) & \
                                    (self.voltage_drop.conductor_material == conductor_material) & \
                                    (self.voltage_drop.insulation_material == insulation_material) & \
                                    (self.voltage_drop.csa == csa),selection]
        
        factor = next(iter(out),1)
        r_cu =22
        r_al = 36
        x_3p_s = 0.09
        x_3p_m = 0.08
        x_1p = 0.12
        factor_cal = math.sqrt(3) * ( r_cu if conductor_material=='cu' else r_al) * ( 0.8 + 0.6 * (x_3p_m if cores=='multi' else x_3p_s) ) / csa
        return factor
    
    def __voltage_drop_calc__(self,
                            row,load_type='distribution_3ph',
                            ambient_temperature=20):
        
        out =  self.voltage_drop
        r_cu =22
        r_al = 36
        x_3p_s = 0.09
        x_3p_m = 0.08
        x_1p = 0.12
        x = 0
        if load_type == '3ph_s':
            x = x_3p_s
        if load_type == '3ph_m':
            x = x_3p_m
        if load_type == '1ph':
            x = x_1p
        resis_corr = ( ( r_cu if row.conductor_material=='cu' else r_al)  / row.csa1)* (1+0.00393*(ambient_temperature-20))
        
        if type(row.ac_resistance_20deg) == str:
            row.ac_resistance_20deg = float(row.ac_resistance_20deg.split('/')[0])
        return math.sqrt(3) * resis_corr * (0.8 + x * 0.6) 
                
    def get_icc(self,
                conductor_material:str='cu',
                insulation_material:str='pvc',   
                sheath_material:str='pvc',   
                cores:int=1,
                armour_type:str='none',
                size:float=1):
        '''
        Current carrying capacity.
        
        parameters:
        -----------
            conductor_material : str (default: cu)
                cable conductor material cu/al 
            insulation_material : str (default: pvc)
                conductor insulation material  
            sheath_material : str (default: pvc)
                sheath insulation material  
            cores : int (default:1)
                number of cable cores 
            armour_type : str (default:none)
                type of armour (steal tape 'STA'/steal wires 'SWA'/alumonium wires 'awa' ) 
            cable_size : float (default: 1)
                cable cross sectional area (1/1.5/2.5/4/6/10/16/25/35/50/75/90/120/150/185/240/300) 
        Returns:
        -------
            DataFrame : cable current capacity
        '''        
        try:
            self.icc['csa1'] = double(self.icc.csa.str.extract(r'(\d+)'))
            result= self.icc.loc[(self.icc.conductor_material == conductor_material) & \
                (self.icc.insulation_material == insulation_material) & \
                (self.icc.sheath_material == sheath_material) & \
                (self.icc.armour_type == armour_type) & \
                (self.icc.cores == cores)  & \
                (self.icc.csa1  == double(size) ) \
                ]
            if result.empty:
                0
            else:
                return result.iloc[0]

        except ValueError as e:
            print(f"{e}")  
    
    def get_size(self,
                il, 
                conductor_material:str='cu',
                insulation_material:str='pvc',   
                sheath_material:str='pvc',   
                cores:int=1,
                armour_type:str='none'):
        '''
        Get cable size based on load current.
        
        parameters:
        -----------
            il : float
                load current
            conductor_material : str (default: cu)
                cable conductor material cu/al 
            insulation_material : str (default: pvc)
                conductor insulation material  
            sheath_material : str (default: cu)
                'cu' copper and 'al' for aluminium 
            cores : int (default:1)
                number of cable cores 
            armour_type : str (default:none)
                type of armour (steal tape 'STA'/steal wires 'SWA'/alumonium wires 'awa' ) 
        Returns:
        --------
            float : cable current capacity
        '''        
        try:
            self.icc['csa1'] = double(self.icc.csa.str.extract(r'(\d+)'))
            filtered_list = self.icc.loc[(self.icc.conductor_material == conductor_material) & \
                (self.icc.insulation_material == insulation_material) & \
                (self.icc.sheath_material == sheath_material) & \
                (self.icc.armour_type == armour_type) & \
                (self.icc.cores == cores ) \
                ]
            filtered_list.iloc[(filtered_list.amps_laid_in_air_flat_spaced-il).abs().idxmin()]['csa']
        except ValueError as e:
            print(f"{e}")  
    
    def get_cable_Lmax(self,
                    voltage_drop:float,
                    load_voltage:float,
                    power_factor:float,
                    load_amps:float,
                    cable_resis:float,
                    ambient_temperature:int,
                    conductor_material:str='cu',
                    cable_csa:float=1.5,
                    load_type:str='distribution_1ph'
                    ):
        '''
        Get the cable maximum run based on calculated voltage drop.
        
        parameters:
        -----------
            voltage_drop : float
                load voltage drop in percent
            load_voltage : float 
                load nominal voltage in volts
            power_factor : float
                power factor    
            load_amps : float 
                load current in amps
            cable_resis : float
                cable ac resistance in ohms
            ambient_temperature : int 
                cable ambient temperature in degree celisius
            conductor_material : str (default: cu)
                cable conductor material cu/al 
            cable_csa : float (default: 1)
                cable cross sectional area (1/1.5/2.5/4/6/10/16/25/35/50/75/90/120/150/185/240/300) 
            load_type : str
                distribution_1ph / distribution_3ph / motor_3ph    
        Returns:
        --------
            float : maximum cable run in meters
        '''        
        #ΔV = (I x L x R x Cos φ) / 1000
        r_cu =22
        r_al = 36
        x_3p_s = 0.09
        x_3p_m = 0.08
        x_1p = 0.12
        x = 0
        if load_type == '3ph_s':
            x = x_3p_s
        if load_type == '3ph_m':
            x = x_3p_m
        if load_type == '1ph':
            x = x_1p
        resis_corr = ( ( r_cu if conductor_material=='cu' else r_al)  / cable_csa)* (1+0.00393*(ambient_temperature-20))
        
        if type(cable_resis) == str:
            cable_resis = float(cable_resis.split('/')[0])
        pf = power_factor if power_factor!=0 else 0.85
        Lmax = 0
        match load_type:
                    case 'distribution_1ph':
                        Lmax = (load_voltage*voltage_drop/100) * 1000 / (2*load_amps*(pf+math.sin(math.acos(pf))))
                    case 'distribution_3ph':
                        Lmax = (load_voltage*voltage_drop/100)  * 1000 / (math.sqrt(3)*load_amps*(pf+math.sin(math.acos(pf))))
                    case _:
                        pass
                            
        return Lmax

    def  select_cable(self,
                    load_current:float,
                    cable_run:float,
                    load_voltage:float,
                    load_type:str,
                    ac_dc:str = 'ac',
                    load_pf:float = 0.80,
                    voltage_drop_max:float = 3,
                    ambient_temperature:float=30,
                    trays_no:int = 1,
                    cricuits_in_tray:int = 1,
                    ground_temperature:float=20,
                    ground_thermal_resistivity:float = 100,
                    burial_depth:float = 0.5,
                    distence_between_burried_circuits:float = 0.3,
                    cable_armour:str='none',
                    installation_method:str='tray_horizontal_spaced',
                    installation_formation:str= 'flat',                    
                    extr_derating:float=1
                    ):
        
        '''select a cable based on the supplied parameters , selection is based on elsweedy cables  
        
        parameters:
        -----------
            load_current : float 
                loading current in amps
            cable_run : float 
                cable run length in meters
            load_voltage :float
                load voltage level (230 / 400) 
            load_type : str 
                distribution_1ph / distribution_3ph / motor_3ph    
            ac_dc : str (default: ac)
                load voltage type (ac / dc) 
            load_pf : float (default: 0.85)
                load power factor (0-1) 
            voltage_drop_max : float (default: 3)
                Max allowed voltage drop in percent , for distribution it should be 3% ,and for motors should be 5% based on IEC
            ambient_temperature : float (default: 30)
                cable ambient temperature 
            trays_no : int (default:1)
                number of trays for grouped cables 
            cricuits_in_tray : int (default:1)
                number of circuits in a tray for grouped cables  
            ground_temperature : float (default: 20)
                cable ground temperature 
            ground_thermal_resistivity : float (default: 100)
                Soil thermal resistivity K.m/W 
            burial_depth : float (default: 0.5)
                cable barial depth in meters 
            distence_between_burried_circuits : float (default: 0.3)
                distance between cables in meters
            cable_armour : str (default: 'none')
                    cable armour type  steal tape armour (sta) ,steal wire armour (swa) ,
                    aluminium tape armour / aluminium wire armour (awa)   
            installation_method : str (default: tray_horizontal_spaced)
                cable installation method 
                    (
                    tray_horizontal_spaced /  
                    tray_vertical_spaced /
                    tray_horizontal_touched / 
                    tray_vertical_touched /
                    ladder_touched / 
                    ladder_spaced
                    burried_direct /
                    burried_duct
                    ) 
            installation_formation : str (default: flat)
                    cable formation flat or trefoil        
            extr_derating : float (default:1)
                extra derating for the cable from 0.1 to 1 
                
        Returns:
        --------
            dataframe : cable_list 
        
        Examples:
        --------
        create new cable object
        >>> new_cable_class = Cable()
        
        use the select_cable() function and fill out the data
        
        >>> selected_new_cable = new_cable_class.select_cable(load_voltage= 400, 
        ...                             load_current=30,
        ...                             cable_run=100,
        ...                             ground_temperature=45,
        ...                             installation_method='burried_direct',
        ...                             cable_armour='sta',
        ...                             installation_formation='flat')
        
        print the results
        
        >>> print(selected_new_cable)
        
        you can export the results to csv
        
        >>> selected_new_cable.to_csv('result.csv',index=False)
        '''
        try:
            derating_needed = False
            if (ambient_temperature > 30) | (ground_temperature > 20) | (ground_thermal_resistivity >100):
                derating_needed = True
            # checking voltage
            if (load_voltage > 1000) | (ac_dc == 'dc'):
                raise Exception('voltage is not supported.')
            # checking for Icc
            suitable_cables = self.icc
            # fixing sizes for calculation
            suitable_cables['csa1'] = double(suitable_cables.csa.str.extract(r'(\d+)'))
            suitable_cables['amps_derated'] = pd.Series(dtype=float)
            suitable_cables['derating_factor'] = pd.Series(dtype=float)
            suitable_cables['Vd'] = pd.Series(dtype=float)
            suitable_cables['max_cable_run'] = pd.Series(dtype=float)
            # common derating factors
            pvc_derating = self.__pvc_rated_temperature_derating_factors__(temperrature=ambient_temperature)
            # free air derating    
            pvc_air_df = self.__air_temprature_derating_factor__(ambient_temperature,'pvc')
            xlpe_air_df = self.__air_temprature_derating_factor__(ambient_temperature,'xlpe')
            # underground derating
            pvc_derating_ground_temp =self.__ground_temprature_derating_factor__(ground_temperature=ground_temperature,insulationmaterial='pvc')
            xlpe_derating_ground_temp =self.__ground_temprature_derating_factor__(ground_temperature=ground_temperature,insulationmaterial='xlpe')
            # installation method derating
            installtion_details = installation_method.split("_")
            touched_spaced = ''
            if len(installtion_details)>2:
                touched_spaced = installtion_details[2] # touched or spaced
            air_burried = ''
            if (installtion_details[0] == 'tray') | (installtion_details[0] == 'tray'):
                air_burried = 'free_air'
            else:
                air_burried = 'ground'
            # getting derating factors
            if air_burried == 'free_air':
                if (load_type == 'distribution_3ph') | (load_type == 'motor_3ph'):
                    grouping_factor_single = self.__grouping_derating_factors__(cores='single',trays_no=trays_no,cables_no=cricuits_in_tray,installation_method=installation_method)
                if load_type == 'distribution_1ph':
                    grouping_factor_single = self.__grouping_derating_factors__(cores='single',trays_no=trays_no,cables_no=cricuits_in_tray,installation_method=installation_method)
                grouping_factor_muli = self.__grouping_derating_factors__(cores='multi',trays_no=trays_no,cables_no=cricuits_in_tray,installation_method=installation_method)
                
                derating_factor_single_pvc = pvc_air_df * pvc_derating * grouping_factor_single * extr_derating
                derating_factor_multi_pvc = pvc_air_df * pvc_derating * grouping_factor_muli* extr_derating
                derating_factor_single_xlpe = xlpe_air_df *  grouping_factor_single* extr_derating
                derating_factor_multi_xlpe = xlpe_air_df *  grouping_factor_muli* extr_derating
                
                suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'pvc'),'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'pvc'),f'amps_laid_in_air_{installation_formation}_{touched_spaced}']*derating_factor_single_pvc

                suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'pvc') ,'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'pvc') ,f'amps_laid_in_air_{installation_formation}_{touched_spaced}']*derating_factor_multi_pvc
                
                
                suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'xlpe'),'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'xlpe'),f'amps_laid_in_air_{installation_formation}_{touched_spaced}']*derating_factor_single_xlpe


                suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'xlpe'),'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'xlpe'),f'amps_laid_in_air_{installation_formation}_{touched_spaced}']*derating_factor_multi_xlpe
                
                
                suitable_cables = suitable_cables.loc[suitable_cables.amps_derated > load_current]   
            
            if air_burried == 'ground':
                
                grouping_factor_single = self.__grouping_derating_factors__(cores='single',trays_no=trays_no,cables_no=cricuits_in_tray,installation_method=installation_method)
                grouping_factor_muli = self.__grouping_derating_factors__(cores='multi',trays_no=trays_no,cables_no=cricuits_in_tray,installation_method=installation_method)
                
                derating_factor_single_pvc = pvc_derating_ground_temp * pvc_derating * grouping_factor_single * extr_derating
                derating_factor_multi_pvc = pvc_derating_ground_temp * pvc_derating * grouping_factor_muli* extr_derating
                derating_factor_single_xlpe = xlpe_derating_ground_temp *  grouping_factor_single* extr_derating
                derating_factor_multi_xlpe = xlpe_derating_ground_temp *  grouping_factor_muli* extr_derating
                
                
                installation_formation_str = ''
                if installation_method == 'burried_direct':
                    installation_formation_str = f'amps_laid_in_groud_{installation_formation}'
                else:
                    installation_formation_str = f'amps_laid_in_groud_duct'
                
                suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'pvc'),'derating_factor']=derating_factor_single_pvc
                suitable_cables.loc[(suitable_cables.cores >1) & (suitable_cables.insulation_material == 'pvc'),'derating_factor']=derating_factor_multi_pvc
                suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'xlpe'),'derating_factor']=derating_factor_single_xlpe
                suitable_cables.loc[(suitable_cables.cores >1) & (suitable_cables.insulation_material == 'xlpe'),'derating_factor']=derating_factor_multi_xlpe
                
                
                suitable_cables  = suitable_cables.loc[(suitable_cables.armour_type == cable_armour)] 
                suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'pvc'),'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'pvc') ,installation_formation_str]*derating_factor_single_pvc
                
                suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'pvc'),'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'pvc') ,installation_formation_str]*derating_factor_multi_pvc
                
                suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'xlpe') ,'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores ==1) & (suitable_cables.insulation_material == 'xlpe'),installation_formation_str]*derating_factor_single_xlpe


                suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'xlpe') & (suitable_cables.armour_type == cable_armour),'amps_derated'] = \
                        suitable_cables.loc[(suitable_cables.cores > 1) & (suitable_cables.insulation_material == 'xlpe') & (suitable_cables.armour_type == cable_armour),installation_formation_str]*derating_factor_multi_xlpe
                
                suitable_cables.loc[(suitable_cables.cores ==1),'amps_derated'] =  \
                        suitable_cables.loc[(suitable_cables.cores ==1)].apply (lambda x:x.amps_derated * self.__burial_depth_derating_factors__(depth=burial_depth,installation_method=installation_method,cores='single',cable_size=x.csa1) , axis=1) 
                suitable_cables.loc[(suitable_cables.cores >1),'amps_derated'] =  \
                        suitable_cables.loc[(suitable_cables.cores >1)].apply (lambda x: x.amps_derated * self.__burial_depth_derating_factors__(depth=burial_depth,installation_method=installation_method,cores='multi',cable_size=x.csa1) , axis=1) 
                if cricuits_in_tray > 1:
                    suitable_cables.loc[(suitable_cables.cores ==1),'amps_derated'] =  \
                        suitable_cables.loc[(suitable_cables.cores ==1)].apply (lambda x: x.amps_derated *self.__laid_direct_in_ground_derating_factors__(cores='single',circuits_no=cricuits_in_tray,installation_formation=installation_formation,spacing=distence_between_burried_circuits) , axis=1) 
                    suitable_cables.loc[(suitable_cables.cores >1),'amps_derated'] =  \
                        suitable_cables.loc[(suitable_cables.cores >1)].apply (lambda x: x.amps_derated *self.__laid_direct_in_ground_derating_factors__(cores='multi',circuits_no=cricuits_in_tray,installation_formation=installation_formation,spacing=distence_between_burried_circuits) , axis=1) 
                            
                suitable_cables = suitable_cables.loc[suitable_cables.amps_derated > load_current]                       
            # getting voltage drop
            if (load_type == 'distribution_3ph') & (load_pf == 0.8):
                suitable_cables['Vd'] =  suitable_cables.apply \
                    (lambda x:  load_current*self.__voltage_drop__(cores='single' ,conductor_material=x['conductor_material'] ,csa=x['csa1'], insulation_material=x['insulation_material'],installation_formation=installation_formation , armour_type=cable_armour) * cable_run/1000 if x['cores']== 1 else \
                        load_current*self.__voltage_drop__(cores='multi' ,conductor_material=x['conductor_material'] ,csa=x['csa1'], insulation_material=x['insulation_material'],installation_formation=installation_formation, armour_type=cable_armour) * cable_run/1000  , axis=1) #load_current*self.__voltage_drop__(csa=x['csa1'],cores='multi') * cable_run/1000
            else:
                suitable_cables['Vd'] =  suitable_cables.apply (lambda x:  (load_current*7 if load_type=='motor_3ph' else 1) * load_current*self.__voltage_drop_calc__(x,load_type=load_type,ambient_temperature=ambient_temperature) * cable_run/1000, axis=1) 
            suitable_cables = suitable_cables[suitable_cables['Vd'] < (voltage_drop_max*load_voltage/100) ]
            
            #getting cable
            suitable_cables_1c = suitable_cables[suitable_cables.cores==1]
            suitable_cables_1c.reset_index(inplace=True)
            
            suitable_cables_multi = suitable_cables[suitable_cables.cores>2]
            suitable_cables_multi.reset_index(inplace=True)

            if len(suitable_cables_1c) >0:
                #suitable_cables_1c.to_csv('suitable_cables_1c.csv')    
                least_suitable_cables_1c=suitable_cables_1c.iloc[suitable_cables_1c['csa1'].idxmin()]
                least_suitable_cables_1c['max_cable_run'] = self.get_cable_Lmax(voltage_drop=voltage_drop_max,
                                                                    load_voltage=load_voltage,            
                                                                    load_amps=load_current,
                                                                    cable_resis= least_suitable_cables_1c.ac_resistance_20deg,
                                                                    ambient_temperature=ambient_temperature,
                                                                    conductor_material=least_suitable_cables_1c.conductor_material,
                                                                    cable_csa=least_suitable_cables_1c.csa1,
                                                                    load_type=load_type,
                                                                    power_factor=load_pf)
            else:
                least_suitable_cables_1c = pd.Series(data=['No single core available'])
            if len(suitable_cables_multi) >0: 
                #suitable_cables_multi.to_csv('suitable_cables_multi.csv')
                suitable_cables_multi=suitable_cables_multi.iloc[suitable_cables_multi['csa1'].idxmin()]
                suitable_cables_multi['max_cable_run'] = self.get_cable_Lmax(voltage_drop=voltage_drop_max,
                                                                    load_voltage=load_voltage,            
                                                                    load_amps=load_current,
                                                                    cable_resis= suitable_cables_multi.ac_resistance_20deg,
                                                                    ambient_temperature=ambient_temperature,
                                                                    conductor_material=suitable_cables_multi.conductor_material,
                                                                    cable_csa=suitable_cables_multi.csa1,
                                                                    load_type=load_type,
                                                                    power_factor=load_pf)
            else:
                suitable_cables_multi = pd.Series()
            
            selection = pd.DataFrame([
                                    least_suitable_cables_1c,
                                    suitable_cables_multi
                                    ])            
            return selection
        except ValueError as e:
            print(f"{e}")  

# if __name__ == "__main__":
#     new_cable_class = CableOperations() #db_path="elsweedy_cables.db")
#     # asa proposal for grouping  extr_derating=0.75

#     selected_new_cable = new_cable_class.select_cable(
#                                 load_voltage= 400, 
#                                 load_current=39,
#                                 cable_run=250,
#                                 load_type='distribution_3ph', #motor_3ph
#                                 installation_method='burried_direct',
#                                 cable_armour='sta',
#                                 installation_formation='flat',
#                                 ground_temperature=45
#                                 )
#     print(selected_new_cable)
#     selected_new_cable.to_csv('result.csv',index=False)