import math
from typing import Optional,Union,Generic,TypeVar
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
# from ipywidgets import *

T = TypeVar('T')

class ACMachine:
    '''
    Ac induction machine class
    '''
    name = 'ACMachine' # class attribute
    
    def __init__(self):        
        # Nameplat data
        self._kw = None
        self._Vs = None
        self._Vr = None
        self._Is = None
        self._Ir = None
        self._Istart = None
        self._Inoload = None
        self._pf = None
        self._eff = None
        self._hz = None
        self._connection = None   
        # motor parameters
        self._X1 = None   
        self._R1 = None   
        self._R2_d = None 
        self._X2_d = None 
        self._Xm = None   
        self._Rc = None   
        self._Rstart = None  
        self._a = self._Vs / self._Vr if self._Vs !=None and self._Vr!=None and self._Vr !=0 else None
        # mechanical parameters
        self._rpm = None 
        self._poles = None
        self._s = None
        self._STmax = None
        self._Inertia = None
        self._Tr = None
        self._Tmax = None
        self._Tb = None
        self._frame = None
        self._mounting = None 
        self._ip = None 
        self._cooling = None 
        self._duty = None 
        self._rotation = None 
        self._thermalclass = None 
        self._weight = None 
        self._noise = None
        # lossess
        self._Pcu1 = None
        self._Pcu2 = None
        self._Pcu = None
        self._Pcore1 = None
        self._Pcore2 = None
        self._Pcore = None
        self._Pfre = None
        self._Plossess = self._Pcu1 if self._Pcu1 !=None else 0 + self._Pcu2 if self._Pcu2 !=None else 0 + self._Pcore1 if self._Pcore1 !=None else 0 
        + self._Pcore2 if self._Pcore2 !=None else 0 + self._Pfre if self._Pfre !=None else 0 
        #brand
        self._brand = None
        self._brandtype = None
        self._standard = None
        #bearings and grease
        self._greaseBrand = None
        self._greasetype = None
        self._greaseQtyDe = None
        self._greaseQtyNde = None
        self._greaseHrs = None
        self._deBearing = None
        self._de1Bearing = None
        self._ndeBearing = None
        # dimentions
        self._base_length = None
        self._base_width = None
        self._shaft_dia = None
        self._shaft_height = None
        self._extra = None
        
    #region properties    
    
    #region Nameplat data
    @property
    def kw(self) -> float:
        return self._kw

    @kw.setter
    def kw(self, value:float):
        if value < 0:
            raise ValueError('rated power cannot be less than 0')
        self._kw = value

    @property
    def Vs(self):
        return self._Vs

    @Vs.setter
    def Vs(self, value):
        self._Vs = value

    @property
    def Vr(self):
        return self._Vr

    @Vr.setter
    def Vr(self, value):
        self._Vr = value

    @property
    def Is(self):
        return self._Is

    @Is.setter
    def Is(self, value):
        self._Is = value

    @property
    def Ir(self):
        return self._Ir

    @Ir.setter
    def Ir(self, value):
        self._Ir = value

    @property
    def Istart(self):
        return self._Istart

    @Istart.setter
    def Istart(self, value):
        self._Istart = value

    @property
    def Inoload(self):
        return self._Inoload

    @Inoload.setter
    def Inoload(self, value):
        self._Inoload = value

    @property
    def pf(self):
        return self._pf

    @pf.setter
    def pf(self, value):
        self._pf = value

    @property
    def eff(self):
        return self._eff

    @eff.setter
    def eff(self, value):
        self._eff = value

    @property
    def hz(self):
        
        return self._hz

    @hz.setter
    def hz(self, value):
        self._hz = value

    @property
    def connection(self):
        '''
        s for star d for delta
        '''
        return self._connection

    @connection.setter
    def connection(self, value):
        self._connection = value
    #endregion
    
    #region motor parameters
    @property
    def X1(self):
        '''
        stator reactance
        '''
        return self._X1

    @X1.setter
    def X1(self, value):
        self._X1 = value

    @property
    def R1(self):
        '''
        stator resistance
        '''
        return self._R1

    @R1.setter
    def R1(self, value):
        self._R1 = value

    @property
    def R2_d(self):
        '''
        rotor resistance refered to stator
        '''
        return self._R2_d

    @R2_d.setter
    def R2_d(self, value):
        self._R2_d = value

    @property
    def X2_d(self):
        '''
        rotor reactnace refered to stator
        '''
        return self._X2_d

    @X2_d.setter
    def X2_d(self, value):
        self._X2_d = value

    @property
    def Xm(self):
        '''
        magnetizing reactnace
        '''
        return self._Xm

    @Xm.setter
    def Xm(self, value):
        self._Xm = value

    @property
    def Rc(self):
        '''
        magnetizing resistance
        '''
        return self._Rc

    @Rc.setter
    def Rc(self, value):
        self._Rc = value

    @property
    def Rstart(self):
        '''
        External starting resistance
        '''
        return self._Rstart

    @Rstart.setter
    def Rstart(self, value):
        self._Rstart = value
    
    @property
    def a(self):
        '''
        turns ratio 
        '''
        return self._a if self._a==None else self._Vs / self._Vr if self._Vs !=None and self._Vr!=None and self._Vr !=0 else None

    @a.setter
    def a(self, value):
        self._a = value
    #endregion
    
    #region mechanical parameters
    @property
    def rpm(self) -> int:
        '''
        motor rotor speed in rpm (not synchronous speed).
        '''
        return self._rpm

    @rpm.setter
    def rpm(self, value):
        self._rpm = value

    @property
    def poles(self) -> int:
        '''
        motor pole pairs
        '''
        if self._rpm < 800:
            self._poles =  8
        elif  self._rpm > 800 & self._rpm < 1000:
            self._poles = 6    
        elif  self._rpm > 1000 & self._rpm < 1500:
            self._poles = 4    
        elif  self._rpm > 1500:
            self._poles = 2
        else:
            raise ValueError('rpm value is not set') 
        return self._poles  

    @poles.setter
    def poles(self, value:int):
        self._poles = value

    @property
    def s(self):
        '''
        motor slip
        '''
        ns = 120*self._hz /self.poles 
        return self._s if self._s == None else ( (ns - self._rpm) / ns)

    @s.setter
    def s(self, value):
        self._s = value

    @property
    def STmax(self):
        return self._STmax

    @STmax.setter
    def STmax(self, value):
        self._STmax = value

    @property
    def Inertia(self):
        return self._Inertia

    @Inertia.setter
    def Inertia(self, value):
        self._Inertia = value

    @property
    def Tr(self):
        return self._Tr

    @Tr.setter
    def Tr(self, value):
        self._Tr = value

    @property
    def Tmax(self):
        return self._Tmax

    @Tmax.setter
    def Tmax(self, value):
        self._Tmax = value

    @property
    def Tb(self):
        return self._Tb

    @Tb.setter
    def Tb(self, value):
        self._Tb = value

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        self._frame = value

    @property
    def mounting(self):
        '''
        mounting types B3,B5 , ...
        '''
        return self._mounting

    @mounting.setter
    def mounting(self, value):
        self._mounting = value

    @property
    def ip(self):
        return self._ip

    @ip.setter
    def ip(self, value):
        self._ip = value

    @property
    def cooling(self):
        '''
        cooling type
        '''
        return self._cooling

    @cooling.setter
    def cooling(self, value):
        self._cooling = value

    @property
    def duty(self):
        '''
        S1,...
        '''
        return self._duty

    @duty.setter
    def duty(self, value):
        self._duty = value

    @property
    def rotation(self):
        '''
        cw ,ccw , cw/ccw
        '''
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value

    @property
    def thermalclass(self):
        '''
        motor thermal class type e.g F , B, H
        '''
        return self._thermalclass

    @thermalclass.setter
    def thermalclass(self, value):
        self._thermalclass = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def noise(self):
        return self._noise

    @noise.setter
    def noise(self, value):
        self._noise = value
    #endregion
    
    #region lossess
    @property
    def Pcu1(self):
        return self._Pcu1

    @Pcu1.setter
    def Pcu1(self, value):
        self._Pcu1 = value

    @property
    def Pcu2(self):
        return self._Pcu2

    @Pcu2.setter
    def Pcu2(self, value):
        self._Pcu2 = value

    @property
    def Pcu(self):
        return self._Pcu

    @Pcu.setter
    def Pcu(self, value):
        self._Pcu = value

    @property
    def Pcore1(self):
        return self._Pcore1

    @Pcore1.setter
    def Pcore1(self, value):
        self._Pcore1 = value

    @property
    def Pcore2(self):
        return self._Pcore2

    @Pcore2.setter
    def Pcore2(self, value):
        self._Pcore2 = value

    @property
    def Pcore(self):
        return self._Pcore

    @Pcore.setter
    def Pcore(self, value):
        self._Pcore = value

    @property
    def Pfre(self):
        return self._Pfre

    @Pfre.setter
    def Pfre(self, value):
        self._Pfre = value

    @property
    def Plossess(self):
        return self._Plossess 

    @Plossess.setter
    def Plossess(self, value):
        self._Plossess = value
    
    #endregion
    
    #region brand
    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        self._brand = value

    @property
    def brandtype(self):
        return self._brandtype

    @brandtype.setter
    def brandtype(self, value):
        self._brandtype = value

    @property
    def standard(self):
        return self._standard

    @standard.setter
    def standard(self, value):
        self._standard = value
    #endregion
    
    #region bearings and grease
    @property
    def greaseBrand(self):
        return self._greaseBrand

    @greaseBrand.setter
    def greaseBrand(self, value):
        self._greaseBrand = value

    @property
    def greasetype(self):
        return self._greasetype

    @greasetype.setter
    def greasetype(self, value):
        self._greasetype = value

    @property
    def greaseQtyDe(self):
        return self._greaseQtyDe

    @greaseQtyDe.setter
    def greaseQtyDe(self, value):
        self._greaseQtyDe = value

    @property
    def greaseQtyNde(self):
        return self._greaseQtyNde

    @greaseQtyNde.setter
    def greaseQtyNde(self, value):
        self._greaseQtyNde = value

    @property
    def greaseHrs(self):
        return self._greaseHrs

    @greaseHrs.setter
    def greaseHrs(self, value):
        self._greaseHrs = value

    @property
    def deBearing(self):
        return self._deBearing

    @deBearing.setter
    def deBearing(self, value):
        self._deBearing = value

    @property
    def de1Bearing(self):
        return self._de1Bearing

    @de1Bearing.setter
    def de1Bearing(self, value):
        self._de1Bearing = value

    @property
    def ndeBearing(self):
        return self._ndeBearing

    @ndeBearing.setter
    def ndeBearing(self, value):
        self._ndeBearing = value
    #endregion
    
    #region dimentions
    @property
    def base_length(self):
        return self._base_length

    @base_length.setter
    def base_length(self, value):
        self._base_length = value

    @property
    def base_width(self):
        return self._base_width

    @base_width.setter
    def base_width(self, value):
        self._base_width = value

    @property
    def shaft_dia(self):
        return self._shaft_dia

    @shaft_dia.setter
    def shaft_dia(self, value):
        self._shaft_dia = value

    @property
    def shaft_height(self):
        return self._shaft_height

    @shaft_height.setter
    def shaft_height(self, value):
        self._shaft_height = value

    @property
    def extra(self):
        return self._extra

    @extra.setter
    def extra(self, value):
        self._extra = value
    #endregion
    
    
    #endregion
    
    def intit_typicals(self,kw,Vs=400,Is=None,rpm =None,hz =50,pf = 0.82 , eff = 0.8 , Vr =None,Ir =None):
        self._kw = kw
        self._Vs = Vs
        self._Vr = Vr
        self._Is = Is if Is != None else kw*2
        self._Ir = Ir
        self._pf = pf
        self._eff = eff
        self._hz = hz
        self.rpm = rpm 
        self._a = self._Vs / self._Vr if self._Vs !=None and self._Vr!=None and self._Vr !=0 else None
    
    @classmethod
    def __rms_to_max__(cls,value):
        return np.sqrt(2)*value
    
    @classmethod
    def __rms_to_average__(cls,value):
        return 2*np.sqrt(2)*value / np.pi
    
    def __slip__(self,rpm:int=None) -> float:
        '''
        calculates the motor slip (n_sync - n_rotor / n_sych) based on different rpm values
        
        Parameters
        ----------
        rpm : int 
            spread sheet file name (should be in this database direcotry)
        
        Notes
        ------
        motor rated frequency and poles(or rpm) should be defined
        
        Returns
        -------
            slip value : Float
        '''
        ns = (120*self._hz /self.poles ) 
        nr = rpm 
        return (ns - nr)/ ns  
    
    def __slip_approx_undervoltage___(self,volt:int) -> float:
        '''
        calculates Steady-state slip of induction motor at undervoltage,
        based on the small-slip approximation s ∝ 1 /V^2.
        Parameters
        ----------
        volt : int 
            voltage drop value
        
        Notes
        ------
        motor rated frequency and poles(or rpm) should be defined
        
        Returns
        -------
            new slip value at voltage drop : Float
        '''
        if self._poles ==0:
            self._poles = self.__poles__()
        s_rat = self.__slip__(rpm=self.rpm)
        s_low = s_rat *  (self._Vs/volt)**2
        return s_low
    
    def __rpm_approx_undervoltage___(self,volt:int) -> float:
        '''
        calculates Steady-state rpm of induction motor at undervoltage,
        based on the small-slip approximation s ∝ 1 /V^2 slip is caluculated,
        Parameters
        ----------
        volt : int 
            voltage drop value
        
        Notes:
        ------
        motor rated frequency and poles(or rpm) should be defined
        
        Returns:
        -------
            new rpm value at voltage drop : Float
        '''
        s_low = self.__slip_approx_undervoltage___(volt)
        return (1-s_low) * (120*self._hz/ self._poles) 

    def torque(self,speed,Rext=0):
        '''
        Motor output torque as a function of speed 
        and with Rext (in case of resistor starting) 
        
        Parameters:
            speed (float): Motor speed in rpm
            Rext (float):  External resistor for starting in ohm
        Returns:
            Torque (float) : Motor output torque in N.m
        '''    
        slip = self.__slip__(speed)
        if np.isscalar(slip) and np.isnan(slip): 
            return 0
        
        Wsyn = 4*np.pi * self._hz / self._poles
        Rth = np.float_power( self._Xm / (self._Xm+self._X1) ,2) * self._R1
        Xth = self._X1
        Vth = (self._Xm * self._Vs) / np.sqrt((np.float_power(self._R1,2)  + np.float_power(self._X1+self._Xm ,2 )))
        T = (np.float_power(Vth,2) * (self._R2_d + Rext)) / ( Wsyn *(np.float_power(Rth+((self._R2_d + Rext)/slip) ,2 ) + np.float_power(Xth+self._X2_d ,2 )) * slip)
        #T = np.float_power(self.Vs,2) * self.R2_d / ( Wsyn *np.float_power(Rth+(self.R2_d/self.s) ,2 ) * np.float_power(Xth+self.X2_d ,2 ) * self.s )
        T[np.isnan(T)] = 0
        return T
    
    def torque_slip_Vsmal(self):
        '''
        calculate the approximated torque when slip values are very small 
        '''
        Wsync = 1/(4*np.pi*self._hz)
        slip = (120*self._hz/self._poles) - self.rpm / (120*self._hz/self._poles)
        return (self._Vs^2 * slip) /(Wsync*(self._R2_d)) 
    
    def torque_approx(self,speed=None):
        '''
        Using approximate IEEE equivalent cIscuit to get the torq vs speed
        '''
        try:
            if self.Xth == None:
                raise Exception('Xth must be set')
            if self._X2_d == None:
                raise Exception('X2_d must be set')
            
            nr = speed if speed == None else self.rpm
            Wsync = 1/(4*np.pi*self._hz)
            slip = (120*self._hz/self._poles) - nr / (120*self._hz/self._poles)
            return (self._Vs^2 * self._R2_d) /(Wsync*(self.Xth+self._X2_d)*slip) 
        except Exception as e:
            print(e)
    
    def torque_estmiate(self):
        ''' Toque estimation based on power in kw and speed in rpm
        using the formula  9.5488 * ACP / S
        '''
        return 9.5488 * self._kw*1000 / self.rpm
    
    def torque_from_current(self,i):
        '''
        calculate the torque based on operating current 
        while all [voltage , power factor,effiecincy, and rpm] are const
        '''
        return (self._Vs * i * self._pf * self._eff) / (self.rpm) 
    
    def torque_max(self):
        '''
        
        '''
        Wsyn = 4*np.pi * self._hz / self._poles
        Rth = np.float_power( self._Xm / (self._Xm+self._X1) ,2) * self._R1
        Xth = self._X1
        Vth = (self._Xm * self._Vs) / np.sqrt((np.float_power(self._R1,2)  + np.float_power(self._X1+self._Xm ,2 )))
        T = np.float_power(Vth,2)/ (2* Wsyn *  (Rth+ np.sqrt( np.float_power(Rth,2) + np.float_power(Xth+self._X2_d ,2 ) ) ))
        #T = np.float_power(Vth,2)/ (2* Wsyn *  (Xth+self.X2_d ))
        return T
    
    def test_data(self,Vnl,Inl,Pnl,Freqnl, Vbr,Ibr,Pbr,Freqbr):
        '''
        Motor No load and blocked rotor tests
        '''
        #no load test
        # rotaional lossess 
        self.Prot = Pnl - 3*np.float_power(Inl,2)   # W
        V1 = Vnl / np.sqrt(3)                # V/phase
        Znl = V1 / Inl                       # no load impedance in Ω   
        Rnl = Pnl / (3* np.float_power(Inl,2))               # no load resistance in Ω 
        Xnl = np.float_power((np.float_power(Znl,2) - np.float_power(Rnl,2)) ,0.5)            # no load reactance in Ω (that is X1 +Xm =XNnl) 
        # blocked rotor (short circuit) test
        Rbl = Pbr / (3*  np.float_power(Ibr,2) )                  # blocked rotor resistance in Ω 
        self._R2_d = Rbl - self._R1              
        Zbr = Vbr / (np.sqrt(3) * Ibr)       # blocked rotor impedance in Ω
        Xbl = np.float_power((np.float_power(Zbr,2) - np.float_power(Rbl,2)) ,0.5)         # blocked rotor reactance in Ω
        if Freqbr < Freqnl:                 # if blocked rotor test not at no load frequency adjust
           Xbl = Xbl * Freqnl / Freqbr
        self._X1 = Xbl/ 2
        self._X2_d = self._X1
        self._Xm = Xnl - self._X2_d
        self._R2_d  = np.float_power(((self._X2_d +self._Xm) / self._Xm),2) * self._R2_d
        self._Pcu1 ,self._Pcu2,self._Pcu ,self._Pcore1,self._Pcore2,self._Pcore,self._Pfre = self.__power_lossess__()
        self._Plossess = self._Pcu +self._Pcore+self._Pfre
        self._STmax = self.__slip_at_Tmax__()
        self._Rstart = self.__resistance_start__()
        self._Istart = self.__Is_start__() if self._Istart == 0 else self._Istart
        return self._R1,self._R2_d , self._X1 , self._X2_d , self._Xm
    
    def __Is_start__(self) -> float:
        V1 = self._Vs/ np.sqrt(3)
        Z1 = complex(self._R1 +self._X1) + (complex(0,self._Xm) * complex(self._R2_d,self._X2_d)) / complex(self._X2_d,self._Xm)
        Is = V1 / Z1
        Is = np.sqrt(np.float_power(Is.real,2) + np.float_power(Is.imag,2))
        return Is
    
    def __slip_at_Tmax__(self) -> float:
        Rth = np.float_power( self._Xm / (self._Xm+self._X1) ,2) * self._R1
        Xth = self._X1        
        return self._R2_d / np.sqrt(np.float_power(Rth,2)  + np.float_power(Xth+self._X2_d,2))
    
    def __resistance_start__(self) -> float:
        Rth = np.float_power( self._Xm / (self._Xm+self._X1) ,2) * self._R1
        Xth = self._X1   
        return np.sqrt(np.float_power(Rth,2)  + np.float_power(Xth+self._X2_d,2)) - self._R2_d 
        
    def __power_lossess__(self):
        # stator coppor losses
        Pcu1 = 3*np.float_power(self._Is,2) * self._R1 if self._Pcu1 == None else self._Pcu1
        # rotor coppor losses
        Pcu2 =  3*np.float_power(self._Ir,2) * (self._R2_d/np.float_power(self._a,2)) if self._Pcu2 == None else self._Pcu2
        # motor coppor losses
        Pcu = Pcu1+Pcu2
        # stator core losses
        Pcore1 = 0
        # rotor core losses
        Pcore2 = 0
        # motor core losses
        Pcore = Pcore1 + Pcore2
        # friction and windage losses
        Pfre = 0
        return Pcu1 ,Pcu2,Pcu ,Pcore1,Pcore2,Pcore,Pfre
        
    def undervoltage_lossess(self,voltage:int) -> float:
        '''
        Steady-state operation losses of induction motor at undervoltage
        
        Parameters
        ----------
        voltage : int 
            undervoltage value
            
        Returns
        -------
            Float : power lossses in kw
        '''
        #Based on the small-slip approximation s ∝ 1 /V^2, the new slip at the low voltage is
        slip_low = self.__slip_approx_undervoltage___(volt=voltage)
        # power at low voltage
        p_out = (1- slip_low)/(1 - self.__slip__(self.rpm)) * self._kw
        # rotor loss (I'r)**2*R'r in terms of the rated rotor copper loss at rated voltage.
        p_rot_copp = (slip_low/self.__slip__(self.rpm))
        return p_out

    def overvoltage_lossess(self,voltage:int) -> float:
        '''
        Steady-state operation of induction motor at overvoltage
        
        Parameters
        ----------
        voltage : int 
            overvoltage value
            
        Returns
        -------
            Float : power lossses in kw
        '''
        #Based on the small-slip approximation s ∝ 1 /V^2, the new slip at the low voltage is
        slip_low = self.__slip_approx_undervoltage___(volt=voltage)
        # power at low voltage
        p_out = (1- slip_low)/(1 - self.__slip__()) * self._kw
        # rotor loss (I'r)**2*R'r in terms of the rated rotor copper loss at rated voltage.
        p_rot_copp = (slip_low/self.__slip__())
        return p_out
    
    def draw_torque_speed(self,rpm_range:np.ndarray =None,Rext:float=0,Start_time:int=None,load_torque:np.ndarray=None):
        fig,ax = plt.subplots(figsize=(14,5))
        fig.tight_layout()
        ns = (120*self._hz /self._poles )
        rpm_range = rpm_range if rpm_range.any() else np.arange(-1*2*ns, 2*ns ,1)
        def init_fun():
            ax.set_ylabel('Torque (N.m)')
            ax.set_xlabel('speed (rpm)')
            ax.set_title('Torque/speed profile',fontsize=18 )
            ax.plot(rpm_range,self.torque(rpm_range),linewidth=5) 
            ax.text(100, self.torque_estmiate()+100,"Rated torque = {val:0,.2f} {val1}".format(val=self.torque_estmiate()/1000 , val1 = 'k.Nm'),fontsize=13 )
            ax.axhline(y = self.torque_estmiate() , color='r',linestyle= 'dashed' )
            ax.text(100, self.torque_max()+100, "Max torque = {val:0,.2f} {val1}".format(val=self.torque_max()/1000 , val1 = 'k.Nm'),fontsize=13 )
            ax.axhline(y = self.torque_max() , color='r',linestyle= 'dashed' )
            ax.grid(True, alpha=0.3, linestyle="--")
        
        if load_torque.any():
            init_fun()
            x = np.ones(len(rpm_range), dtype=int) * self.torque_estmiate() * 0.9
            line, = ax.plot(rpm_range,x,linewidth=5)

            def update(w = 1.0):
                line.set_ydata(w * x)
                fig.canvas.draw()
            slider = widgets.FloatSlider(value=0.9)
            slider.observe(update)
            interact(update)
        else: init_fun()   
        plt.show()
        # def update_line_chart(btn):
        #     for i in range(10):
        #         time.sleep(1)
        #         idx1 = np.random.choice(np.arange(self.torque_estmiate()*0.4 , self.torque_estmiate()*3))
        #         line.y = idx1 * x
        # btn = widgets.Button(description="Play", icon='play')
        # btn.on_click(update_line_chart)
        # widgets.VBox(btn)

                
        if Rext>0:
            ax.plot(rpm_range,self.torque(rpm_range,Rext=Rext))
            Pl1 = np.trapz(self.torque(rpm_range,Rext=Rext)) * Start_time/4
            ax.plot(rpm_range,self.torque(rpm_range,Rext=Rext*0.75)) 
            Pl2 = np.trapz(self.torque(rpm_range,Rext=Rext*0.75)) * Start_time/4
            ax.plot(rpm_range,self.torque(rpm_range,Rext=Rext * 0.5)) 
            Pl3 = np.trapz(self.torque(rpm_range,Rext=Rext*0.5)) * Start_time/4
            ax.plot(rpm_range,self.torque(rpm_range,Rext=Rext*0.25)) 
            Pl4 = np.trapz(self.torque(rpm_range,Rext=Rext*0.25)) * Start_time/4
            return (Pl1+Pl2+Pl3+Pl4) * 3
        return np.trapz(self.torque(rpm_range),rpm_range) * Start_time * 3 
    
    def draw_torque_speed_anim(self,rpm_range:np.ndarray =None,Rext:float=0,Start_time:int=None,load_torque:np.ndarray=None):
        
        ns = (120*self._hz /self._poles )
        rpm_range = rpm_range if rpm_range.any() else np.arange(-1*2*ns, 2*ns ,1)
        power_range =self.torque(rpm_range)
        
        fig,ax = plt.subplots(figsize=(14,5))
        ax = plt.axes(xlim=(0,6), ylim=(-10, 10))
        anim_data_skip = 50           
        # ax.set_xticklabels(idx, rotation=30)
        ax.legend()
        line2, =ax.plot(rpm_range[0],power_range[0],linewidth=5) 
        ax.text(100, self.torque_estmiate()+100,"Rated torque = {val:0,.2f} {val1}".format(val=self.torque_estmiate()/1000 , val1 = 'k.Nm'),fontsize=13 )
        ax.axhline(y = self.torque_estmiate() , color='r',linestyle= 'dashed' )
        ax.text(100, self.torque_max()+100, "Max torque = {val:0,.2f} {val1}".format(val=self.torque_max()/1000 , val1 = 'k.Nm'),fontsize=13 )
        ax.axhline(y = self.torque_max() , color='r',linestyle= 'dashed')
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.set_ylabel('Power (MW)')
        ax.set_xlabel('speed (rpm)')
        ax.set_title('Power/speed profile',fontsize=18)    
        def animate(frame):
            line2.set_xdata(rpm_range[frame])
            line2.set_ydata(power_range[frame])
            return line2
        anim = FuncAnimation(fig, animate, frames= len(rpm_range), interval=50, repeat=False)
        anim._start()
        plt.show()
        
    def draw_power_speed(self,rpm_range:np.ndarray =None):
        fig,ax = plt.subplots(figsize=(14,5))
        ax.set_ylabel('Power (MW)')
        ax.set_xlabel('speed (rpm)')
        ax.set_title('Power/speed profile',fontsize=18 )
        ns = (120*self._hz /self._poles )
        rpm_range = rpm_range if rpm_range.any() else np.arange(-1*2*ns, 2*ns ,1)
        power_range = (self.torque(rpm_range) * rpm_range) / 1000000
        ax.plot(rpm_range, power_range) 
        print(power_range)
        # ax.text(ns-100, self.kw+100,'rated Power',fontsize=13 )
        # ax.axhline(y = self.kw , color='r',linestyle= 'dashed' )
        
        # ax.text(ns-100, self.torque_max() +100,'max Power',fontsize=13 )
        # ax.axhline(y = self.torque_max() , color='r',linestyle= 'dashed' )

    @classmethod
    def to_string(cls):
        return cls.name
    
    @classmethod
    def to_object(cls,kw,Vs=400,Is=None,rpm =None,hz =50,pf = 0.82 , eff = 0.8 , Vr =None,Ir =None):
        '''
            factory fr ac machine
        '''
        return cls(kw,Vs,Is,rpm ,hz,pf,eff)

class DCMachine:
    pass


# cmc_motor = ACMachine(5800,Vs=11000,Is=369,rpm=994,Vr=2107,Ir=1658,pf=0.85,eff=0.971)
# cmc_motor.Inertia = 576

# cmc_motor.R1 = 0.08435
# motor_params = cmc_motor.test_data(Vnl=11008.7,Inl=116.5,Pnl=76774,Freqnl=50,Vbr = 3583.3,Ibr = 564.4 ,Pbr = 509430 , Freqbr = 50)
# print(motor_params)
# # print(cmc_motor.R1)
# # print(cmc_motor.R2_d)
# # print(cmc_motor.X1)
# # print(cmc_motor.X2_d)
# # print(cmc_motor.Xm)
# cmc_motor.draw_torque_speed()
