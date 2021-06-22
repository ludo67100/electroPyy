# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:34:18 2019

@author: Ludovic.SPAETH
"""

class Filters():
    
    def __init__(self): 
        
        filt = self.filt

    def bandpass(signal,axis=0,freq_low=50,freq_high=1000,N=8,filtertype='butter',sample_rate=20000):
        
        '''
        compute bandpass filtering on numpy array in accordance with Nyquist law
        
        INPUTS: 
            signal (numpy array): the signal to filter
            axis (int): axis for filtering (if nd array)
            freq_low (float): high pass threshold
            freq_high (float): low pass threshold
            N (int): filter magnitude
            samplte_rate (int): signal sampling rate (in Hz)
            
        OUTPUTS:
            sigs_filtered (numpy array): the filtered signal
        '''
        import scipy.signal
        Wn = [ freq_low/(sample_rate/2), freq_high/(sample_rate/2)]
        sos_coeff = scipy.signal.iirfilter(N, Wn, btype='band', ftype=filtertype, output='sos')
        bp_filtered = scipy.signal.sosfiltfilt(sos_coeff, signal,axis=axis)
        
        return bp_filtered

    
    def lowpass(signal, axis=0,freq=1000,N=8,filtertype='butter',sample_rate=20000):
        
        import scipy.signal
        Wn = freq/(sample_rate/2)
        sos_coeff = scipy.signal.iirfilter(N, Wn, btype='lowpass', ftype=filtertype, output='sos')
        low_filtered = scipy.signal.sosfiltfilt(sos_coeff, signal,axis=axis)
        
        return low_filtered
    
    def highpass(signal, axis=0,freq=1000,N=8,filtertype='butter',sample_rate=20000):
        
        import scipy.signal
        Wn = freq/(sample_rate/2)
        sos_coeff = scipy.signal.iirfilter(N, Wn, btype='highpass', ftype=filtertype, output='sos')
        high_filtered = scipy.signal.sosfiltfilt(sos_coeff, signal,axis=axis)
        
        return high_filtered

##Test (should be commented)
#    
#if __name__ == '__main__': 
#    
#    from neo.rawio import WinWcpRawIO as win 
#    import numpy as np
#
#    file = 'U:/RAW DATA/Cuffed Mice/08-06-2017/170608_008.wcp'
#
#    reader = win(file)
#    reader.parse_header() #HEADER NEEDS TO BE PARSED !!!!!!!!!!!!!!!
#    nb_sweeps = reader.header['nb_segment'][0]
#    sampling_rate = reader.get_signal_sampling_rate()
#
#    raw_sigs = reader.get_analogsignal_chunk(block_index=0, seg_index=10, 
#                                             i_start=0, 
#                                             i_stop=-1,
#                                             channel_indexes=[0])
#    
#    
#    time_vector = np.arange(0,len(raw_sigs),1)*1./sampling_rate
#
#    
#    from matplotlib import pyplot as plt
#    
#    plt.figure()
#    plt.plot(time_vector, raw_sigs,color='blue',label='raw signal')
#    
#    bp_signal = Filter.bandpass(raw_sigs,axis=0,freq_low=1,freq_high=700,N=8,sample_rate=sampling_rate)
#    lp_signal = Filter.lowpass(raw_sigs,axis=0,freq=100,sample_rate=sampling_rate)
#    hp_signal = Filter.lowpass(raw_sigs,axis=0,freq=1000,sample_rate=sampling_rate)
#    
#    plt.plot(time_vector, bp_signal,color='orange',label='band pass')
#    plt.plot(time_vector, lp_signal,color='red',label='low pass')    
#    plt.plot(time_vector, hp_signal,color='green',label='high pass')    
#    plt.legend(loc='best')    

    
    
    
