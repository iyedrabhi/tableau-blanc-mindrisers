from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='tcsfr').exists():
    User.objects.create_user('tcsfr','tcsfr@example.com','testpass')
from django.test import Client
c = Client()
r = c.get('/login/')
print('GET', r.status_code)
print('cookies', dict(c.cookies))
import re
m = re.search(b'name="csrfmiddlewaretoken" value="([^"]+)"', r.content)
print('csrf_in_form', bool(m))
token = m.group(1).decode() if m else None
print('token', token)
p = c.post('/login/', {'username':'tcsfr','password':'testpass','csrfmiddlewaretoken': token})
print('POST status', p.status_code)
print('POST content len', len(p.content))
print('POST content snippet', p.content[:500])
