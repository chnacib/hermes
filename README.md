# Hermes
![build](https://github.com/chnacib/aws-sdk-hermes/actions/workflows/ci.yml/badge.svg)

Coleta de recursos na aws de forma programática

O programa tem como objetivo a coleta de recursos dentro de uma conta aws de forma programática.

Recursos: IAM,AMI,EC2,RDS,Snapshot,Security Groups,EBS,Load balancers e S3.


<br>

## Requisitos

* Possuir **python3** instalado com as seguintes libs:

```
boto3==1.21.26
pandas==1.4.2
openpyxl==3.0.10
awscli==1.22.81
python-dotenv==0.20.0
progress==1.6
```

* Possuir acesso programático à conta com pelo menos permissão de **ReadOnlyAccess**

<br>

## Configuração

Primeiramente o usuário deve realizar login no awscli passando as credenciais.
```
$ aws configure
```

ou exportando as credenciais como variável de ambiente.

```
$ export AWS_ACCESS_KEY_ID="xxxxxxxxx"
$ export AWS_SECRET_ACCESS_KEY="xxxxxxxxx"
```
Instalar as libs se for necessário, utilizando o arquivo **requirements.txt**
```
pip install -r requirements.txt
```


### Variáveis de Ambiente

| Nome | Description  | Default |
| --- |  --- |  --- |
AWS_REGION | Região padrão para a pesquisa de recursos pelo SDK | us-east-1
PROJ_NAME | Nome do projeto, os arquivos gerados incluírão esse nome. Utilizar um nome diferente para cada cliente. | projx
OUPUT_FOLDER | Pasta na qual os arquivos gerados serão salvos | ./output/

<br>

## Como utilizar

Para utilizar a aplicação é necessário executar o comando:
```
python3 main.py <options>
```
Para definir quais serviços devem ser incluídos na análise é preciso utilizar os argumentos:



### Serviços:

| Argument | Description |
| --- |  --- |
| --s3 | Buckets S3 | 
| --iam | Usuários IAM |
| --ec2 | Instâncias EC2 | 
| --sg-ec2 | Security Groups - EC2 |
| --ebs | Volumes EBS |
| --snapshot | Snaphots de Volumes EBS |
| --ami | Imagens AMI |
| --loadbalancer | Loadbalancers |
| --rds | RDS |
| --sg-rds | Security Groups - RDS |
| -a, --all | Inclui todos os serviços | 




### Opções Adicionais:

| Argument | Description |
| --- |  --- |
| -j, --join | Unifica todos as planilhas geradas em um único arquivo | 
| -h | Help | 


### Exemplos:




Para gerar um relatório referente ao S3 e um relatório referente à RDS:

```
python3 main.py --s3 --rds
```

Para gerar um relatório único que contenha todos os serviços:

```
python3 main.py -a -j
```
<br>


## Utilizando docker

É possível executar essa aplicação utilizando um container docker hospedado publicamente no dockerhub registry.

Para a execução via docker, é necessário ter o awscli instalado na máquina local e configurar as credenciais com o `aws configure`. Após isso, basta utilizar o seguinte comando:

```
docker run -it -v "$(pwd):/app/output" -v $HOME/.aws/credentials:/root/.aws/credentials:ro -e PROJ_NAME=XXXXX -e AWS_REGION=us-east-1 chnacib/hermes 
```

Lembrando que deve ser passado as opções adicionais ao final do comando. Por exemplo:

```
docker run -it -v "$(pwd):/app/output" -v $HOME/.aws/credentials:/root/.aws/credentials:ro -e PROJ_NAME=XXXXX -e AWS_REGION=us-east-1 chnacib/hermes --all --join

```

Os arquivos serão gerados no diretório local onde foi executado o comando docker, ou basta substituir a variável $(pwd) pelo path desejado.


