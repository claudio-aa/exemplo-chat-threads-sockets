# exemplo-chat-threads-sockets

Repositório de exemplo para aulas de Princípios e Técnicas em Cibersegurança.

## Propósito

Demonstra comunicação em rede com sockets TCP e concorrência com threads em Python.
Usado como material didático para alunos aprenderem:
- Modelo cliente/servidor com `socket`
- Concorrência com `threading`
- Comunicação bidirecional em tempo real (chat)

## Ficheiros

- `chat_server.py` — servidor TCP multi-cliente com threads, suporta comandos `/quit` e `/who`
- `chat_client.py` — cliente de linha de comandos com thread para receber mensagens em paralelo

## Comandos disponíveis no chat

| Comando | Descrição |
|---------|-----------|
| `/quit` | Sair do chat |
| `/who`  | Listar utilizadores ligados |

## Executar

```bash
# Servidor
python chat_server.py

# Cliente (noutra janela)
python chat_client.py --name Alice
```

## Repositório

https://github.com/claudio-aa/exemplo-chat-threads-sockets
