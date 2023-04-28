# import os
import fdtd
import numpy as np
# import matplotlib.pyplot as plt

grid = fdtd.Grid(shape=(260, 15.5e-6, 1), grid_spacing=77.5e-9)
# x boundaries
grid[0:10, :, :] = fdtd.PML(name="pml_xlow")
grid[-10:, :, :] = fdtd.PML(name="pml_xhigh")
# y boundaries
grid[:, 0:10, :] = fdtd.PML(name="pml_ylow")
grid[:, -10:, :] = fdtd.PML(name="pml_yhigh")
# simfolder = grid.save_simulation("Lenses")  # initializing environment to save simulation data
# print(simfolder)

x, y = np.arange(-200, 200, 1), np.arange(190, 200, 1)
X, Y = np.meshgrid(x, y)
f = 100
lens_mask = X ** 2 + Y ** 2 <= (2*f) ** 2
for j, col in enumerate(lens_mask.T):
    for i, val in enumerate(np.flip(col)):
        if val:
            grid[30 + i : 50 - i, j - 100 : j - 99, 0] = fdtd.Object(permittivity=1.5 ** 2, name=str(i) + "," + str(j))
            break

grid[15, 50:150, 0] = fdtd.LineSource(period=1550e-9 / (3e8), name="source")

grid[80:200, 80:120, 0] = fdtd.BlockDetector(name="detector")

# with open(os.path.join(simfolder, "grid.txt"), "w") as f:
#     f.write(str(grid))
#     wavelength = 3e8/grid.source.frequency
#     wavelengthUnits = wavelength/grid.grid_spacing
#     GD = np.array([grid.x, grid.y, grid.z])
#     gridRange = [np.arange(x/grid.grid_spacing) for x in GD]
#     objectRange = np.array([[gridRange[0][x.x], gridRange[1][x.y], gridRange[2][x.z]] for x in grid.objects], dtype=object).T
#     f.write("\n\nGrid details (in wavelength scale):")
#     f.write("\n\tGrid dimensions: ")
#     f.write(str(GD/wavelength))
#     f.write("\n\tSource dimensions: ")
#     f.write(str(np.array([grid.source.x[-1] - grid.source.x[0] + 1, grid.source.y[-1] - grid.source.y[0] + 1, grid.source.z[-1] - grid.source.z[0] + 1])/wavelengthUnits))
#     f.write("\n\tObject dimensions: ")
#     f.write(str([(max(map(max, x)) - min(map(min, x)) + 1)/wavelengthUnits for x in objectRange]))

# for i in range(400):
#     grid.step()  # running simulation 1 timestep a time and animating
#     if i % 10 == 0:
#         # saving frames during visualization
#         grid.visualize(z=0, animate=True, index=i, save=True, folder=simfolder)
#         plt.title(f"{i:3.0f}")
#
# grid.save_data()  # saving detector readings

grid.run(total_time=400)

grid.visualize(z=0, show=True)