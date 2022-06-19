# aws-sdk-hermes
Coleta de recursos na aws de forma programática

O programa tem como objetivo a coleta de recursos dentro de uma conta aws de forma programática.

Recursos: IAM,AMI,EC2,RDS,Snapshot,Security Groups,EBS,Load balancers,S3,EFS e WAF.


## Requisitos

* Possuir **python3** instalado com as seguintes libs:

```
boto3==1.24.11
pandas==1.4.2
openpyxl==3.0.10
awscli==1.18.69
```

* Possuir acesso programático à conta com pelo menos permissão de **ReadOnlyAccess**


## Como utilizar

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

Após isso, basta executar o programa utilizando o comando:

```
python3 main.py
```


## Work in Progress  👷🏻‍♂️

- [x] IAM
- [ ] AMI
- [ ] EC2
- [ ] RDS
- [ ] Snapshot
- [ ] SecurityGroups
- [ ] EBS
- [ ] Load balancer
- [ ] S3
- [ ] EFS
- [ ] WAF
- [ ] Imagem docker
- [ ] CI/CD build & push



