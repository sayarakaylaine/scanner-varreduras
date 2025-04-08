# 🔎 Scanner de Portas TCP/UDP

Este projeto é uma ferramenta de varredura de portas TCP e UDP com suporte a interface gráfica (Tkinter) e linha de comando. Ideal para diagnósticos de rede e testes de segurança em ambientes autorizados.

---

## 🛠 Funcionalidades
- Varredura de portas **TCP** e **UDP**
- Suporte à seleção de faixa de portas e múltiplos IPs
- Interface Gráfica (GUI) com **Tkinter**
- Exportação de resultados para **CSV**
- Execução com **multi-threading** para melhor desempenho

---

## 🖥 Tecnologias Utilizadas
- [Python 3](https://www.python.org/)
- **Tkinter** (nativo do Python) / Interface gráfica
- [Scapy](https://scapy.net/) / Varredura de portas UDP
- **Socket** (nativo do Python) / Varredura de portas TCP
- **Threading** (nativo do Python)

---

## 💻 Requisitos

- Python 3.7 ou superior
- Sistema Linux (suporte opcional para Windows/macOS)
- Permissões administrativas para envio de pacotes UDP

---

## 🛂 Instalação das Dependências
Antes de executar o programa, instale as bibliotecas necessárias:

```bash
pip install scapy
```

## 🚀 Como Executar
### Modo Linha de Comando (CLI)
Para rodar a varredura via terminal, utilize:

```bash
python scanner_varredura.py -i 192.168.1.1 -p 22,80,443 --tcp --udp
```

Parâmetros:
- `-i` ou `--ips`: Define os IPs a serem escaneados (separados por vírgula).
- `-p` ou `--ports`: Define as portas a serem verificadas (ex: `22,80,443` ou intervalo `1-1000`).
- `--tcp`: Habilita a varredura TCP.
- `--udp`: Habilita a varredura UDP.

### Modo Interface Gráfica (GUI)
Para abrir a interface gráfica:

```bash
python scanner_varredura.py
```
A interface permite inserir o IP, escolher portas e selecionar os modos de varredura TCP e UDP.

### ⚠ Aviso Legal
O uso deste scanner deve ser feito apenas em redes autorizadas. O uso indevido pode violar leis locais e resultar em penalidades.

