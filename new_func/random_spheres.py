import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab


def generate_sphere_positions(volume, fraction, diameter_px, sx, sy, sz):
    positions = []
    num_spheres = int(np.round(fraction * np.prod(volume.shape) / ((4/3) * np.pi * (diameter_px**3))))
    print(f"{num_spheres} spheres of diameter {diameter_px} occupy {fraction:.2f} of the {sx}x{sy}x{sz} volume")

    while len(positions) < num_spheres:
        # generate a random position within the bounds of the 3D volume
        x = np.random.randint(diameter_px, sx-diameter_px)
        y = np.random.randint(diameter_px, sy-diameter_px)
        z = np.random.randint(diameter_px, sz-diameter_px)
        pos = np.array([x, y, z])

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
        x, y, z = pos
        # place the sphere in the 3D volume
        for i in range(-diameter_px//2, diameter_px//2 + 1):
            for j in range(-diameter_px//2, diameter_px//2 + 1):
                for k in range(-diameter_px//2, diameter_px//2 + 1):
                    if np.linalg.norm(np.array([i, j, k])) <= diameter_px//2:
                        volume[x + i, y + j, z + k] = 1

    return volume


def generate_Volume_Binary(diameter_spheres, volume_fraction, dim_x, dim_y, dim_z):

    # create an empty 3D numpy array
    volume = np.zeros((dim_x, dim_y, dim_z), dtype=int)

    # generate positions for N non-overlapping spheres
    positions = generate_sphere_positions(volume, volume_fraction, diameter_spheres, dim_x, dim_y, dim_z)

    # place the spheres in the 3D volume
    volume = place_spheres_in_volume(volume, positions, diameter_spheres)

    # # display the 3D volume with the spheres
    # mlab.figure(bgcolor=(0, 0, 0), size=(800, 800))
    # mlab.contour3d(volume, contours=[0.5], transparent=True)
    # mlab.show()

    # take a slice of the volume along the z-axis
    slice2D = volume[:, dim_y // 2, :]

    # display the slice using matplotlib
    plt.imshow(slice2D, cmap='gray')
    plt.show()

    return volume
