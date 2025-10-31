import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from python.app.repos.client_repo import ClientRepo
import uuid

if __name__ == '__main__':
    crepo = ClientRepo()
    unique = uuid.uuid4().hex[:8]
    try:
        cid = crepo.create({'full_name': 'Premium Test', 'email': f'prem+{unique}@test.com', 'phone': f'9{unique}', 'client_type': 'premium'})
        print('created client id=', cid)
    except Exception as e:
        print('create error', repr(e))
        raise
    try:
        c = crepo.get(cid)
        print('got client repr:', repr(c))
        try:
            print('client dict:', c.dict())
        except Exception as e:
            print('client.dict() error:', repr(e))
    except Exception as e:
        print('get error', repr(e))
        raise
