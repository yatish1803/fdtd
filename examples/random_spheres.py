import numpy as np
from mayavi import mlab


def generate_sphere_positions(num_spheres):
    positions = []
    while len(positions) < num_spheres:
        # generate a random position within the bounds of the 3D volume
        x = np.random.randint(10, 90)
        y = np.random.randint(10, 90)
        z = np.random.randint(10, 190)
        pos = np.array([x, y, z])

        # check if the sphere overlaps with any previously placed spheres
        overlapping = False
        for p in positions:
            dist = np.linalg.norm(pos - p)
            if dist < 10:
                overlapping = True
                break

        # if the sphere does not overlap, add its position to the list
        if not overlapping:
            positions.append(pos)

    return positions


def place_spheres_in_volume(volume, positions):
    for pos in positions:
        x, y, z = pos
        # place the sphere in the 3D volume
        for i in range(-5, 6):
            for j in range(-5, 6):
                for k in range(-5, 6):
                    if np.linalg.norm(np.array([i, j, k])) <= 5:
                        volume[x + i, y + j, z + k] = 1

    return volume


# create an empty 3D numpy array
volume = np.zeros((100, 100, 200), dtype=int)

# generate positions for 100 non-overlapping spheres
positions = generate_sphere_positions(100)

# place the spheres in the 3D volume
volume = place_spheres_in_volume(volume, positions)

# display the 3D volume with the spheres
mlab.figure(bgcolor=(0, 0, 0), size=(800, 800))
mlab.contour3d(volume, contours=[0.5], transparent=True)
mlab.show()
