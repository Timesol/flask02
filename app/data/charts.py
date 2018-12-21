import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

#%matplotlib inline

def barchart():


    plt.style.use('ggplot')

    x = ['Test', 'Hydro', 'Gas', 'Oil', 'Coal', 'Biofuel']
    energy = [5, 6, 15, 22, 24, 8]

    x_pos = [i for i, _ in enumerate(x)]

    plt.bar(x_pos, energy, color='green')
    plt.xlabel("Energy Source")
    plt.ylabel("Energy Output (GJ)")
    plt.title("Energy output from various fuel sources")

    plt.xticks(x_pos, x)

    plt.savefig('/home/ahoehne/flask02/app/static/images/new_plot.png')    




