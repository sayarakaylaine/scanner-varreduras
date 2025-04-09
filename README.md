# Scanner de Portas TCP/UDP

Este projeto é uma ferramenta de varredura de portas TCP e UDP com suporte a interface gráfica (Tkinter) e linha de comando. Ideal para diagnósticos de rede e testes de segurança em ambientes **autorizados**.

## 🛠 Funcionalidades
- Varredura de portas **TCP** e **UDP**
- Suporte a **múltiplos IPs** e **faixas de portas**
- Interface Gráfica (GUI) intuitiva, com **Tkinter**
- **Exportação de relatório** no formato **.CSV** e **PDF**
- Execução **multi-thread** para maior desempenho
- Compatível com sistemas **Linux** (suporte opcional para Windows/macOS)

## 💻 Tecnologias Utilizadas
- [Python 3](https://www.python.org/)
- **Tkinter** – GUI nativa do Python
- [Scapy](https://scapy.net/) – Varredura de portas UDP
- **Socket** (módulo nativo) – Varredura TCP
- **Threading** – Execução paralela de varreduras
- **FPDF** – Geração de relatórios em PDF
- **CSV** – Geração de relatórios em formato tabular

## 🧾 Requisitos

- Python 3.7 ou superior
- Sistema Linux (preferencialmente)
- Permissão sudo (em alguns sistemas para pacotes UDP)
-  Internet (para instalar as dependências)
  
---

## 🛂 Instalação das Dependências
Antes de executar o programa, instale as bibliotecas necessárias:

```bash
pip install scapy
```

```bash
pip install fpdf
```

## 🚀 Como Executar
### Modo Interface Gráfica (GUI)
Para abrir a interface gráfica, digite no terminal:

```bash
python scanner_varredura.py
```

Como utilizar a interface gráfica:

1. Insira o(s) IP(s) desejado(s)
2. Defina a faixa ou lista de portas
3. Selecione TCP, UDP ou ambos
4. Clique em Iniciar Varredura
5. Exporte o relatório (opcional)

### Modo Linha de Comando (CLI)
Para rodar a varredura via terminal, sem interface:

```bash
python scanner_varredura.py -i 192.168.1.1 -p 22,80,443 --tcp --udp
```

Parâmetros a utilizar:
- `-i` ou `--ips`: Define os IPs a serem escaneados (separados por vírgula).
- `-p` ou `--ports`: Define as portas a serem verificadas (ex: `22,80,443` ou intervalo `1-1000`).
- `--tcp`: Habilita a varredura TCP.
- `--udp`: Habilita a varredura UDP.

---

## 📄 Exportação de Relatório
Ao finalizar a varredura na **GUI**, clique em **Exportar para CSV** ou **Exportar para PDF**. Será salvo um arquivo `.csv` ou `pdf` com os seguintes campos:

- IP
- Porta
- Protocolo
- Estado (Aberta, Fechada, Filtrada, etc.)

---

## 📦 Clonando o Repositório

```bash
git clone https://github.com/sayarakaylaine/scanner-varreduras.git
cd nome-do-repo
python scanner_varredura.py
```

---

## ⚠ Aviso Legal
Esta ferramenta é de uso **educacional** e não deve ser utilizada em redes sem autorização. O uso indevido pode configurar crime segundo leis locais

## 👩🏻‍💻 Autora
Desenvolvido por **`Sayara Kaylaine Oliveira Silva`**, sob orientação do professor **`Karan Luciano`**, no Instituto Federal de Rondônia (IFRO) - Campus Ji-Paraná.

