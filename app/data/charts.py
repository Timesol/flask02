import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from app.models import Customer,Location,Network,User,Statistic
from flask_login import login_user, logout_user, current_user, login_required

#%matplotlib inline

def barchart():

	user=User.query.filter_by(username=current_user.username).first_or_404()
	category=Category.query.filter_by(name="Installation").first_or_404()
	category.statistics
	stats=user.statistics
	

    for i in stats:



    plt.style.use('ggplot')

    x = ['Installation', 'Commissioning', 'Dismantling', 'MPLS', 'CIA', 'Hardware','Unlock', 'Disruption']
    energy = [5, 6, 15, 22, 24, 8]

    x_pos = [i for i, _ in enumerate(x)]

    plt.bar(x_pos, energy, color='green')
    plt.xlabel("Energy Source")
    plt.ylabel("Energy Output (GJ)")
    plt.title("Energy output from various fuel sources")

    plt.xticks(x_pos, x)

    plt.savefig('/home/ahoehne/flask02/app/static/images/new_plot.png')    




