# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:58:20 2019

@author: Sam Garcia (adapted by ludovic.spaeth)
Script for convolution in scalogram design 
"""

import numpy as np
from scipy.signal import resample
from scipy.fftpack import fft,ifft,fftshift,fftfreq


class Convolution():
    
    def __init__(self):
        print ('Convolution module loaded')
        
    def generate_wavelet_fourier(len_wavelet,
                                 f_start,
                                 f_stop,
                                 deltafreq,
                                 sampling_rate,
                                 f0,
                                 normalization):
        
        '''
        Computes the wavelet coefficients at all scales and makes corresponding Fourier transform
        When different signal scalograms are computed with the exact same coefficient
        this function can be excecuted once and the result is passed directly to compute_morlet_scalogram
        
        Output = wf : Fourier transform of the waverlet coefficients (after weighting), Fourier freq at first
        '''
        
        #Computes final map scales
        scales = f0/np.arange(f_start,f_stop,deltafreq)*sampling_rate
       
        #compute wavelet coeffs at all scales
        xi = np.arange(-len_wavelet/2.0,len_wavelet/2.0)
        xsd = xi[:,np.newaxis()] / scales
        wavelet_coefs = np.exp(complex(1j)*2.0*np.pi*f0*xsd)*np.exp(-np.power(xsd,2)/2.)
        
        weighting_function = lambda x: x**(-(1.0))
        wavelet_coefs = wavelet_coefs*weighting_function(scales[np.newaxis(),:])
        
        #Transform the wavelet into the Fourier domain 
        wf=fft(wavelet_coefs,axis=0)
        wf=wf.conj() #Used to be an error here
        
        
        return wf 
    
    
    def compute_morlet_scalogram(ana,
                                 f_start=5,
                                 f_stop=100,
                                 deltafreq=1,
                                 sampling_rate=200,
                                 t_start=-np.inf,
                                 t_stop=np.inf,
                                 f0=2.5,
                                 normalisation=0,
                                 wf=None):
        
        #Reduce the signal to the limits
        sig = ana.signal[(ana.t()>=t_start)&(ana.t()<=t_stop)]
        
        if sig.size>0:
            if wf is None:
                if ana.sampling_rate != sampling_rate:
                    sig = resample(sig,sig.size*sampling_rate/ana.sampling_rate)
                wf = Convolution.generate_wavelet_fourier(sig.size,max(f_start,deltafreq),min(f_stop,ana.sampling_rate/2.),deltafreq,sampling_rate,f0,normalisation)
            else:
                if sig.size != wf.shape[0]:
                    sig=resample(sig,wf.shape[0])
                    
            #Transform the signal in Fourier domain 
            sigf=fft(sig)
            
            #Convolve (mult. in Fourier space)
            wt_tmp = ifft(sigf[:,np.newaxis()]*wf,axis=0)
            
            #Shift output from ifft
            wt = fftshift(wt_tmp,axes=[0])
            
        else: 
            scales = f0/np.arange(f_start,f_stop,deltafreq)*sampling_rate
            wt = np.empty((0,scales.size),dtype='complex')
            
        return wt 
    
    def FFT(signal,sampling_rate,plot=True,freq_range=[0,200]):
        
        '''
        signal (array) : the signal
        sampling_rate (int or float) : signal sampling rate in Hz
        '''
        
        signal = np.asarray(signal)
        
        time_vector = np.arange(0,len(signal),1)/sampling_rate
        
        timewindow = signal.size
        period = 1./sampling_rate
        # Fourrier transform
        signal_fft = abs(fft(signal))    # abs to get real part only
        
        # get frequential domain
        signal_freq = fftfreq(timewindow,period)
        
        # Get real values from FFT and frequency domain
        signal_fft = signal_fft[0:len(signal_fft)//2]
        signal_freq = signal_freq[0:len(signal_freq)//2]
        
        if plot==True: 
            from matplotlib import pyplot as plt
        
            fig, ax = plt.subplots(2,1)
        
            #Plot the signal
            ax[0].set_title('signal')
            ax[0].plot(time_vector, signal)
            ax[0].set_xlabel('Time (s)'); ax[0].set_ylabel('Signal Amp')
            
            #Plot the spectrum
            ax[1].plot(signal_freq,signal_fft)
            ax[1].set_xlabel('Freq. range (Hz)'); ax[1].set_ylabel('Freq. Power')
            ax[1].set_xlim(freq_range[0],freq_range[1])
            plt.tight_layout()
            plt.show(); 
            
        return signal_fft, signal_freq
