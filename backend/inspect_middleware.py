import sys, os
from app.main import app

print('user_middleware:', app.user_middleware)
for idx, m in enumerate(app.user_middleware):
    print(idx, type(m), getattr(m, 'cls', None), getattr(m, 'options', None))
