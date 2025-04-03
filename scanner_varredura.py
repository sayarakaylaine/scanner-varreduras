import socket
import argparse
import threading
import tkinter as tk
from tkinter import scrolledtext
from scapy.all import sr1, IP, UDP

# Função para varredura TCP
def scan_tcp(ip, port, gui_output=None):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1) # Tempo de resposta
    result = sock.connect_ex((ip, port))  # Tenta conectar na porta
    message = f"[ABERTA] Porta TCP {port}" if result == 0 else f"[FECHADA/FILTRADA] Porta TCP {port}"
    
    if gui_output:
        gui_output.insert(tk.END, message + "\n")  # Exibe resultado na interface gráfica
    else:
        print(message)
    
    sock.close()

# Função para varredura UDP
def scan_udp(ip, port, gui_output=None):
    pkt = IP(dst=ip) / UDP(dport=port)
    response = sr1(pkt, timeout=1, verbose=0)  # Envia pacote UDP
    
    if response is None:
        message = f"[FILTRADA] Porta UDP {port}"
    elif response.haslayer(UDP):
        message = f"[ABERTA] Porta UDP {port}"
    else:
        message = f"[FECHADA] Porta UDP {port}"
    
    if gui_output:
        gui_output.insert(tk.END, message + "\n")  # Exibe resultado na interface gráfica
    else:
        print(message)

# Processa intervalo de portas
def process_ports(port_arg):
    ports = []
    for part in port_arg.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

# Modo para executar no terminal
def cli_mode(args):
    ips = args.ips.split(",")
    ports = process_ports(args.ports)
    scan_tcp_enabled = args.tcp or not args.udp
    scan_udp_enabled = args.udp
    
    threads = []
    for ip in ips:
        print(f"\n[+] Iniciando varredura em {ip}...")
        for port in ports:
            if scan_tcp_enabled:
                t = threading.Thread(target=scan_tcp, args=(ip, port))
                threads.append(t)
                t.start()
            if scan_udp_enabled:
                t = threading.Thread(target=scan_udp, args=(ip, port))
                threads.append(t)
                t.start()
    
    for t in threads:
        t.join()

# Modo para executar na interface gráfica
def gui_mode():
    def start_scan():
        ip = ip_entry.get()
        ports = list(map(int, ports_entry.get().split(",")))
        results_text.delete(1.0, tk.END)  # Limpa a área de saída
        
        if tcp_var.get():
            results_text.insert(tk.END, f"\n[+] Iniciando varredura TCP em {ip}...\n")
            for port in ports:
                threading.Thread(target=scan_tcp, args=(ip, port, results_text)).start()
        
        if udp_var.get():
            results_text.insert(tk.END, f"\n[+] Iniciando varredura UDP em {ip}...\n")
            for port in ports:
                threading.Thread(target=scan_udp, args=(ip, port, results_text)).start()
    
    def clear_fields():
        ip_entry.delete(0, tk.END)  # Limpa o campo de IP
        ports_entry.delete(0, tk.END)  # Limpa o campo de portas
        results_text.delete(1.0, tk.END)  # Limpa a área de saída

    root = tk.Tk()
    root.title("Scanner de Portas TCP/UDP")

    tk.Label(root, text="Endereço IP:").pack()
    ip_entry = tk.Entry(root, width=30)
    ip_entry.pack()

    tk.Label(root, text="Portas (ex: 22,80,443):").pack()
    ports_entry = tk.Entry(root, width=30)
    ports_entry.pack()

    tcp_var = tk.BooleanVar(value=True)
    udp_var = tk.BooleanVar(value=False)

    tk.Checkbutton(root, text="Varredura TCP", variable=tcp_var).pack()
    tk.Checkbutton(root, text="Varredura UDP", variable=udp_var).pack()

    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame, text="Iniciar Varredura", command=start_scan).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Limpar Campos", command=clear_fields).pack(side=tk.LEFT, padx=5)

    global results_text
    results_text = scrolledtext.ScrolledText(root, width=50, height=10)
    results_text.pack()
    
    root.mainloop()

# Ponto de entrada do programa
def main():
    parser = argparse.ArgumentParser(description="Varredura de Portas TCP e UDP")
    parser.add_argument("-i", "--ips", help="Endereços IPs (separados por vírgula)")
    parser.add_argument("-p", "--ports", help="Portas a escanear (ex: 22,80,443 ou 1-1000)")
    parser.add_argument("--udp", action="store_true", help="Habilita varredura UDP")
    parser.add_argument("--tcp", action="store_true", help="Habilita varredura TCP")
    args = parser.parse_args()
    
    if args.ips and args.ports:
        cli_mode(args)
    else:
        gui_mode()

if __name__ == "__main__":
    main()
