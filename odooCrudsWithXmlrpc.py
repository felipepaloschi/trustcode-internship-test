import xmlrpclib

url = 'https://odao.odoo.com'
db = 'odao'
username = 'sadaddasdada@gmail.com'
password = '12345qaz'

server = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))

uid = server.authenticate(db, username, password, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))


# Create a new client and return his identifier:
# {'name': "Novo cliente", 'phone': '2131231', 'email':'papa@papa.com',
# 'street': 'rua rosa, legal, massa, 2'}
def createClient(**kwargs):
    return models.execute_kw(
        db, uid, password, 'res.partner', 'create', [kwargs])


# Update client information:
def updateClient(identifier, **kwargs):
    models.execute_kw(
        db, uid, password, 'res.partner', 'write', [[identifier], kwargs])


def countClients():
    return models.execute_kw(
        db, uid, password,
        'res.partner', 'search_count',
        [[['customer', '=', True]]])


def clientList():
    ids = models.execute_kw(
        db, uid, password,
        'res.partner', 'search',
        [[['customer', '=', True]]],
        {'limit': 10})

    # List comprehensions, getting client data using the
    # ids from the previous search
    clientData = [models.execute_kw(
                    db, uid, password,
                    'res.partner', 'read',
                    [i], {'fields': ['name', 'street']}) for i in ids]

    # The previous 'read' returns every dict inside of a list,
    # so we need to get them
    # out of the list before sorting
    clientData = [x[0] for x in clientData]

    return sorted(clientData, key=lambda k: k['name'])


def biggestSale():
    sales = models.execute_kw(
            db, uid, password,
            'sale.order', 'search_read',
            [],
            {'fields': ['name', 'id', 'partner_id', 'amount_total'],
             'order': 'amount_total'})

    return sales[-1]


# Compares the products ids in the order_lines with the products model
def saleInfo(identifier):
    sales = models.execute_kw(
                db, uid, password,
                'sale.order',
                'read',
                [identifier],
                {'fields': ['order_line']})

    return [models.execute_kw(
                db, uid, password,
                'product.product',
                'read',
                [i],
                {'fields': ['product_id', 'lst_price']}) for i in sales[0][
                    'order_line']]


# Returns the absolute (considering only the number os sales)
# and the price (considers the price of
# each sale) percent of sales
def closedSalesPercent():
    salesOrders = models.execute_kw(
        db, uid, password,
        'sale.order', 'search_read',
        [],
        {'fields': ['id', 'amount_total', 'state']})

    sales = [i for i in salesOrders if i['state'] == 'sale']
    draft = [i for i in salesOrders if i['state'] == 'draft']

    try:
        absolutPercent = ((float(len(sales)))/(
            float(len(sales))+float(len(draft))))*100
    except ZeroDivisionError:
        return 0

    total_sales = sum(i['amount_total'] for i in sales)
    total_draft = sum(i['amount_total'] for i in draft)

    try:
        pricePercent = float((total_sales/(total_sales + total_draft))*100)
    except ZeroDivisionError:
        return 0

    return {'absolutPercent': absolutPercent, 'pricePercent': pricePercent}


def invoiceAmountPerMonth(month):
    invoice = models.execute_kw(
        db, uid, password,
        'account.invoice', 'search_read',
        [],
        {'fields': ['create_date', 'amount_total']})

    invoiceThisMonth = [i for i in invoice if int(
        i['create_date'][5:7]) == month]

    return sum(i['amount_total'] for i in invoiceThisMonth)


def options():
    print '0--> Cadastrar cliente;'
    print '1--> Atualizar cadastro;'
    print '2--> Contar clientes;'
    print '3--> Listar clientes em ordem alfabetica;'
    print '4--> Maior venda;'
    print '5--> Informacoes sobre vendas;'
    print '6--> Porcentagem de vendas;'
    print '7--> Faturas em um mes;\n'
    print 'Digite exit para sair.\n'


def stringToDict(string):
    a = string.split('-')
    b = [x.split('=') for x in a]
    return {x[0]: x[1] for x in b}


def interface(option):
    if option == 0:
        data = raw_input("Entre com os dados do cliente na forma \
            'campo1=dado1-campo2=dado 2':\n")
        try:
            dictData = stringToDict(data)
            ide = createClient(**dictData)
        except Exception:
            print "Voce inseriu dados de forma incorreta, verifique a\
                documentacao caso tenha duvidas."
        else:
            print 'Sucesso, cliente id = {}'.format(ide)

    if option == 1:
        ide = None
        while type(ide) != int:
            ide = input("Entre com o id do cliente: \n")

        data = raw_input("Entre com os dados do cliente na forma \
            'campo1=dado1-campo2=dado 2':\n")
        try:
            dictData = stringToDict(data)
            dictData.update({'customer': True})
            ide = updateClient(ide, **dictData)
        except IndexError:
            print 'Nao existe um cliente com o Id inserido.'
        except Exception:
            print "Voce inseriu dados de forma incorreta, verifique a\
                documentacao caso tenha duvidas."
        else:
            print 'Sucesso'

    if option == 2:
        print "No momento temos {} clientes na base de dados.".format(
            countClients())

    if option == 3:
        a = clientList()
        for i in a:
            if i['street']:
                print 'Nome: {} Endereco: {}'.format(i['name'], i['street'])
            else:
                print 'Nome: {}'.format(i['name'])

    if option == 4:
        big = biggestSale()
        print "Nome: {} Id: {} Valor total: {}".format(
            big['name'], big['id'], big['amount_total'])

    if option == 5:
        data = None
        while type(data) != int:
            try:
                data = input("Entre com id da venda: ")
            except Exception:
                print 'Valor invalido!'

        try:
            prod = saleInfo(data)
        except IndexError:
            print 'Nao existe um registro de venda com o Id inserido.'
        else:
            for i in prod:
                print 'Id do prod: {}, Preco: {}'.format(
                    i[0]['id'], i[0]['lst_price'])

    if option == 6:
        a = closedSalesPercent()
        print 'Porcentagem absoluta: {}%'.format(a['absolutPercent'])
        print 'Porcentagem em relacao aos precos: {}%'.format(
            a['pricePercent'])

    if option == 7:
        data = None
        while type(data) != int and not 0 < data <= 12:
            data = input("Entre com mes desejado: ")
        total = invoiceAmountPerMonth(data)
        print 'Total de vendas do mes {} foi de {}'.format(data, total)


print "Bem-Vindo!\n"

options()

while True:
    option = raw_input("Selecione uma opcao (ou digite help para ver as opcoes\
        novamente): ")
    try:
        option = int(option)
    except Exception:
        pass

    if option == 'help':
        options()
    elif 0 <= option <= 7:
        interface(option)
    elif option == 'exit':
        break
    else:
        print "Favor inserir um comando valido!\n"
