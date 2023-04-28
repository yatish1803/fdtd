import new_func
import fdtd
import numpy as np
# matplotlib.use('TkAgg',force=True)
import matplotlib.pyplot as plt

# print("Switched to:",matplotlib.get_backend())
# from mayavi import mlab

sx = 256
sy = 512
sz = 512

dim_x = 100
dim_y = 100
dim_z = 100

# create an empty 3D numpy array
volume = np.zeros((dim_x, dim_y, dim_z), dtype=int)

# generate positions for N non-overlapping spheres
volume_fraction = 0.8
diameter_spheres = 16

positions = new_func.generate_sphere_positions(volume, volume_fraction, diameter_spheres, dim_x, dim_y, dim_z)

# place the spheres in the 3D volume
volume = new_func.place_spheres_in_volume(volume, positions, diameter_spheres)

# # display the 3D volume with the spheres
# mlab.figure(bgcolor=(0, 0, 0), size=(800, 800))
# mlab.contour3d(volume, contours=[0.5], transparent=True)
# mlab.show()

# take a slice of the volume along the z-axis
slice2D = volume[:, dim_y // 2, :]

# display the slice using matplotlib
plt.imshow(slice2D, cmap='gray')
plt.show()

################################################################################

fdtd.set_backend("numpy")

# In[3]:

wavelength = 491e-9
n_m = 1.38
n_s = 1.33

factor = 10
grid = fdtd.Grid(
    shape=(sx+40, sy+30, 1),  # 25um x 15um x 1 (grid_spacing) --> 2D FDTD
    grid_spacing=(wavelength / n_m) / factor,
    permittivity=n_s ** 2,
)

grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")

# simfolder = grid.save_simulation("Single_Sphere")  # initializing environment to save simulation data
# print(simfolder)

grid[0:sx+40, 10, 0] = fdtd.LineSource(
    period=wavelength / 3e8, name="source"
)

grid[20:sx+20, 10:sy+10, 0] = fdtd.BlockDetector(name="detector")

# x = y = np.linspace(-1, 1, 100)
# X, Y = np.meshgrid(x, y)
# circle_mask = X**2 + Y**2 < 1
permittivity = np.ones((100, 100, 1)) * n_s ** 2
permittivity += slice2D[:, :, None] * (n_m ** 2 - n_s ** 2)
grid[100:200, 100:200, 0] = fdtd.Object(permittivity=permittivity, name="object")

grid.run(total_time=3)
# grid.save_data()  # saving detector readings
grid.visualize(z=0, show=True)
# plt.show()
# globals().clear()

# df = np.load(os.path.join(simfolder, "detector_readings.npz"))
# fdtd.intensity_map_2D(df["detector (E)"])
