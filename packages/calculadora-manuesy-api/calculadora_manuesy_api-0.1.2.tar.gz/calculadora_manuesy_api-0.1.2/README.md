# API Calculadora

Esta é uma API simples de calculadora construída usando **FastAPI**. A API fornece endpoints para realizar operações aritméticas básicas, como adição, subtração, multiplicação e divisão.

## Funcionalidades

- Realizar operações aritméticas básicas:
  - Adição
  - Subtração
  - Multiplicação
  - Divisão
  - Fatorial
  - Exponencial
  - Raiz Quadrada
- Validação de entrada usando modelos do **Pydantic**.
- Lida com divisão por zero de forma adequada, com mensagens de erro apropriadas.

## Requisitos

- Python 3.9 ou superior
- Dependências listadas no arquivo `requirements.txt`:
  - `fastapi==0.95.2`
  - `pydantic==1.10.7`
  - `uvicorn==0.22.0`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/manuLemos/calculadoraAPI-lib.git
   cd calculadoraAPI-lib
   ```

2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Executando a Aplicação

1. Inicie o servidor FastAPI usando o Uvicorn:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Abra o navegador e navegue para:
   ```
   http://127.0.0.1:8000/docs
   ```
   Isso abrirá a documentação interativa da API (Swagger UI).

## Endpoints da API

### 1. **Adição**
   - **Endpoint**: `/add`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 5,
       "b": 3
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 8
     }
     ```

### 2. **Subtração**
   - **Endpoint**: `/subtract`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 5,
       "b": 3
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 2
     }
     ```

### 3. **Multiplicação**
   - **Endpoint**: `/multiply`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 5,
       "b": 3
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 15
     }
     ```

### 4. **Divisão**
   - **Endpoint**: `/divide`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 6,
       "b": 3
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 2
     }
     ```
   - **Tratamento de Erros**:
     - Se `b` for `0`, a API retornará:
       ```json
       {
         "detail": "Division by zero is not allowed"
       }
       ```
### 5. **Raiz Quadrada**
   - **Endpoint**: `/sqrt`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 9
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 3
     }
     ```
   - **Tratamento de Erros**:
     - Se `a` for menor que `0`, a API retornará:
       ```json
       {
         "detail": "A raiz quadrada de um número negativo não é real."
       }
       ```

### 6. **Exponencial**
   - **Endpoint**: `/exponent`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 2,
       "b": 4
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 16
     }
     ```

### 7. **Fatorial**
   - **Endpoint**: `/factorial`
   - **Método**: `POST`
   - **Corpo da Requisição**:
     ```json
     {
       "a": 5
     }
     ```
   - **Resposta**:
     ```json
     {
       "result": 120
     }
     ```

## Agradecimentos

- Construído com [FastAPI](https://fastapi.tiangolo.com/)
- Inspirado na simplicidade do Python para construir APIs.

Você pode instalar a biblioteca via pip:

  ```bash
  pip install calculadora-manuesy-api
  ```