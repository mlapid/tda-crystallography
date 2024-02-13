from gemmi import cif
from Crystal import Crystal

path = "data/AEI.cif"
doc = cif.read_file(path)
crystal = Crystal(doc)

crystal.plot()