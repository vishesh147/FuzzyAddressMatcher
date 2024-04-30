from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

engine = create_engine('sqlite:///addresses.db')

Base = automap_base()
Base.prepare(engine)
Address = Base.classes.Address

session = Session(engine)

results = session.query(Address).all()
for result in results:
    print(result.id, result.address)

# Close the session
session.close()
