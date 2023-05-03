import numpy as np
import matplotlib.pyplot as plt
import os
from mayavi import mlab


def generate_sphere_positions(volume, fraction, diameter_px, dim_x, dim_z, dim_y):
    positions = []
    num_spheres = int(fraction * np.prod(volume.shape) / ((4/3) * np.pi * ((diameter_px/2)**3)))
    print(f"{num_spheres} spheres of diameter {diameter_px} occupy {fraction:.2f} of the {dim_x}x{dim_z}x{dim_y} volume")

    while len(positions) < num_spheres:
        # generate a random position within the bounds of the 3D volume
        x = np.random.randint(diameter_px, dim_x-diameter_px)
        z = np.random.randint(diameter_px, dim_z-diameter_px)
        y = np.random.randint(diameter_px, dim_y-diameter_px)
        pos = np.array([x, z, y])

        # check if the sphere overlaps with any previously placed spheres
        overlapping = False
        for p in positions:
            dist = np.linalg.norm(pos - p)
            if dist < diameter_px:
                overlapping = True
                break

        # if the sphere does not overlap, add its position to the list
        if not overlapping:
            positions.append(pos)

    return positions


def place_spheres_in_volume(volume, positions, diameter_px):
    for pos in positions:
        x, z, y = pos
        # place the sphere in the 3D volume
        for i in range(-diameter_px//2, diameter_px//2 + 1):
            for j in range(-diameter_px//2, diameter_px//2 + 1):
                for k in range(-diameter_px//2, diameter_px//2 + 1):
                    if np.linalg.norm(np.array([i, j, k])) <= diameter_px//2:
                        volume[x + i, z + j, y + k] = 1

    return volume


def generate_Volume_Binary(diameter_px, volume_fraction, dim_x, dim_z, dim_y, folder=None):

    # create an empty 3D numpy array
    volume = np.zeros((dim_x, dim_z, dim_y), dtype=int)

    # generate positions for N non-overlapping spheres
    positions = generate_sphere_positions(volume, volume_fraction, diameter_px, dim_x, dim_z, dim_y)

    # place the spheres in the 3D volume
    volume = place_spheres_in_volume(volume, positions, diameter_px)
    print(volume.shape)

    # # display the 3D volume with the spheres
    # mlab.figure(bgcolor=(0, 0, 0), size=(800, 800))
    # mlab.contour3d(volume, contours=[0.5], transparent=True)
    # mlab.show()

    # take a slice of the volume along the z-axis
    slice2D = volume[:, :, dim_y // 2]
    print(slice2D.shape)

    # display the slice using matplotlib
    plt.imshow(slice2D, cmap='gray')

    if folder is not None:
        my_file = 'Object_2D_slice.png'
        plt.savefig(os.path.join(folder, my_file))

    plt.show()

    return volume
