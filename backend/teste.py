from sqlalchemy.orm import sessionmaker
from backend.app.models import Cliente, db
Session=sessionmaker(bind=db)
session=Session()


#deletar somente um
session.query(Cliente).delete()
session.commit()
session.close()

print("deletado com sucesso")