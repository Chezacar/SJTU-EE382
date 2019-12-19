from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
def show(x,y,transformed):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x[0,:], x[1,:], x[2,:], c='m', marker='v')
    ax.scatter(y[0,:], y[1,:], y[2,:], c='r', marker='^')
    ax.scatter(transformed[0,:], transformed[1,:], transformed[2,:], c='c', marker='o')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend(['src', 'dsc', 'trans'])
    plt.show()