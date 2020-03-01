from threading import Thread

import requests
from bs4 import BeautifulSoup
from model.Endereco import Endereco
import time


class Correios:

    def buscaCEP(self, cep):
        data = {'relaxation': cep, 'tipoCEP': 'ALL', 'semelhante': 'N'}

        session = requests.Session()

        time.sleep(0.2)
        flag_processou_busca = False
        while not flag_processou_busca:
            try:
                response = session.post(
                    "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm",
                    data)
                flag_processou_busca = True


            except:
                time.sleep(1.0)

        listEnderecos = []

        while True:

            soup = BeautifulSoup(response.content, 'html.parser')
            tableEnderecos = soup.find_all("table", class_="tmptabela")[0]
            trEnderecos = tableEnderecos.find_all("tr")

            # REMOVE O CABECALHO DA TABELA
            trEnderecos.pop(0)

            for endereco in trEnderecos:
                tdEndereco = endereco.find_all("td")
                listEnderecos.append(
                    Endereco(tdEndereco[0].text, tdEndereco[1].text, tdEndereco[2].text, tdEndereco[3].text))

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

            time.sleep(0.2)
            flag_processou_proximo = False
            while not flag_processou_proximo:
                try:
                    response = session.post(
                        "http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm",
                        data)
                    flag_processou_proximo = True;

                except:
                    time.sleep(1.0)

        return listEnderecos