from sqlalchemy.orm import sessionmaker
from models import Cliente, db
Session=sessionmaker(bind=db)
session=Session()


#deletar somente um
session.query(Cliente).filter(Cliente.id ==1).delete()
session.commit()
session.close()
