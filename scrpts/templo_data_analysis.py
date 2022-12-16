from tkinter import N
from scipy import signal
from scipy.fft import fft, ifft, fftfreq, fftshift
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




class templo_trial:
    #force plate has 4 sensors
    #origin of the plate is in the centre ~Xcm below the plate (maybe 2cm)
    #Force plate is a Kistler
    
    fs = 100 #Hz
    T = 1/fs #s


    def __init__(self, file_location):
        self.file_location = file_location
        self.df = pd.read_csv(self.file_location,sep='\t',header=(0))
        self.N_samples = len(self.df)


    def sag_force_magnitudes(self):
        self.df['fzx'] = pow(pow(self.df.fx,2) + pow(self.df.fz,2), 0.5)
        return self.df['fzx']

    def cor_force_magnitudes(self):
        self.df['fzy'] = pow(pow(self.df.fy,2) + pow(self.df.fz,2), 0.5)
        return self.df['fzy']

    def trans_force_magnitudes(self):
        self.df['fxy'] = pow(pow(self.df.fy,2) + pow(self.df.fx,2), 0.5)
        return self.df['fxy']

    def sag_force_directions(self):
        self.df['0zx'] = np.degrees(np.arctan(self.df.fz / self.df.fx))
        d = self.df.loc[:,['0zx']]
        d.plot()
        plt.show()
        return self.df['0zx']

    def cor_force_directions(self):
        self.df['0zy'] = np.degrees(np.arctan(self.df.fz / self.df.fy))
        d = self.df.loc[:,['0zy']]
        d.plot()
        plt.show()
        return self.df['0zy']

    def trans_force_directions(self):
        self.df['0xy'] = np.degrees(np.arctan(self.df.fx / self.df.fy))
        d = self.df.loc[:,['0xy']]
        d.plot()
        plt.show()
        return self.df['0xy']
    
    def xyz_force_plot(self):
        forces = self.df.loc[:,['fx','fy','fz']]
        forces.plot()
        plt.show()

    def cor_sag_trans_force_plot(self):
        pass

    def cor_sag_trans_direction_plot(self):
        pass

    def filter_design(self, fs):
        N = 25
        Wn = (self.collection_freq/2) - 1
        sig = self.df.loc[:,['fz']]  
        sos = signal.butter(N, Wn, 'low', analog=False, output='sos', fs=fs)
        filtered = signal.sosfilt(sos, sig)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(sig)
        ax1.set_title('10 Hz and 20 Hz sinusoids')
        ax2.plot(filtered)
        ax2.set_title('After 15 Hz high-pass filter')
        plt.tight_layout()
        plt.show()

    def fast_fourier_transform(self, T):
        N = self.N_samples  
        y = self.df.loc[:,['fy']]   
        T = T

        yf = fft(y)
        xf = fftfreq(N, T)
        xf = fftshift(xf)
        yplot = fftshift(yf)
        plt.plot(xf, 1.0/N * np.abs(yplot))
        plt.grid()
        plt.show()




myfile = 'scrpts\\J-20220927-093421.txt'
trial_1 = templo_trial(myfile)

trial_1.filter_design()