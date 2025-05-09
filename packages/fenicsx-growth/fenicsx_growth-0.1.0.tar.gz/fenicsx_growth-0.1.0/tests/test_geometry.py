from mpi4py import MPI

import growth.geometry


def test_unit_cube():
    # Just add a smoke test for now
    comm = MPI.COMM_WORLD
    geo = growth.geometry.load_cube_geometry(comm)
    assert geo is not None
