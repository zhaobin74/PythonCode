"""
create_passtracers.py
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


import os
import glob
import numpy as np

from scipy import interpolate
import sys
sys.path.insert(1,'/projects/v45/python')
import netCDF4 as nc

def cpt():

    vals=nc.Dataset('/short/v45/pas561/mom/input/mom01v2/ocean_temp_salt.res.nc','r')
    zaxis_1 = vals.variables['zaxis_1'][:]
    xaxis_1 = vals.variables['xaxis_1'][:] 
    yaxis_1 = vals.variables['yaxis_1'][:] 
    temp = vals.variables['temp'][:]
    vals.close()

    km=temp.shape[1]
    jm=temp.shape[2]
    im=temp.shape[3]
    print 'km,jm,im',km,jm,im

    data_file = '/g/data1/v45/mom01_comparison/KDS75_wind/ocean_month.150.ncra.diff.nc'
    input2 = nc.Dataset(data_file, 'r')
    tx = input2.variables['tau_x'][:]

    print 'shape tx=\n ',tx.shape
    
    #create masks
    msk = np.ones(np.shape(temp))

    for k in xrange(km):
        for j in xrange(jm):
            for i in xrange(im):
                if tx.data[0,j,i]>0.075:
                    msk[0,k,j,i] = 1
                else:
                    pass


    save_field(xaxis_1,yaxis_1,zaxis_1,msk,'ocean_passive.res.nc','passive_patch_1')

def save_field(x, y, z, field,name,var):

    field_nc = nc.Dataset(name,'w')

    nt,nz, ny, nx = field.shape
    print 'nz,ny,nx',nz,ny,nx
    field_nc.createDimension('ZT', nz)
    field_nc.createDimension('LAT', ny)
    field_nc.createDimension('LON', nx)

    z_nc = field_nc.createVariable('ZT', 'f8', ('ZT',))
    z_nc[:] = z
    z_nc.long_name = 'depth'
    z_nc.units = 'm'
    z_nc.axis = 'Cartesian Z'

    lat_nc = field_nc.createVariable('LAT', 'f8', ('LAT',))
    lat_nc[:] = y
    lat_nc.long_name = 'Mercator Gridded Latitude'
    lat_nc.units = 'degrees north'
    lat_nc.axis = 'Cartesian Y'

    lon_nc = field_nc.createVariable('LON', 'f8', ('LON',))
    lon_nc[:] = x
    lon_nc.long_name = 'Mercator Gridded Longitude'
    lon_nc.units = 'degrees east'
    lon_nc.axis = 'Cartesian X'

    temp_nc = field_nc.createVariable(var, 'f8', ('ZT', 'LAT', 'LON'))
    temp_nc[:] = field

    field_nc.close()



    #output_file = 'ocean_passive.res.nc'
    #print "Writing output file ",output_file
    ## Output to NetCDF file
    #output = Dataset(output_file, 'w', format='NETCDF4')

    #output.createDimension('GRID_X_T', jm)
    #y_var = output.createVariable('GRID_X_T', 'f8', ('GRID_X_T',))
    #y_var.units = 'degree_east'
    
    #y_var[:] = yt_ocean[:]

    #output.createDimension('xt_ocean', im)
    #x_var = output.createVariable('xt_ocean', 'f8', ('xt_ocean',))
    #x_var.units = 'meters'
    #x_var[:] = xt_ocean[:]

    #dx_var = output.createVariable('dxt', 'f8', ('yt_ocean', 'xt_ocean',))
    #dx_var.units = 'm'
    #dx_var[:,:] = dxt
    
    #output.close()

    
    if __name__ == "__main":
       cpt()
        
     

   



