import gudhi
import numpy as np
import ipywidgets as widgets

from typing import List, Tuple
from plotly.graph_objs import graph_objs as go
from plotly.offline    import iplot
from ripser import Rips


class RipsComplex:

    DIMENSION: int = 2

    def __init__(self, data: np.array, distance_matrix: bool = False):
        self.data = data # 3-D point cloud or distance matrix
        self.distance_matrix = distance_matrix

        self.simplex_tree: gudhi.SimplexTree = gudhi.RipsComplex(points=data).create_simplex_tree(max_dimension=self.DIMENSION)
        self.filtration: List[Tuple[List, float]] = list(self.simplex_tree.get_filtration())
        self.max_radius: float = max(self.filtration, key=lambda x: x[1])[1]

        self.rips_complex = Rips(maxdim = self.DIMENSION, verbose = False)

        self.persistence: List[np.array] = None
        if self.distance_matrix:
            self.persistence = self.rips_complex.fit_transform(X = self.data, distance_matrix = True)
        else:
            self.persistence = self.rips_complex.fit_transform(X = self.data, distance_matrix = False)
    
    def plot(self, radius: float = None) -> None:

        if radius is None:
            radius = self.max_radius
        else:
            if radius > self.max_radius:
                radius = self.max_radius

        print(f"Plotting simplicial complex with radius {radius:.2f}...")

        x = self.data[:, 0]
        y = self.data[:, 1]
        z = self.data[:, 2]

        edges = np.array([s[0] for s in self.filtration if len(s[0]) == 2 and s[1] <= radius])
        triangles = np.array([s[0] for s in self.filtration if len(s[0]) == 3 and s[1] <= radius])

        def create_edges(edges) -> Tuple[list, list, list]:

            if len(edges) == 0:
                return [], [], []
            else:
                x_edges = []
                y_edges = []
                z_edges = []

                for p in edges:
                    for i in range(2):
                        x_edges.append(x[p[i]])
                        y_edges.append(y[p[i]])
                        z_edges.append(z[p[i]])
                    x_edges.append(None)
                    y_edges.append(None)
                    z_edges.append(None)

                return x_edges, y_edges, z_edges

        def create_triangles(triangles) -> Tuple[list, list, list]:
            if len(triangles) == 0:
                return [], [], []
            else:
                i = triangles[:, 0]
                j = triangles[:, 1]
                k = triangles[:, 2]
                return i, j, k
        

        x_edges, y_edges, z_edges = create_edges(edges)
        i, j, k = create_triangles(triangles)


        nodes = go.Scatter3d(
            x = x,
            y = y,
            z = z,
            mode = 'markers',
            name = 'nodes',
            marker = dict(
                symbol = 'circle',
                size = 6,
                opacity = 0.8
            )
        )

        edges = go.Scatter3d(
            x = x_edges,
            y = y_edges,
            z = z_edges,
            mode = 'lines',
            name = 'edges'
        )

        mesh = go.Mesh3d(
            x = x, 
            y = y, 
            z = z,
            i = i,
            j = j,
            k = k,
            color = 'orange',
            opacity = 0.30,
            name = 'triangles'
        )

        fig = go.Figure(data=[nodes, edges, mesh])
        fig.update_layout(
            scene=dict(
                xaxis_title='x',
                yaxis_title='y',
                zaxis_title='z'
            ),
            title = f"Rips Complex with radius {radius:.2f}"
        )
        fig.show()

        return
    
    def plot_interactive(self, step: float = 0.1) -> None:

        '''Only works in jupyter notebook environment.'''

        x = self.data[:, 0]
        y = self.data[:, 1]
        z = self.data[:, 2]

        nodes = go.Scatter3d(
            x = x,
            y = y,
            z = z,
            mode = 'markers',
            name='nodes',
            marker=dict(
                symbol='circle',
                size=6,
                opacity=0.8
            )
        )

        edges = go.Scatter3d(
            x = [],
            y = [],
            z = [],
            mode='lines',
            name='edges'
        )

        mesh = go.Mesh3d(
            x = x, 
            y = y, 
            z = z,
            i = [],
            j = [],
            k = [],
            color = 'orange',
            opacity=0.30,
            name='triangles'
        )

        fig = go.Figure(data=[nodes, edges, mesh])
        fig.update_layout(
            scene=dict(
                xaxis_title='x',
                yaxis_title='y',
                zaxis_title='z'
            )
        )

        radiusWidget = widgets.FloatSlider(
            value = 0.0,
            min = 0.0,
            max = self.max_radius,
            step = step,
            description = 'Radius:'
        )

        def update_edges(edges) -> Tuple[list, list, list]:

            x_edges = []
            y_edges = []
            z_edges = []

            for p in edges:
                for i in range(2):
                    x_edges.append(x[p[i]])
                    y_edges.append(y[p[i]])
                    z_edges.append(z[p[i]])
                x_edges.append(None)
                y_edges.append(None)
                z_edges.append(None)

            return x_edges, y_edges, z_edges

        @widgets.interact(radius = radiusWidget)
        def update_mesh(radius) -> None:

            edges = np.array([s[0] for s in self.filtration if len(s[0]) == 2 and s[1] <= radius])
            triangles = np.array([s[0] for s in self.filtration if len(s[0]) == 3 and s[1] <= radius])

            if len(edges) > 0:
                x_edges, y_edges, z_edges = update_edges(edges)
                fig.data[1].x = x_edges
                fig.data[1].y = y_edges
                fig.data[1].z = z_edges
            else:
                fig.data[1].x = []
                fig.data[1].y = []
                fig.data[1].z = []
            
            if len(triangles) > 0:
                fig.data[2].i = triangles[:, 0]
                fig.data[2].j = triangles[:, 1]
                fig.data[2].k = triangles[:, 2]
            else:
                fig.data[2].i = []
                fig.data[2].j = []
                fig.data[2].k = []

            fig.update_layout(
                autosize=False,
                width = 800,
                height = 800,
                title=f'Rips Complex with radius {radius:.2f}'
            )
            iplot(fig)

        return
    
# if __name__ == "__main__":
#     data = np.random.rand(10, 3)
#     rips_complex = RipsComplex(data)
#     rips_complex.plot(0.5)