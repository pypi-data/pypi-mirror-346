# Calculadora com FastAPI

## 📝 Descrição

Esta aplicação é uma **API REST** desenvolvida com **FastAPI** que realiza operações matemáticas básicas: soma, subtração, multiplicação e divisão. Cada operação é exposta como um **endpoint** que aceita dois números como entrada e retorna o resultado da operação.

## ✨ Funcionalidades

- Operações básicas (Soma, Subtração, Multiplicação, Divisão)

## 🔚 Endpoints

### 1. Soma 

- URL: /add
- Método: POST
- Descrição: Soma dois números.
- Exemplo de corpo da Req:

```
{
  "value1": 10,
  "value2": 5
}
```

- Exemplo de resposta:

```
{
  "result": 15
}
```

### 2. Subtração 

- URL: /subtract
- Método: POST
- Descrição: Subtrai o segundo número do primeiro.
- Exemplo de corpo da Req:

```
{
  "value1": 10,
  "value2": 5
}
```

- Exemplo de resposta:

```
{
  "result": 5
}
```

### 3. Multiplicação 

- URL: /multiply
- Método: POST
- Descrição: Multiplica dois números.
- Exemplo de corpo da Req:

```
{
  "value1": 10,
  "value2": 5
}
```

- Exemplo de resposta:

```
{
  "result": 50
}
```

### 4. Divisão 

- URL: /divide
- Método: POST
- Descrição: Divide o primeiro número pelo segundo. Retorna um erro se o divisor for zero.
- Exemplo de corpo da Req:

```
{
  "value1": 10,
  "value2": 5
}
```

- Exemplo de resposta:

```
{
  "result": 2.0
}
```

- Erro para Divisão por Zero:

```
{
  "result": "Error: Division by zero is not allowed."
}
```

## ▶️ Como Executar

1. Clone o repositório

2. Instale as dependências:

```
pip install fastapi uvicorn
```

3. Execute o servidor:

```
uvicorn main:app --reload
```

## 📌 Observações

- Certifique-se de que o servidor está rodando antes de enviar requisições.
- Utilize a documentação interativa para testar os endpoints de forma mais fácil.
