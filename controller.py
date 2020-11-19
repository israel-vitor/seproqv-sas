from datetime import datetime

from firebase_service import *


def getMainDataServers(type=None):
    dobject = DATA.child('server').get()
    dataServers = dobject.each()
    serversName = []
    if type == None:
        for i in dataServers:
            if i.val()['_delete'] == 1:
                try:
                    serversName.append([i.val()['name'], i.val()['office'], i.val()['reason'], i.val()['departament'],
                                        reajustDateForMain(cleanData(i.val()['evaluate_date'])), i.key()])
                except:
                    serversName.append(
                        [i.val()['name'], i.val()['office'], i.val()['reason'], i.val()['departament'], '-------',
                         i.key()])

    else:
        for i in dataServers:
            if i.val()['type_number'] == type and i.val()['_delete'] == 1:
                serversName.append((i.val()['name'], i.val()['office'], i.val()['reason'], i.val()['departament'],
                                    reajustDateForMain(cleanData(i.val()['evaluate_date'])), i.key()))
    return serversName


def getSearchDataServers(name):
    dobject = DATA.child('server').get()
    dataServers = dobject.each()
    serversData = []
    for i in dataServers:
        try:
            if name in i.val()['name'].lower():
                serversData.append([i.val()['name'], i.val()['office'], i.val()['reason'], i.val()['departament'],
                                    reajustDateForMain(cleanData(i.val()['evaluate_date']))])
        except:
            if name in i.val()['name'].lower():
                serversData.append(
                    [i.val()['name'], i.val()['office'], i.val()['reason'], i.val()['departament'], '-------'])
    return serversData


def getServer(idServer):
    serverBase = DATA.child('server').child(idServer).get()
    serverData = serverBase.val()
    server = Server()
    server.set_id(serverBase.key())
    server.set_name(serverData['name'])
    server.set_office(serverData['office'])
    server.set_departament(serverData['departament'])
    server.set_process(serverData['process'])
    server.set_reason(serverData['reason'])
    server.set_delete(serverData['_delete'])
    server.set_type_number(serverData['type_number'])
    server.set_type_process(serverData['type_process'])
    server.set_contact(serverData['contact'])
    server.set_biannually_ld(serverData['_evaluate']['bi_annually']['last_date'])
    server.set_biannually_nd(serverData['_evaluate']['bi_annually']['next_date'])
    server.set_quarterly_ld(serverData['_evaluate']['quarterly']['last_date'])
    server.set_quarterly_nd(serverData['_evaluate']['quarterly']['next_date'])
    return server


def insertServer(server, remark=None):
    try:
        dataServer = {
            'name': server.get_name(),
            'office': server.get_office(),
            'departament': server.get_departament(),
            'process': server.get_process(),
            'reason': server.get_reason(),
            '_delete': server.get_delete(),
            'type_number': server.get_type_number(),
            'type_process': server.get_type_process(),
            'contact': server.get_contact(),
            'evaluate_date': server.get_evaluate_date(),
            '_evaluate': {
                'bi_annually': {
                    'last_date': server.get_biannually_ld(),
                    'next_date': server.get_biannually_nd()
                },
                'quarterly': {
                    'last_date': server.get_quarterly_ld(),
                    'next_date': server.get_quarterly_nd()
                }}}
        DATA.child('server').push(dataServer)
        if remark != None:
            dataServers = DATA.child('server').get().each()
            key = dataServers[-1].key()
            for i in remark:
                i.set_idServer(key)
                dataRemark = {
                    '_key': i.get_idServer(),
                    'title': i.get_about(),
                    '_date': i.get_time(),
                    'note': i.get_remark()
                }
                DATA.child('remark').push(dataRemark)
        return 'Servidor cadastrado com sucesso!'
    except:
        return 'Erro!'


