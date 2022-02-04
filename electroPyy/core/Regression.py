# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 14:23:37 2019

@author: ludovic.spaeth
"""

class Regression():

    def LinReg(x,y,conf=0.95,printparams=True,plot=True, ax=False):
        '''
        This code computes regression on synaptic charges measured in uncaging experiments
        Model (linear fit) is segregated between inputs depending on their location 
        inspired by : http://apmonitor.com/che263/index.php/Main/PythonRegressionStatistics
        
        x,y (1D arrays) = the x & y data 
        
        conf (float) = confidence treshold (alpha = 1-conf)
        
        printparams (bool) : if True, will display fit parameters and R value in the console
        
        plot (bool) : if True, will plot the result of the linear reg 
        
        ax, if False: creates a new figure or fill with corresponding subplot name 
        
        Returns : 
            
            px (array) : x-axis for plot, based on min/max values of x
            
            nom (array) : y-values of linear model (nomial values of y)
            
            lpb, upb (arrays) : lower and upper prediction bands 
            
            r2 = squared correlation coefficient 
        
        '''
        import numpy as np 
        from scipy.optimize import curve_fit
        import matplotlib.pyplot as plt
        from scipy import stats
        import uncertainties as unc
        import matplotlib
        from sklearn import metrics
        matplotlib.rcParams['pdf.fonttype'] = 42
        
        #Pip install uncertainties if needed 
        try :
            import uncertainties.unumpy as unp
            
        except : 
            import pip
            pip.main(['install','uncertainties'])
            import uncertainties.unumpy as unp 
        
        
        n = len(y)
        
        def f(x, a, b):
            return a * x + b
        
        popt, pcov = curve_fit(f, x, y)
        
        # retrieve parameter values
        a = popt[0]
        b = popt[1]
    
        # compute r^2
        r2 = 1.0-(sum((y-f(x,a,b))**2)/((n-1.0)*np.var(y,ddof=1)))

        
        # calculate parameter confidence interval
        a,b = unc.correlated_values(popt, pcov)

        
        if printparams ==True:
            print('Optimal Values')
            print('a: ' + str(a))
            print('b: ' + str(b))
            print('R^2: ' + str(r2))
            print('Uncertainty')
            print('a: ' + str(a))
            print('b: ' + str(b))
            
       
        # calculate regression confidence interval
        px = np.linspace(np.min(x),np.max(x),n)
        py = a*px+b
        nom = unp.nominal_values(py)
        std = unp.std_devs(py)
        
        def predband(x, xd, yd, p, func, conf=conf):
            '''
            x = requested points
            xd = x data
            yd = y data
            p = parameters
            func = function name
            '''
            alpha = 1.0 - conf    # significance
            N = xd.size          # data sample size
            var_n = len(p)  # number of parameters
            # Quantile of Student's t distribution for p=(1-alpha/2)
            q = stats.t.ppf(1.0 - alpha / 2.0, N - var_n)
            # Stdev of an individual measurement
            se = np.sqrt(1. / (N - var_n) * \
                         np.sum((yd - func(xd, *p)) ** 2))
            # Auxiliary definitions
            sx = (x - xd.mean()) ** 2
            sxd = np.sum((xd - xd.mean()) ** 2)
            # Predicted values (best-fit model)
            yp = func(x, *p)
            # Prediction band
            dy = q * se * np.sqrt(1.0+ (1.0/N) + (sx/sxd))
            # Upper & lower prediction bands.
            lpb, upb = yp - dy, yp + dy
            return lpb, upb
        
        lpb, upb = predband(px, x, y, popt, f, conf=conf)
            
        if plot == True:
            
            if ax=False:
            
                # plot data
                plt.figure()
                plt.scatter(x, y, s=20, label='Data')
                # plot the regression
                plt.plot(px, nom, c='orange', label='y=a x + b',linewidth=2)

                # uncertainty lines (95% confidence)
                plt.plot(px, nom - 1.96 * std, c='0.5',linestyle='--',\
                         label='95% Confidence Region')
                plt.plot(px, nom + 1.96 * std, c='0.5',linestyle='--')
                # prediction band (95% confidence)
                plt.plot(px, lpb, color='0.5',label='95% Prediction Band',linestyle=':')
                plt.plot(px, upb, color='0.5',linestyle=':')
                plt.ylabel('Y')
                plt.xlabel('X')
                plt.legend(loc='best')
                plt.title('Linear Reg : R$^2$={}'.format(round(r2,2)))
                plt.show()
                
            else:
            
                # plot data
                ax.figure()
                ax.scatter(x, y, s=20, label='Data')
                # plot the regression
                ax.plot(px, nom, c='orange', label='y=a x + b',linewidth=2)

                # uncertainty lines (95% confidence)
                ax.plot(px, nom - 1.96 * std, c='0.5',linestyle='--',\
                         label='95% Confidence Region')
                ax.plot(px, nom + 1.96 * std, c='0.5',linestyle='--')
                # prediction band (95% confidence)
                ax.plot(px, lpb, color='0.5',label='95% Prediction Band',linestyle=':')
                ax.plot(px, upb, color='0.5',linestyle=':')
                ax.legend(loc='best')
                ax.set_title('Linear Reg : R$^2$={}'.format(round(r2,2)))
            
        return px,nom,lpb,upb,r2,std
        
        
#if __name__ == '__main__':
#    
#    import numpy as np 
#
#    x = np.array([10,2,5,6,9,8,25,20,12,52,34,18,25,6,17])
#    y = np.array([10,2,6,7,9,9,35,27,14,60,37,19,26,10,19])
#    
#    px, nom, lpb, upb, r2, std = Regression.LinReg(x,y)
#    
#    '''
#    #First compute the residuals
#    residuals = nom-y
#    
#    #Then the mean squared error
#    mse = ((y-nom)**2).mean(axis=0)
#    
#    #Now the standard residuals 
#    std_residuals = residuals/np.sqrt(mse)
#    
#    
#    
#    '''
    
