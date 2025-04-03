# Scanner de Portas TCP/UDP
Este projeto é um scanner de portas TCP e UDP que permite verificar o estado de portas abertas, fechadas ou filtradas em dispositivos de rede. O programa pode ser executado tanto via linha de comando (CLI) quanto por uma interface gráfica (GUI) desenvolvida com Tkinter.

🛠 Funcionalidades

- Varredura de portas TCP e UDP

- Suporte a múltiplos IPs e intervalos de portas

- Interface gráfica para facilitar o uso

- Execução em threads para melhor desempenho

- Tecnologias Utilizadas

Python

Tkinter (Interface gráfica)

Scapy (Varredura de portas UDP)

Socket (Varredura de portas TCP)

📦 Instalação das Dependências

Antes de executar o programa, instale as bibliotecas necessárias:

pip install scapy

🚀 Como Executar

Modo Linha de Comando (CLI)

Para rodar a varredura via terminal, utilize:

python scanner_varredura.py -i 192.168.1.1 -p 22,80,443 --tcp --udp

Parâmetros:

-i ou --ips: Define os IPs a serem escaneados (separados por vírgula).

-p ou --ports: Define as portas a serem verificadas (ex: 22,80,443 ou intervalo 1-1000).

--tcp: Habilita a varredura TCP.

--udp: Habilita a varredura UDP.

Modo Interface Gráfica (GUI)

Para abrir a interface gráfica:

python scanner_varredura.py

A interface permite inserir o IP, escolher portas e selecionar os modos de varredura TCP e UDP.

⚠ Aviso Legal

O uso deste scanner deve ser feito apenas em redes autorizadas. O uso indevido pode violar leis locais e resultar em penalidades.
