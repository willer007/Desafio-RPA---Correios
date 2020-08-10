from flow.Correios import Correios
import csv

#PATTERN MAIN - FLUXO PRINCIPAL DE EXECUCAO
def main():
    correios = Correios()
    with open('searched_ceps.csv', 'w', newline='') as csvfile:
        enderecoWriter = csv.writer(csvfile, delimiter=';')
        enderecoWriter.writerow(['Searched CEP:', 'Logradouro/Nome:', 'Bairro/Distrito:', 'Localidade/UF:', 'CEP:'])
        listEndereco = correios.buscaCEP(22770)
        for endereco in listEndereco:
            enderecoWriter.writerow([22770, endereco.logradouroNome, endereco.bairroDistrito, endereco.localidadeUF, endereco.cep])

if __name__ == "__main__":
    main()