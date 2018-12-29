
from app import db
from app.models import User, Post, Location, Customer, Network, Post_r, Statistic, Category, Subcategory, Info, Hardware


def addC():
    list=["aDSL Asymmetrisch","xDSL Asymmetrisch","Cable Asymmetrisch","vDSL","vULL","IP Add on","Fernwärme",
    "DSL Symmetrisch","xDSL Symmetrisch","Cable Symmetrisch","CIA","EPL","Ethernet Link",
    "Platin","Ecard","Ecard-Internet","Quick Install","UMTS Backup",
     "Managed Security/Lizenzen", "Zwangsfertiggstellt","off. Fertigstel. Kunde	off.","Fertigstel. UPC","MPLS Projekt","MPLS Standard",
     "Sperren","Entsperren","Sonstiges"] 


    for i in list:
	    u=Subcategory(name=i)
	    db.session.add(u)
	    db.session.commit()
