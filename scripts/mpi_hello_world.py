from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
n_ranks = comm.Get_size()

print ('{}/{} Hello World!'.format(rank + 1, n_ranks))
