from models import *

tok = UserToken(user_id=1, token='anfjaf')
db.session.add(tok)
db.session.commit()