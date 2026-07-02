import argparse
import socket
import threading


HOST_PADRAO = "127.0.0.1"
PORTA_PADRAO = 5000

clientes = {}
clientes_lock = threading.Lock()


def enviar_linha(sock, texto):
    sock.sendall((texto + "\n").encode("utf-8"))


def contar_clientes():
    with clientes_lock:
        return len(clientes)


def nomes_ligados():
    with clientes_lock:
        return set(clientes.values())


def registar_cliente(sock, nome):
    nome_base = nome.strip() or "sem_nome"
    nome_final = nome_base
    contador = 2

    with clientes_lock:
        nomes = set(clientes.values())
        while nome_final in nomes:
            nome_final = f"{nome_base}_{contador}"
            contador += 1
        clientes[sock] = nome_final
        total = len(clientes)

    return nome_final, total


def remover_cliente(sock):
    with clientes_lock:
        nome = clientes.pop(sock, None)
        total = len(clientes)

    try:
        sock.close()
    except OSError:
        pass

    return nome, total


def difundir(texto, ignorar=None):
    with clientes_lock:
        destinos = list(clientes.keys())

    for destino in destinos:
        if destino is ignorar:
            continue
        try:
            enviar_linha(destino, texto)
        except OSError:
            remover_cliente(destino)


def tratar_cliente(sock, endereco):
    ficheiro = sock.makefile("r", encoding="utf-8")
    nome = None

    try:
        nome_recebido = ficheiro.readline()
        if not nome_recebido:
            return

        nome, total = registar_cliente(sock, nome_recebido)
        print(f"[servidor] {nome} ligou-se de {endereco[0]}:{endereco[1]}. Ligados: {total}")

        enviar_linha(sock, f"[sistema] Entraste no chat como {nome}. Escreve /quit para sair.")
        difundir(f"[sistema] {nome} entrou no chat. ({total} ligados)", ignorar=sock)

        for linha in ficheiro:
            mensagem = linha.strip()
            if mensagem == "":
                continue
            if mensagem.lower() == "/quit":
                break
            if mensagem.lower() == "/who":
                nomes = ", ".join(sorted(nomes_ligados()))
                enviar_linha(sock, f"[sistema] Ligados: {nomes}")
                continue

            print(f"[{nome}] {mensagem}")
            difundir(f"[{nome}] {mensagem}")

    except ConnectionResetError:
        pass
    finally:
        nome_removido, total = remover_cliente(sock)
        if nome_removido:
            print(f"[servidor] {nome_removido} desligou-se. Ligados: {total}")
            difundir(f"[sistema] {nome_removido} saiu do chat. ({total} ligados)")


def iniciar_servidor(host, porta):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((host, porta))
    servidor.listen()

    print(f"[servidor] Chat disponível em {host}:{porta}")
    print("[servidor] Carrega Ctrl+C para parar.")

    try:
        while True:
            sock, endereco = servidor.accept()
            thread = threading.Thread(target=tratar_cliente, args=(sock, endereco), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[servidor] A terminar.")
    finally:
        servidor.close()


def argumentos():
    parser = argparse.ArgumentParser(description="Servidor de chat com sockets e threads.")
    parser.add_argument("--host", default=HOST_PADRAO, help=f"Endereço onde o servidor escuta. Valor por omissão: {HOST_PADRAO}")
    parser.add_argument("--port", type=int, default=PORTA_PADRAO, help=f"Porta Transmission Control Protocol (TCP). Valor por omissão: {PORTA_PADRAO}")
    return parser.parse_args()


if __name__ == "__main__":
    args = argumentos()
    iniciar_servidor(args.host, args.port)
