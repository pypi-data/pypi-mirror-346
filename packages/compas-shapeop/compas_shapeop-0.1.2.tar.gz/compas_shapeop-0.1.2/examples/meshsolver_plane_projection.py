import compas
from compas.geometry import Scale
from compas.geometry import Translation
from compas_viewer import Viewer

from compas_shapeop.meshsolver import MeshSolver

T = Translation.from_vector([-5, -5, -3]) * Scale.from_factors([2, 2, 2])
s = MeshSolver.from_obj(compas.get("hypar.obj"), T)
s.fix_vertices(weight=0.01)
s.constrain_edge_lengths()
s.constrain_face_diagonals()
s.constrain_face_planarity()

viewer = Viewer()
mesh_obj = viewer.scene.add(s.mesh)


@viewer.on(interval=1)
def update(frame):
    s.solve(1)
    mesh_obj.update(update_data=True)


viewer.show()
