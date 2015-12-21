from app import app,db
from app.models import User


useradd = User('lobert','rschmidt.zalles@gmail.com','libert')

db.session.add(useradd)

db.session.commit()
