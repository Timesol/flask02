import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
#%matplotlib inline
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory, Info, Hardware
import os

def barchart():

    u=current_user
    a=Category.query.filter_by(name='Installation').first()
    b=Category.query.filter_by(name='Commissioning').first()
    c=Category.query.filter_by(name='Dismantling').first()
    d=Category.query.filter_by(name='MPLS').first()
    e=Category.query.filter_by(name='CIA').first()
    f=Category.query.filter_by(name='Hardware').first()
    g=Category.query.filter_by(name='Unlock').first()
    h=Category.query.filter_by(name='Disruption').first()

    a=u.statistics.filter(Statistic.category==a).count()
    b=u.statistics.filter(Statistic.category==b).count()
    c=u.statistics.filter(Statistic.category==c).count()
    d=u.statistics.filter(Statistic.category==d).count()
    e=u.statistics.filter(Statistic.category==e).count()
    f=u.statistics.filter(Statistic.category==f).count()
    g=u.statistics.filter(Statistic.category==g).count()
    h=u.statistics.filter(Statistic.category==h).count()


    plt.style.use('ggplot')

    x = ['Installation', 'Commissioning', 'Dismantling', 'MPLS', 'CIA', 'Hardware','Unlock', 'Disruption']
   
    y = [a,b,c,d,e,f,g,h]
    plt.figure(figsize=(12,5))
    plt.bar(x, y, color='green' )
    plt.xlabel("Categorys")
    plt.ylabel("Amount")
    plt.title("Userstatistic")



    plt.savefig(os.environ.get('IMAGE_FOLDER')+current_user.username+'_barplot.png')    