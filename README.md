# aws-sdk-hermes
Coleta de recursos na aws de forma programática

O programa tem como objetivo a coleta de recursos dentro de uma conta aws de forma programática.

Recursos: IAM,AMI,EC2,RDS,Snapshot,Security Groups,EBS,Load balancers,S3,EFS e WAF.


<br>

## Requisitos

* Possuir **python3** instalado com as seguintes libs:

```
boto3==1.24.11
pandas==1.4.2
openpyxl==3.0.10
awscli==1.18.69
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


---

## Work in Progress  👷🏻‍♂️

- [x] IAM
- [x] AMI
- [x] EC2
- [x] RDS
- [x] Snapshot
- [x] SecurityGroups
- [x] EBS
- [x] Load balancer
- [x] S3
- [ ] Imagem docker
- [ ] CI/CD build & push



