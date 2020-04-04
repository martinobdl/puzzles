import numpy as np 


def build_solver(N):
    N_tri = sum([2*j+1 for j in range(N-1)])
    N_points = int(N*(N+1)/2)


    A=np.zeros((1,N_points)).astype(int)

    d={}
    for i in range(0,N):
        for j in range(i+1):
            n = int((i*(i+1)/2)+j+1)
            d[(i,j)] = n

    for i in range(1,N):
        for j in range(2*i-1):
            if j==0:
                row = np.zeros(N_points).astype(int)
                p1,p2,p3=d[(i,j)],d[(i,j+1)],d[(i-1,j)]
                row[p1-1]=1
                row[p2-1]=1
                row[p3-1]=1
                A = np.concatenate((A, row.reshape(1,N_points)), axis=0)
            elif j>=i:
                pass
            else:
                row = np.zeros(N_points).astype(int)
                p1,p2,p3=d[(i,j)],d[(i,j+1)],d[(i-1,j)]
                row[p1-1]=1
                row[p2-1]=1
                row[p3-1]=1
                A = np.concatenate((A, row.reshape(1,N_points)), axis=0)

                row = np.zeros(N_points).astype(int)
                p1,p2,p3=d[(i,j)],d[(i-1,j)],d[(i-1,j-1)]
                row[p1-1]=1
                row[p2-1]=1
                row[p3-1]=1
                A = np.concatenate((A, row.reshape(1,N_points)), axis=0)
    A = A[1:,:]
    print(A.shape[0])
    np.savetxt("./data/tri_"+str(N)+".txt",A,header=str(A.shape[1]),comments="",fmt='%d')

if __name__ == "__main__":
    for N in range(2,41):
        if int(N*(N+1)/2%3==0):
            # build_solver(N)
            print(N)

