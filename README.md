# Clean Architecture

A Clean Architecture (ou Arquitetura Limpa) é uma forma de organizar seu código focando em separar bem as responsabilidades e isolar regras de negócio das dependências externas (como banco de dados, web, APIs, etc).

**✅ Vantagens:**
- Código muito bem organizado
- Regras de negócio ficam separadas de banco, APIs etc.
- Fácil de testar.

**❌Desvanatgens:**
- Curva de aprendizado maior
- Pode parecer overkill se o projeto for pequeno.

<BR>

**🔧 Ideal quando:** o projeto vai crescer, mas o time ainda é pequeno e quer manter qualidade desde o início.

<BR>

## Ideia central:
Você separa o sistema em camandas e depende do centro para fora, nunca o contrário.

    [ Regra de Negócio Pura ]  <--- não depende de nada
    ⬇
    [ Casos de Uso ]
    ⬇
    [ Adaptadores ] (ex: views, repos)
    ⬇
    [ Frameworks / Externos ] (ex: Flask, banco, API)

<BR>

## Camadas explicadas:

| Camada | O que Faz | Exemplo em Python
| ----------- | ----------- | -----------
| Entities | Regras de negócio puras | Classes com lógica (ex: Pedido, cliente)
| Use Cases | Casos de uso específicos | CriarPedido, CalcularDesconto
| Interface | Adaptadores entre regras e o mundo externo | Repositórios, serializadores
| Frameworks & Drivers | Tudo externo | Flask/FastAPI, banco, Redis, etc
| | | 

<BR>

**✅ Vantagens na prática:**
- Você pode trocar Flask por FastAPI e nada muda nas regras
- Pode testar o negócio sem rodar servidor.
- É fácil migrar banco, trocar ORM ou conectar novas saídas (ex: fila, API externa).

<BR>

## Sistema de Pedidos (Loja simples) - Exemplo de aplicação
**Funcionalidade:**
- Criar pedido (cliente + itens)
- Calcular total
- Listar pedidos

**Conceitos aplicados:**
- Entidade: Pedido, Item
- Use Case: criar_pedido(), listar_pedidos()
- Adapter: RepositorioPedidoMemoria ou SQL
- Framework: API Flask

<BR>

## 🟢 Camada: Entities (Entidades / Regras de negócio)
**📌 O que é?**
A camada de Entities representa o coração do sistema. aqui ficam as regras puras de negócio: cálculos, validações, estruturas, comportamentos. essa camada:

- **Não depende de nada externo** (nem Flask, nem banco, nem JSON, nada)
- Pode ser usada em qualquer aplicação: CLI, WEB, Mobile, API.
- É a parte mais testável e reutilizável do sistema.

<BR>

### 🛒 Nosso sistema: Sistema de Pedidos

**🧠Vamos pensar o seguinte:**

- Um cliente faz um pedido
- Cada pedido tem vários itens
- Cada item tem um nome e preço
- O pedido pode calcular o total

<BR>

**📁 Estrutura da pasta:**

    project/
    └── entities/
        ├── item.py
        └── pedido.py

<BR>

**🧩 Concluindo sobre Entities (Entidades):**

- Entidade Item: só tem nome e preço

- Entidade Pedido:
    - Guarda o nome do cliente
    - Tem uma lista de itens
    - Tem uma regra de negócio: calcular total

<BR>

## 🟢 Camada: Use cases (Casos de uso)
**📌 O que é?**

A camada de Use Cases orquestra o que o sistema deve fazer com base nas regras de negócio. Ela usa as entidades (do centro) para aplicar as ações específicas do sistema.

**🧠 Pense assim:**

- A entidade Pedido sabe calcular o total.
- Mas o use case vai dizer "crie um pedido com esses itens e salve".

**ou seja:**

- **Entidade** ➡ comportamento puro
- **Use case** ➡ ação que resolve um objetivo real

**📁 Estrutura da pasta:**

    project/
    └── use_cases/
        └──criar_pedido.py

<BR>

**🧩 Concluindo sobre Use Cases:**

- Define ações completas do sistema.
- Usa entidades para aplicar lógica.
- Depende de interfaces/abstrções, nunca de coisas concretas (como banco ou Flask)
- É muito fácil de testar com mocks.

## 🟢 Camada: Adapter (Interface)

**🎯 As abstrações como Factorys, Repositórios, Interfaces, Gateways etc. ficam na nessa camada.**

**📌 Função da camada de Adapters:**

Essa camada "Traduza" o mundo externo (Frameworks, banco de dados, APIs, etc.) para o que os Use cases entendem.

**ou seja:**
- Os Use cases não sabem como salvar no banco, eles só dizem: "Salve usando esse repositório".
- A camada Adapters implementa essa interface e de fato salva no SQLite, PostgreSQL, etc.
- Factorys entram aqui também, caso você precise escolher qual implementação usar ou criar objetos com alguma lógica específica.
 
<BR>

**Em resulmo:**

| Papel | Onde fica? | Exemplo
| ---------| ---------| ---------
| Interface (abstração) | Interface Adapters | RepositorioPedido
| Implementação concreta | Interface Adpters | RepositorioMemoria, RepositorioSQL
| Factory (Opcional) | Interface Adapters | get_repositorio(tipo)
| Use Case | Casos de Uso | Recebe a interface e usa
| Entidade | entities | Não sabe nada disso
|||

<BR>

**📁 Estrutura de diretórios:**

    project/
    ├── entities/
    ├── use_cases/
    ├── interfaces/
    │   └── repositorio.py        ← interface
    └── adapters/
        └── repositorio_memoria.py  ← implementação

<BR>

**🧠 Elementos da camada:**

| Elemento | O que faz
| ---------| ---------
| RepositorioPedido | Define como os casos de uso esperam se comunicar com o mundo externo
| RepositorioMemoria | Implementa essa interface, usando uma lista na memória
| get_repositorio() | Dá flexibilidade pra trocar o tipo de armazenamento depois
|||

## 🟢 Camada: Frameworks & Delivery
**📌 O que é?**

Essa camada lida com frameworks e tecnologias externas:
 - Flask, FastAPI, Django, etc.
 - Interfaces web (HTTP)
 - Controllers, Views, Rotas
 - Banco de dados real (Se não abstraido via adapter)
 - WebSockets, CLI, qualquer forma de entrada/saída

<BR>

⚠️ Ela é a mais externa e descartável – se você trocar Flask por FastAPI, o núcleo continua igual.

**🎯 O que faz?**

Criar um pequeno servidor Flask com um endpoint POST /pedidos para:
- Receber um pedido em JSON
- Criar o pedido com o use case
- Usar o repositório de memória pra salvar
- Retornar o total e os dados do pedido

<BR>

**📁 Estrutura final:**

    project/
    ├── adapters/
    │   ├── repositorio_memoria.py         # Repositório que salva os pedidos na memória
    │   └── repositorio_factory.py         # Factory para escolher repositório
    ├── entities/
    │   ├── item.py                        # Entidade Item (nome, preço)
    │   └── pedido.py                      # Entidade Pedido (cliente, itens, total)
    ├── interfaces/
    │   └── repositorio.py                 # Interface do repositório
    ├── use_cases/
    │   └── criar_pedido.py                # Caso de uso para criar pedido
    └── main.py                            # Camada web com Flask


