# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 17:02:07 2017

@author: owner
"""
# This code finds the data files in the models folder with the given names and 
# interpolates the radius at a desired age, then plots the mass/radius relationship
# for the different planet masses
#matplotlib inline
import mesa_reader as ms
from glob import glob
from scipy import interpolate
import matplotlib.pyplot as plt
import numpy as np

#Make sure these are the right values!
Msol_to_MJup = 0.0009543
Rsol_to_RJup = 0.10045

PlanetMasses = [0.1,0.3,0.5,1.0,3.0,5.0,10.0]

################## This part was just a test
dr = '/Users/owner/mesa7184work/star/test_suite/make_planets/models/Mpinit_0.1_MJup_10.0_ME/LOGS_Mpinit_0.1_MJup_10.0_ME/'
ls = glob(dr + '/history.data')
filename = ls[-1]
mod = ms.MesaData(filename)
print(mod.data('star_mass')[0])
#plt.plot(mod.data('star_age'), mod.data('radius'))
##############

#Make an implicit function that provide radius when you give an age
radius_interp = interpolate.interp1d(mod.data('star_age'), mod.data('radius'))
age = 5e9
#5 Gyrs
print(radius_interp(age))

#Iterate through all the masses
#Make a list of all the LOG file names
LOG_file_list = np.array([])
for ii in PlanetMasses:
    overall_directory = '/Users/owner/mesa7184work/star/test_suite/make_planets/models/'
    LOG_file_list1 = glob(overall_directory + 'Mpinit_'+str(ii)+'_MJup_10.0_ME/*/history.data')
    print(LOG_file_list1[0:1])
    LOG_file_list = np.append(LOG_file_list, LOG_file_list1)

#For each history.data file, add the planet's mass to a mass array.
masses = np.array([])
radii = np.array([])

desired_age = 5e9
for i in range(len(LOG_file_list)):
    mod = ms.MesaData(LOG_file_list[i])
    
    if(max(mod.data('star_age')) >= desired_age):
        
        masses = np.append(masses, mod.data('star_mass')[0]/Msol_to_MJup)
        radius_interp = interpolate.interp1d(mod.data('star_age'), mod.data('radius'))
        radii = np.append(radii, radius_interp(desired_age)/Rsol_to_RJup)

plt.scatter(masses, radii)