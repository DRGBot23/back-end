# Trabalho final de Back-End
# Como executar o projeto

**Importante:** o repositório já acompanha o arquivo `db.sqlite3`, contendo dados iniciais e usuários prontos para uso.

## 1. Clone o repositório

```bash
git clone https://github.com/DRGBot23/back-end.git
cd seu-repo
```

## 2. Crie o ambiente virtual
```bash
python -m venv env
```

## 3. Ative o ambiente:
```bash
Windows:
PowerShell: env\Scripts\activate
Gitbash: source env/Scripts/activate

Linux / Mac:
source env/bin/activate
```

## 4. Instale as dependências
```bash
pip install -r requirements.txt
```
## 5. Execute o servidor
Se necessario use cd supermercado para ficar na pasta certa.
```bash
python manage.py runserver
```
## 6. Agora abra no navegador:
```bash
http://127.0.0.1:8000
```
## Contas de acesso já cadastradas:
```bash
O banco enviado já possui dois usuários configurados:

#Administrador
Email: adm@gmail.com
Senha: 123
Permissões: Pode acessar tudo (produtos, clientes, funcionários, entregas, vendas, etc.)

#Funcionário
Email: func@gmail.com
Senha: 123
Permissões: Pode realizar vendas e visualizar informações básicas.
```
