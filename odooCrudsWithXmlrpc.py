import xmlrpclib

url = 'https://batata.odoo.com'
db = 'batata'
username = 'paloschifelipe@outlook.com'
password = 'cdnn792458'

server = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = server.authenticate(db, username, password, {})

objects = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))


#Create a new client and return his identifier:
#args = {'name': "Novo cliente", 'phone': '2131231', 'email':'papa@papa.com', 'street': 'rua rosa, legal, massa, 2'}
def createClient(**kwargs):
    return objects.execute_kw(db, uid, password, 'res.partner', 'create', [kwargs])

