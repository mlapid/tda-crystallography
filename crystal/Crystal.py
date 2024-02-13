import plotly.express as px
from gemmi import cif
from UnitCell import UnitCell


class Crystal:

    def __init__(self, doc: cif.Document):
        self.doc = doc
        try:
            self.block = doc.sole_block()
        except:
            print("Block error")
            raise

        self.unitCell = UnitCell(self.block)

    def __str__(self) -> str:
        return f'Crystal of {len(self.unitCell.cartesianCoordinates)} vertices with a unit cell {self.unitCell}'

    def plot(self) -> None:
        # Plot in 3D Cartesian coordinates

        fig = px.scatter_3d(
            self.unitCell.to_dataframe(), x='x', y='y', z='z',
            color='symbol', symbol='symbol'
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        fig.show()

        return