def updateServer(server, remark):
    try:
        dataServer = {
            'name': server.get_name(),
            'office': server.get_office(),
            'departament': server.get_departament(),
            'process': server.get_process(),
            'reason': server.get_reason(),
            '_delete': server.get_delete(),
            'type_number': server.get_type_number(),
            'type_process': server.get_type_process(),
            'contact': server.get_contact(),
            'evaluate_date': server.get_evaluate_date(),
            '_evaluate': {
                'bi_annually': {
                    'last_date': server.get_biannually_ld(),
                    'next_date': server.get_biannually_nd()
                },
                'quarterly': {
                    'last_date': server.get_quarterly_ld(),
                    'next_date': server.get_quarterly_nd()
                }}}
        DATA.child('server').child(server.get_id()).update(dataServer)
        key = server.get_id()
        if remark != None:
            for i in remark:
                if i.get_id() != None:
                    if i.get_edit() == True:
                        dataRemark = {
                            '_key': i.get_idServer(),
                            'title': i.get_about(),
                            '_date': i.get_time(),
                            'note': datetime.now().strftime('Editado em %d/%m/%Y') + '\n\n' + i.get_remark()
                        }
                    else:
                        dataRemark = {
                            '_key': i.get_idServer(),
                            'title': i.get_about(),
                            '_date': i.get_time(),
                            'note': i.get_remark()
                        }
                    DATA.child('remark').child(i.get_id()).update(dataRemark)
                else:
                    i.set_idServer(key)
                    dataRemark = {
                        '_key': i.get_idServer(),
                        'title': i.get_about(),
                        '_date': i.get_time(),
                        'note': i.get_remark()
                    }
                    DATA.child('remark').push(dataRemark)
    except:
        return 'Ocorreu um erro!'


def getRemark(idserver):
    allremarks = DATA.child('remark').get()
    allremarksData = allremarks.each()
    remarks = []
    for i in allremarksData:
        if i.val()['_key'] == idserver:
            note = Remark()
            note.set_id(i.key())
            note.set_about(i.val()['title'])
            note.set_remark(i.val()['note'])
            note.set_time(i.val()['_date'])
            note.set_idServer(i.val()['_key'])
            remarks.append(note)
    return remarks


def cleanData(value):
    data = ''
    for i in value:
        try:
            int(i)
            data = data + i
        except:
            continue
    return data


def excludeServers(server):
    dataServer = {
        'name': server.get_name(),
        'office': server.get_office(),
        'departament': server.get_departament(),
        'process': server.get_process(),
        'reason': server.get_reason(),
        '_delete': 0,
        'type_number': server.get_type_number(),
        'type_process': server.get_type_process(),
        'contact': server.get_contact(),
        'evaluate_date': server.get_evaluate_date(),
        '_evaluate': {
            'bi_annually': {
                'last_date': server.get_biannually_ld(),
                'next_date': server.get_biannually_nd()
            },
            'quarterly': {
                'last_date': server.get_quarterly_ld(),
                'next_date': server.get_quarterly_nd()
            }}}
    DATA.child('server').child(server.get_id()).update(dataServer)


def evaluateDate(server):
    bianuallyNext = server.get_biannually_nd()
    quarterlyNext = server.get_quarterly_nd()
    if server.get_biannually_nd() == '//' and server.get_quarterly_nd() != '//':
        quarterlyNextdate = datetime.strptime(quarterlyNext, '%Y/%m/%d')
        return quarterlyNext
    elif server.get_biannually_nd() != '//' and server.get_quarterly_nd() == '//':
        bianuallyNextdate = datetime.strptime(bianuallyNext, '%Y/%m/%d')
        return bianuallyNext
    elif server.get_biannually_nd() != '//' and server.get_quarterly_nd() != '//':
        bianuallyNextdate = datetime.strptime(bianuallyNext, '%Y/%m/%d')
        quarterlyNextdate = datetime.strptime(quarterlyNext, '%Y/%m/%d')
        test = bianuallyNextdate > quarterlyNextdate
        if test == False:
            return bianuallyNext
        else:
            return quarterlyNext


def ajustDate(date):
    finaldate = ''
    date = cleanData(date)
    day = date[:2]
    mon = date[2:4]
    year = date[4:]
    finaldate = year + '/' + mon + '/' + day
    return finaldate


def reajustDate(date):
    finaldate = ''
    day = date[6:]
    mon = date[4:6]
    year = date[:4]
    finaldate = day + mon + year
    return finaldate


def reajustDateForMain(date):
    finaldate = ''
    day = date[6:]
    mon = date[4:6]
    year = date[:4]
    finaldate = day + '/' + mon + '/' + year
    return finaldate
