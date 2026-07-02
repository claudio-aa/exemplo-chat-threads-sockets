import argparse
import socket
import sys
import threading


HOST_PADRAO = "127.0.0.1"
PORTA_PADRAO = 5000


def enviar_linha(sock, texto):
    sock.sendall((texto + "\n").encode("utf-8"))


def receber_mensagens(sock, parar):
    ficheiro = sock.makefile("r", encoding="utf-8")

    try:
        for linha in ficheiro:
            print("\r" + linha.rstrip())
            print("> ", end="", flush=True)
    except OSError:
        pass
    finally:
        parar.set()


def iniciar_cliente(host, porta, nome):
    parar = threading.Event()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, porta))

        thread = threading.Thread(target=receber_mensagens, args=(sock, parar), daemon=True)
        thread.start()

        enviar_linha(sock, nome)

        print(f"Ligado a {host}:{porta} como {nome}.")
        print("Escreve mensagens e carrega Enter. Escreve /quit para sair.")

        try:
            while not parar.is_set():
                mensagem = input("> ").strip()
                if mensagem == "":
                    continue

                enviar_linha(sock, mensagem)

                if mensagem.lower() == "/quit":
                    break

        except (KeyboardInterrupt, EOFError):
            try:
                enviar_linha(sock, "/quit")
            except OSError:
                pass

    parar.set()
    print("\nCliente desligado.")


def argumentos():
    parser = argparse.ArgumentParser(description="Cliente de chat por linha de comandos.")
    parser.add_argument("--host", default=HOST_PADRAO,
                        help=f"Endereço do servidor. Valor por omissão: {HOST_PADRAO}")
    parser.add_argument("--port", type=int, default=PORTA_PADRAO,
                        help=f"Porta TCP do servidor. Valor por omissão: {PORTA_PADRAO}")
    parser.add_argument("--name", help="Nome de conta a mostrar no chat.")
    return parser.parse_args()


if __name__ == "__main__":
    args = argumentos()
    nome = args.name

    if not nome:
        nome = input("Nome de conta: ").strip()

    if not nome:
        print("O nome de conta não pode ficar vazio.")
        sys.exit(1)

    iniciar_cliente(args.host, args.port, nome)
