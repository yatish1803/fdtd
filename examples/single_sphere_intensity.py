#!/usr/bin/env python
# coding: utf-8

# In[13]:


import os
import fdtd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


fdtd.set_backend("numpy")


# In[3]:

wavelength = 491e-9
refractive_index = 1.38/1.33

grid = fdtd.Grid(
    shape = (300, 500, 1), # 25um x 15um x 1 (grid_spacing) --> 2D FDTD
    grid_spacing = (wavelength/refractive_index)/10,
    permittivity = 1,
)

grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")


# In[4]:


simfolder = grid.save_simulation("Single_Sphere")  # initializing environment to save simulation data
print(simfolder)


# In[5]:


grid[50:250, 50, 0] = fdtd.LineSource(
    period = wavelength / (3e8), name="source"
)


# In[6]:


grid[50:250, 60:400, 0] = fdtd.BlockDetector(name="detector")


# In[7]:


x = y = np.linspace(-1,1,100)
X, Y = np.meshgrid(x, y)
circle_mask = X**2 + Y**2 < 1
permittivity = np.ones((100,100,1))
permittivity += circle_mask[:,:,None]*(refractive_index**2 - 1)
grid[100:200, 100:200, 0] = fdtd.Object(permittivity=permittivity, name="object")


# In[8]:


# from IPython.display import clear_output # only necessary in jupyter notebooks
# for i in range(0,640):
#     print(i)
#     grid.step()  # running simulation 1 timestep a time and animating
    # if i % 10 == 0:
    #     # saving frames during visualization
    #     grid.visualize(z=0, animate=True, index=i, save=False, folder=simfolder)
    #     plt.title(f"{i:3.0f}")
        # clear_output(wait=True) # only necessary in jupyter notebooks
grid.run(total_time=100)
# grid.save_data()  # saving detector readings
grid.visualize(z=0, show=True)
# visualize(grid,z=0, show=True)

# In[14]: globals().clear()


# df = np.load(os.path.join(simfolder, "detector_readings.npz"))
# dB_map_2D_(df["detector (E)"])
#
#
# def dB_map_2D_(block_det, choose_axis=2, interpolation="spline16"):
#     """
#     Displays detector readings from an 'fdtd.BlockDetector' in a decibel map spanning a 2D slice region inside the BlockDetector.
#     Compatible with continuous sources (not pulse).
#     Currently, only x-y 2D plot slices are accepted.
#
#     Parameter:-
#         block_det (numpy array): 5 axes numpy array (timestep, row, column, height, {x, y, z} parameter) created by 'fdtd.BlockDetector'.
#         (optional) choose_axis (int): Choose between {0, 1, 2} to display {x, y, z} data. Default 2 (-> z).
#         (optional) interpolation (string): Preferred 'matplotlib.pyplot.imshow' interpolation. Default "spline16".
#     """
#     if block_det is None:
#         raise ValueError(
#             "Function 'dBmap' requires a detector_readings object as parameter."
#         )
#     if len(block_det.shape) != 5:  # BlockDetector readings object have 5 axes
#         raise ValueError(
#             "Function 'dBmap' requires object of readings recorded by 'fdtd.BlockDetector'."
#         )
#
#     # TODO: convert all 2D slices (y-z, x-z plots) into x-y plot data structure
#
#     plt.ioff()
#     plt.close()
#     a = []  # array to store wave intensities
#     for i in tqdm(range(len(block_det[0]))):
#         a.append([])
#         for j in range(len(block_det[0][0])):
#             temp = [x[i][j][0][choose_axis] for x in block_det]
#             a[i].append(max(temp) - min(temp))
#
#     peakVal, minVal = max(map(max, a)), min(map(min, a))
#     print(
#         "Peak at:",
#         [
#             [[i, j] for j, y in enumerate(x) if y == peakVal]
#             for i, x in enumerate(a)
#             if peakVal in x
#         ],
#     )
#     #a = 10 * log10([[y / minVal for y in x] for x in a])
#     a = np.power([[y / minVal for y in x] for x in a],2)
#     plt.title("Intensity map in detector region")
#     plt.imshow(a, cmap="inferno")#, interpolation=interpolation)
#     cbar = plt.colorbar()
#     cbar.ax.set_ylabel("dB scale", rotation=270)
#     plt.show()




