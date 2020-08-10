from threading import Thread

import requests
from bs4 import BeautifulSoup
from model.Endereco import Endereco
import time


class Correios:

    #EFETUA REQUEST DE BUSCA
    def efetuaRequestDeBusca(self, session, data):
        time.sleep(0.2)
        while True:
            try:
                response = session.post(
                    "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm",
                    data)
                return response
            except:
                time.sleep(1.0)


    #METODO QUE REALIZA A BUSCA DE CEPS
    def buscaCEP(self, cep):

        #INICIALIZA VARIAVEIS PARA PRIMEIRA REQUEST
        data = {'relaxation': cep, 'tipoCEP': 'ALL', 'semelhante': 'N'}
        session = requests.Session()

        #FAZ A REQUEST HTTP NO SITE DOS CORREIOS
        response = self.efetuaRequestDeBusca(session, data)

        #INICIALIZA A LISTA DE ENDERECOS
        listEnderecos = []
        while True:

            #PROCESSAMENTO DAS INFORMACOES OBTIDAS ATRAVES DA REQUEST
            soup = BeautifulSoup(response.content, 'html.parser')
            tableEnderecos = soup.find_all("table", class_="tmptabela")[0]
            trEnderecos = tableEnderecos.find_all("tr")

            # REMOVE O CABECALHO DA TABELA
            trEnderecos.pop(0)

            for endereco in trEnderecos:
                tdEndereco = endereco.find_all("td")
                listEnderecos.append(
                    Endereco(tdEndereco[0].text, tdEndereco[1].text, tdEndereco[2].text, tdEndereco[3].text))

            #ENQUANTO ELEMENTO Proxima  ESTA PRESENTE REALIZA NOVA REQUEST
            formProxima = soup.find_all("form", attrs={"name": "Proxima"})
            if (formProxima.__len__() == 0):
                break;

            inputProxima = formProxima[0].find_all("input")
            for proxima in inputProxima:
                data[proxima.attrs["name"]] = proxima.attrs["value"]
            try:
                del data["tipoCEP"]
            except:
                None

            #REALIZA A PROXIMA REQUEST
            response = self.efetuaRequestDeBusca(session, data)

        return listEnderecos