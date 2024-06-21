import os
import numpy as np
import pandas as pd
import gudhi
import plotly.graph_objects as go

df = pd.read_csv(os.path.join('../crystal/output', 'AEI.csv'), header=0)

point_cloud = df[['x', 'y', 'z']].values


rc = gudhi.RipsComplex(points=point_cloud, max_edge_length = 4.0)
skeleton = rc.create_simplex_tree(max_dimension = 2)
#print(dir(rc))

# We are only going to plot the triangles
triangles = np.array([s[0] for s in skeleton.get_skeleton(2) if len(s[0])==3])

# First possibility: plotly

print([s for s in skeleton.get_skeleton(2)])

# fig = go.Figure(data=[
#     go.Mesh3d(
#         # Use the first 3 coordinates, but we could as easily pick others
#         x=point_cloud[:,0],
#         y=point_cloud[:,1],
#         z=point_cloud[:,2],
#         i = triangles[:,0],
#         j = triangles[:,1],
#         k = triangles[:,2],
#     )
# ])
# fig.show()

# points = np.array([skeleton.get_point(i) for i in range(st.num_vertices())])
# # We want to plot the alpha-complex with alpha=0.005 by default.
# # We are only going to plot the triangles
# triangles = np.array([s[0] for s in st.get_skeleton(2) if len(s[0]) == 3 and s[1] <= 0.005])

# print(points)
#
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
#
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# l = ax.plot_trisurf(points[:, 0], points[:, 1], points[:, 2], triangles = triangles)
# ax.set_xlim(-20.1, 20.1)
# ax.set_ylim(-20.1, 20.1)
# ax.set_zlim(-20.1, 20.1)
#
# plt.show()