from __future__ import division

from netCDF4 import Dataset
import numpy as np

from viscous.utilities import find_nearest, scale_lon

CONSTANTS = ["days_in_norm_year", "grav", "omega", "radius", "cp_sw", "sound", "vonkar",
"cp_air", "rho_air", "rho_sw", "rho_fw", "stefan_boltzmann", "latent_heat_vapor",
"latent_heat_fusion", "ocn_ref_salinity", "sea_ice_salinity", "T0_Kelvin", "salt_to_ppt",
"ppt_to_salt", "mass_to_Sv", "head_to_PW", "salt_to_Svppt", "salt_to_mmday", "momentum_factor",
"hflux_factor", "salinity_factor", "sflux_factor", "nsurface_t", "nsurface_u"]

def read_u_coords(path,return_dx=False):
    full_data = Dataset(path,"r")
    lon,lat = np.array(full_data.variables["ULONG"][:]), np.array(full_data.variables["ULAT"][:])
    lon = scale_lon(lon)
    depth = np.array(full_data.variables["z_t"][:]) / 1E2 # cm -> m
    dx = np.array(full_data.variables["DXU"][:])/1E2 # cm -> m
    dy = np.array(full_data.variables["DYU"][:])/1E2 # cm -> m
    dz = np.array(full_data.variables["dz"][:])/1E2 # cm -> m
    full_data.close()
    if return_dx:
        return lon,lat,depth,dx,dy,dz
    else:
        return lon,lat,depth

def read_t_coords(path,return_dx=False):
    full_data = Dataset(path,"r")
    lon,lat = np.array(full_data.variables["TLONG"][:]), np.array(full_data.variables["TLAT"][:])
    lon = scale_lon(lon)
    depth = np.array(full_data.variables["z_t"][:]) / 1E2 # cm -> m
    dx = np.array(full_data.variables["DXT"][:])/1E2 # cm -> m
    dy = np.array(full_data.variables["DYT"][:])/1E2 # cm -> m
    dz = np.array(full_data.variables["dz"][:])/1E2 # cm -> m
    full_data.close()
    if return_dx:
        return lon,lat,depth,dx,dy,dz
    else:
        return lon,lat,depth

def read_density(path):
    full_data = Dataset(path,"r")
    rho = np.array(full_data.variables["RHO"][0,...]) / 1E3 * 1E2**3 # g/cm^3 -> kg/m^3
    full_data.close()
    return rho

def read_potential_density(path):
    full_data = Dataset(path,"r")
    pd = np.array(full_data.variables["PD"][0,...]) / 1E3 * 1E2**3 # g/cm^3 -> kg/m^3
    full_data.close()
    return pd

def read_velocity(path):
    full_data = Dataset(path,"r")
    uvel = np.array(full_data.variables["UVEL"][0,...])/1E2 # cm/s -> m/s
    vvel = np.array(full_data.variables["VVEL"][0,...])/1E2 # cm/s -> m/s
    wvel = np.array(full_data.variables["WVEL"][0,...])/1E2 # cm/s -> m/s
    full_data.close()
    return uvel, vvel, wvel

def read_viscosity(path,target_depth=None,depth_data=None):
    visc_data = Dataset(path,"r")
    variables = []
    for val in visc_data.variables.values():
        variables.append(np.array(val))

    F_PARA = variables[0]/1E2**2 # cm^2/s -> m^2/s
    F_PERP = variables[1]/1E2**2
    visc_data.close()

    if target_depth is None:
        return F_PARA, F_PERP
    else:
        if depth_data is None:
            raise ValueError("Specify depth_data keyword when using target_depth")
        z_i = find_nearest(depth_data,target_depth)
        return F_PARA[z_i,:,:], F_PERP[z_i,:,:]

def read_moc(path):
    full_data = Dataset(path,"r")
    moc = np.array(full_data.variables["MOC"][0,...])
    lat = np.array(full_data.variables["lat_aux_grid"][:])
    depth = np.array(full_data.variables["moc_z"][:]) / 1E2 # cm -> m
    comp = full_data.variables["moc_components"][:]
    region = full_data.variables["transport_regions"][:]
    full_data.close()
    comp_cat = ["".join(list(string.astype(str))) for string in comp]
    region_cat = ["".join(list(string.astype(str))) for string in region]
    return moc, lat, depth, comp_cat, region_cat

def read_bsf(path):
    full_data = Dataset(path,"r")
    bsf = np.array(full_data.variables["BSF"][0,...])
    full_data.close()
    return bsf

def read_temperature(path):
    full_data = Dataset(path,"r")
    temp = np.array(full_data.variables["TEMP"][0,...])
    full_data.close()
    return temp

def read_density_gradient(path):
    full_data = Dataset(path,"r")
    q = np.array(full_data.variables["Q"][0,...])/1E3*1E2**4 # g/cm^4 -> kg/m^4
    full_data.close()
    return q

def read_vorticity(path):
    full_data = Dataset(path,"r")
    pv = np.array(full_data.variables["PV"][0,...])*1E2 # 1/s/cm -> 1/s/m
    full_data.close()
    return pv

def read_windstress(path):
    full_data = Dataset(path,"r")
    taux = np.array(full_data.variables["TAUX"][0,...]) / (1E5 * 1E-2**2) # dyn/cm^2 -> N/m^2
    tauy = np.array(full_data.variables["TAUY"][0,...]) / (1E5 * 1E-2**2) # dyn/cm^2 -> N/m^2
    full_data.close()
    return taux, tauy

def read_constants(path):
    full_data = Dataset(path,"r")
    constants = {key: full_data.variables[key][0] for key in full_data.variables.keys() if key in CONSTANTS}
    full_data.close()
    return constants

def read_region_mask(path):
    full_data = Dataset(path,"r")
    region_mask = full_data.variables["REGION_MASK"][:]
    full_data.close()
    regions = ['Global', 'Atlantic', 'Pacific', 'Indo-Pacific']
    regmask = np.ones(region_mask.shape, dict(names=regions, formats=[bool]*len(regions)))
    regmask['Pacific'] = (region_mask == 2)
    regmask['Atlantic'] = (region_mask >= 6) & (region_mask != 7)
    regmask['Indo-Pacific'] = (region_mask >= 2) & (region_mask <= 3)
    return regmask
