import matplotlib.pyplot as plt

def plot_convergence(history):
    plt.plot(history)
    plt.xlabel("Iteration")
    plt.ylabel("Objective Value")
    plt.title("Optimization Convergence")
    plt.grid(True)
    plt.show()
