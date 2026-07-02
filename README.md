# Exemplo: chat com sockets e threads

Este exemplo mostra uma aplicação cliente-servidor simples em Python.

O chat usa Transmission Control Protocol (TCP), que é o protocolo de transporte usado aqui para manter uma ligação entre cliente e servidor.

Objetivo da aula:

- perceber a diferença entre servidor e cliente;
- ver um servidor a aceitar vários clientes ao mesmo tempo;
- perceber porque são usadas threads;
- observar quem se ligou, quem se desligou e quantos clientes estão ligados;
- ver mensagens identificadas pelo nome de conta de cada cliente.

## Ficheiros

- `chat_server.py`: servidor do chat.
- `chat_client.py`: cliente do chat.

## Como testar localmente

Abre vários terminais na pasta deste exemplo.

### Terminal 1: servidor

Windows:

```powershell
python chat_server.py
```

macOS ou Linux:

```bash
python3 chat_server.py
```

Deves ver algo como:

```text
[servidor] Chat disponível em 127.0.0.1:5000
```

### Terminal 2: primeiro cliente

Windows:

```powershell
python chat_client.py --name ana
```

macOS ou Linux:

```bash
python3 chat_client.py --name ana
```

### Terminal 3: segundo cliente

Windows:

```powershell
python chat_client.py --name bruno
```

macOS ou Linux:

```bash
python3 chat_client.py --name bruno
```

Agora escreve mensagens nos clientes.

Exemplo:

```text
ola
isto esta a funcionar?
/quit
```

## O que observar

No servidor:

- aparece quem se ligou;
- aparece quem se desligou;
- aparece quantos clientes estão ligados;
- aparecem as mensagens recebidas.

Nos clientes:

- cada mensagem recebida mostra o nome de quem enviou;
- mensagens do sistema indicam entradas e saídas;
- o comando `/quit` desliga o cliente.

## Alterações simples para experimentar

1. Mudar a porta do servidor:

```bash
python3 chat_server.py --port 6000
python3 chat_client.py --name ana --port 6000
```

2. Mudar o endereço do servidor:

```bash
python3 chat_client.py --host 127.0.0.1 --name ana
```

3. Experimentar nomes diferentes:

```bash
python3 chat_client.py --name equipa1
python3 chat_client.py --name equipa2
```

## Perguntas para discussão

1. Porque é que o servidor precisa de uma thread por cliente?
2. O que aconteceria se o servidor só conseguisse atender um cliente de cada vez?
3. O que pode correr mal se forem aceites clientes sem limite?
4. O chat cifra as mensagens? Isto seria aceitável numa aplicação real?
5. Que validação falta ao nome de conta?

## Desafio extra recomendado: comando `/who`

Objetivo: quando um cliente escreve `/who`, o servidor deve responder apenas a esse cliente com a lista dos nomes ligados.

Não é necessário fazer este desafio para perceber o exemplo base. Ele serve para treinar leitura de código e uma alteração pequena.

Pistas:

1. A lista de clientes está guardada no servidor.
2. O acesso à lista já usa `clientes_lock`.
3. A resposta deve ser enviada só ao cliente que escreveu `/who`.
4. A função `enviar_linha` já permite enviar uma linha para um cliente.

Resultado esperado:

```text
/who
[sistema] Clientes ligados: ana, bruno
```

Pergunta final: o que deve acontecer se ainda só estiver um cliente ligado?

## Nota de segurança

Este exemplo é didático. Não cifra mensagens, não autentica utilizadores e não deve ser usado em redes públicas.
