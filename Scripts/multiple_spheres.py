import os
import new_func
import fdtd
import numpy as np
# matplotlib.use('TkAgg',force=True)
import matplotlib.pyplot as plt
# print("Switched to:",matplotlib.get_backend())
save = True
sx = 200
sz = 300
sy = 256

fdtd.set_backend("numpy")

# In[3]:

wavelength_freespace = 491e-9
vel_light: float = 299_792_458.0  # [m/s] speed of light
n_m = 1.42
n_s = 1.33
wavelength = wavelength_freespace / n_s
wavelength_px = 10
grid = fdtd.Grid(
    shape=(sx + 40, sz + 40, 1),  # 25um x 15um x 1 (grid_spacing) --> 2D FDTD
    grid_spacing=(wavelength_freespace / n_m) / wavelength_px,  # from Nyquist Theorem
    permittivity=n_s ** 2,
)
grid_spacing = (wavelength_freespace / n_m) / wavelength_px
print(grid_spacing)

b2pml = 10
grid[0:b2pml, :, :] = fdtd.PML(name="pml_xlow")
grid[-b2pml:, :, :] = fdtd.PML(name="pml_xhigh")
grid[:, 0:b2pml, :] = fdtd.PML(name="pml_ylow")
grid[:, -b2pml:, :] = fdtd.PML(name="pml_yhigh")

pml2s_z_left = 0
s2d_left = 10
pml2d = 10
grid[b2pml + pml2d:b2pml + pml2d + sx, b2pml + pml2s_z_left + s2d_left:b2pml + pml2s_z_left + s2d_left + sz, 0] = fdtd.BlockDetector(name="detector")

time_step = wavelength_freespace / vel_light  # or grid_spacing*n_m/vel_light
num_time_steps = int(((s2d_left + sz) / wavelength_px) * wavelength_px)
print(num_time_steps)
b2s = 0
grid[b2s:b2pml + pml2d + sx + pml2d + b2pml - b2s, 10, 0] = fdtd.LineSource(
    period=time_step, name="source"
)


Single_Sphere = True
#################### for multiple spheres #################
# ######################## make simulation volume ############

# grid[object_x_ini:object_x_fin, b2pml + pml2s_z_left + s2d_left + gap_y:b2pml + pml2s_z_left + s2d_left + gap_y + permittivity.shape[1], 0] = fdtd.Object(permittivity=permittivity, name="object")
##################################################################
################## for single sphere #########################
if Single_Sphere:
    if save:
        simfolder = grid.save_simulation("Single_Sphere")  # initializing environment to save simulation data
        print(simfolder)
    else:
        simfolder = None
    diameter_sphere_um = 3.74
    diameter_sphere = int(diameter_sphere_um*1e-6 / grid_spacing)
    print(f"diameter_sphere={diameter_sphere}")
    x = y = np.linspace(-1, 1, diameter_sphere)
    X, Y = np.meshgrid(x, y)
    circle_mask = X**2 + Y**2 < 1
    permittivity = np.ones((diameter_sphere, diameter_sphere, 1)) * n_s ** 2
    permittivity += circle_mask[:, :, None] * (n_m ** 2 - n_s ** 2)

    object_x_ini = int(b2pml + pml2d + sx/2 - permittivity.shape[0]/2)
    object_x_fin = int(object_x_ini + permittivity.shape[0])
else:
    if save:
        simfolder = grid.save_simulation("Multi_Sphere")  # initializing environment to save simulation data
        print(simfolder)
    else:
        simfolder = None
    dim_x = 150
    dim_z = 270
    dim_y = 150

    volume_fraction = 0.15
    diameter_spheres_um = 1.0
    diameter_spheres = int(diameter_spheres_um * 1e-6 / grid_spacing)
    print(diameter_spheres)
    volume = new_func.generate_Volume_Binary(diameter_spheres, volume_fraction, dim_x, dim_z, dim_y, folder=simfolder)
    ################################################################
    object_x_ini = int(b2pml + pml2d + sx / 2 - dim_x / 2)
    object_x_fin = int(object_x_ini + dim_x)
    gap_y = 10
    slice2D = volume[:, :, dim_y // 2]
    permittivity = np.ones((dim_x, dim_z, 1)) * n_s ** 2
    permittivity += slice2D[:, :, None] * (n_m ** 2 - n_s ** 2)

gap_z = 10
grid[object_x_ini:object_x_fin, b2pml + pml2s_z_left + s2d_left + gap_z:b2pml + pml2s_z_left + s2d_left + gap_z + permittivity.shape[1], 0] \
= fdtd.Object(permittivity=permittivity, name="object")
####################################################################
num_bounces = 4
grid.run(total_time=int(num_time_steps*num_bounces))  # Simulation time should allow for ~5 bounces
grid.save_data()  # saving detector readings
grid.visualize(z=0, show=True, folder=simfolder)

# globals().clear()

# permittivity_det_zone = np.ones((sx+1, sy+1)) * n_s ** 2
# permittivity_det_zone[gap_x:gap_x+permittivity.shape[0], gap_y:gap_y+permittivity.shape[1]] = np.squeeze(permittivity)

simfolder = "D:/Yatish/Python/fdtd/fdtd_output/fdtd_output_2023-6-21-15-25-22 (Single_Sphere)"

df = np.load(os.path.join(simfolder, "detector_readings.npz"))
fdtd.dB_map_2D(df["detector (E)"], folder=simfolder)

fdtd.intensity_map(df["detector (E)"], df["detector (H)"], folder=simfolder)

