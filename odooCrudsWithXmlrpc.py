import xmlrpclib

url = 'https://batata.odoo.com'
db = 'batata'
username = 'paloschifelipe@outlook.com'
password = 'cdnn792458'

server = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = server.authenticate(db, username, password, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))


#Create a new client and return his identifier:
#{'name': "Novo cliente", 'phone': '2131231', 'email':'papa@papa.com', 'street': 'rua rosa, legal, massa, 2'}
def createClient(**kwargs):
    return models.execute_kw(db, uid, password, 'res.partner', 'create', [kwargs])

#Update client information:
def updateClient(identifier, **kwargs):
    models.execute_kw(db, uid, password, 'res.partner', 'write', [[identifier], kwargs])

def countClients():
    return models.execute_kw(db, uid, password,
    'res.partner', 'search_count',
    [[['customer', '=', True]]])

def clientList(limit=10):
    ids = models.execute_kw(db, uid, password,
        'res.partner', 'search',
        [[['customer', '=', True]]],
        {'limit': limit})

    #list comprehensions, getting client data using the ids from the previous search
    clientData = [models.execute_kw(db, uid, password,
                'res.partner', 'read',
                [i], {'fields': ['name', 'street']}) for i in ids]


    #the previous 'read' returns every dict inside of a list, so we need to get them
    #out of the list before sorting
    clientData = [x[0] for x in clientData]

    return sorted(clientData, key = lambda k: k['name']) 
