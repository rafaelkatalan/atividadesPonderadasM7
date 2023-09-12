## Notebook (`modelo.ipynb`)

O notebook `modelo.ipynb` cria um modelo de aprendizado de máquina que prevê o número de óbitos em acidentes de trânsito na rodovia Autopista Fernão Dias, no Brasil. O notebook é dividido nas seguintes seções:

- **Importação de Bibliotecas**: Importa as bibliotecas necessárias, incluindo `matplotlib`, `pandas`, `scikit-learn`, entre outras.

- **Carregamento de Dados**: Realiza o carregamento dos dados a partir do arquivo CSV contendo informações sobre acidentes de trânsito.

- **Filtragem de Dados**: Filtra os dados para incluir apenas registros relacionados à "Autopista Fernão Dias", uma vez que o modelo se concentra exclusivamente nessa rodovia.

- **Pré-Processamento de Dados**: Executa etapas de pré-processamento, como tratamento de valores ausentes, conversão de tipos de dados e eliminação de colunas irrelevantes.

- **Preparação para Modelagem**: Prepara os dados para a construção do modelo de aprendizado de máquina, definindo a coluna alvo como "mortos".

- **Modelagem com PyCaret**: Utiliza o framework PyCaret para simplificar a criação e avaliação de modelos de regressão. O modelo LightGBM é selecionado, ajustado e finalizado.

- **Salvando o Modelo**: Salva o modelo finalizado como "lgbmregressor.pkl" para uso futuro.

## Backend `app.py`

O script `app.py` é uma aplicação Flask que serve como uma API para realizar previsões com o modelo treinado. Ele possui as seguintes funcionalidades:

- **API Flask**: Cria uma API web utilizando Flask, projetada para receber dados no formato JSON via solicitações POST e retornar previsões baseadas no modelo treinado.

- **Carregamento do Modelo**: Carrega o modelo pré-treinado a partir do arquivo "lgbmregressor.pkl" usando a biblioteca PyCaret.

- **Previsão com o Modelo**: Quando os dados são enviados para a API, o modelo é utilizado para prever o número de óbitos em acidentes de trânsito com base nas informações fornecidas.

- **Resposta JSON**: As previsões são retornadas como uma resposta JSON.

## Dockerfile

O Dockerfile é usado para criar um contêiner Docker que contém a aplicação Flask e o modelo treinado. Ele possui os seguintes passos:

- **Imagem Base**: Utiliza a imagem base do Python (3.8).

- **Diretório de Trabalho**: Define o diretório de trabalho dentro do contêiner como "/app".

- **Cópia de Dependências**: Copia o arquivo "requirements.txt" e instala as dependências listadas nele.

- **Cópia de Arquivos**: Copia todos os arquivos do diretório atual (onde o Dockerfile está localizado) para o diretório "/app" no contêiner.

- **Exposição da Porta**: Expõe a porta 5000 para permitir o acesso à aplicação Flask.

- **Comando de Inicialização**: Define o comando para iniciar o aplicativo Flask quando o contêiner é executado.

O Dockerfile facilita a criação de um ambiente isolado e portátil para a execução da API em qualquer sistema compatível com Docker.

## Uso da API

Para utilizar a API e obter previsões com base no modelo treinado, siga as instruções abaixo:

### Montando o Container

1. Navegue até o diretório raiz do projeto onde se encontra o Dockerfile.

2. Construa o contêiner Docker executando o seguinte comando:

```bash
docker build -t nome_do_contenedor .
```

### Iniciando o Container

4. Após a conclusão da construção do contêiner, inicie-o com o seguinte comando:

```bash
docker run -p 5000:5000 nome_do_contenedor
```

### Enviando Solicitações

5. Utilize o Postman ou outra ferramenta de sua preferência para enviar solicitações POST para a API. A URL da API será `http://localhost:5000/api`.

6. Insira os dados de entrada no formato JSON na solicitação. Por exemplo:

```json
{
  "km": 10000,
  "automovel": 1,
  "bicicleta": 0,
  "caminhao": 0,
  "moto": 0,
  "onibus": 0,
  "outros": 0,
  "tracao_animal": 0,
  "transporte_de_cargas_especiais": 0,
  "trator_maquinas": 0,
  "utilitarios": 1
}
```

### Recebendo Resultados

7. Após enviar a solicitação, você receberá uma resposta JSON contendo as previsões do modelo, como o número previsto de óbitos em acidentes de trânsito com base nos dados fornecidos.

Lembre-se de que o servidor da API deve estar em execução para processar as solicitações. Certifique-se de seguir as instruções acima para construir, iniciar e utilizar o contêiner da API com sucesso.