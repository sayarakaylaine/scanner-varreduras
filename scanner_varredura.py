import socket
import argparse
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from scapy.all import sr1, IP, UDP, ICMP
import csv
from fpdf import FPDF

# Lista para armazenar os resultados
scan_results = []

# Função centralizada para exibir e registrar resultado
def add_result(ip, port, protocolo, estado, gui_output=None):
    scan_results.append({
        "ip": ip,
        "porta": port,
        "protocolo": protocolo,
        "estado": estado
    })
    mensagem = f"{ip} - Porta {port}/{protocolo} - {estado}"
    if gui_output:
        gui_output.after(0, lambda: gui_output.insert(tk.END, mensagem + "\n"))
    else:
        print(mensagem)


# Função para varredura TCP
def scan_tcp(ip, port, gui_output=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        estado = "ABERTA" if result == 0 else "FECHADA/FILTRADA"
    except Exception as e:
        estado = f"ERRO: {str(e)}"
    finally:
        sock.close()

    add_result(ip, port, "TCP", estado, gui_output)

# Função para varredura UDP com verificação de ICMP
def scan_udp(ip, port, gui_output=None):
    pkt = IP(dst=ip) / UDP(dport=port)
    try:
        response = sr1(pkt, timeout=2, verbose=0)
        if response is None:
            estado = "POTENCIALMENTE ABERTA/FILTRADA"
        elif response.haslayer(ICMP):
            icmp = response.getlayer(ICMP)
            if int(icmp.type) == 3 and int(icmp.code) == 3:
                estado = "FECHADA"
            else:
                estado = f"FILTRADA (ICMP type={icmp.type} code={icmp.code})"
        elif response.haslayer(UDP):
            estado = "ABERTA"
        else:
            estado = "FILTRADA (resposta inesperada)"
    except Exception as e:
        estado = f"ERRO: {str(e)}"

    add_result(ip, port, "UDP", estado, gui_output)

# Função para processar entrada de portas
def process_ports(port_arg):
    ports = []
    for part in port_arg.split(","):
        if "-" in part:
            start, end = map(int, part.split("-"))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

# Execução em modo terminal
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

# Função para interpretar a linha e separar IP, Porta, Protocolo, Estado
def parse_result_line(line):
    try:
        line = line.strip()
        if not line or line.startswith("[+]") or line.startswith("[ERRO]") or line.startswith("[FATAL]"):
            return None

        if "Porta TCP" in line:
            proto = "TCP"
        elif "Porta UDP" in line:
            proto = "UDP"
        else:
            return None

        parts = line.split()
        estado = parts[0].strip("[]")
        porta = parts[2]
        ip = parts[-1]
        return [ip, porta, proto, estado]
    except:
        return None

# Exporta resultados para CSV
def exportar_csv():
    if not scan_results:
        messagebox.showinfo("Exportação", "Nenhum resultado disponível para exportar.")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if caminho:
        with open(caminho, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "Porta", "Protocolo", "Estado"])
            for resultado in scan_results:
                writer.writerow([resultado["ip"], resultado["porta"], resultado["protocolo"], resultado["estado"]])
        messagebox.showinfo("Exportação", f"Resultados exportados com sucesso para {caminho}.")

# Exporta resultados para PDF
def exportar_pdf():
    if not scan_results:
        messagebox.showinfo("Exportação", "Nenhum resultado disponível para exportar.")
        return
    caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if caminho:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Relatório de Varredura de Portas", ln=True, align="C")
        pdf.ln(5)

        # Cabeçalho da tabela
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, "IP", 1, 0, "C", True)
        pdf.cell(30, 10, "Porta", 1, 0, "C", True)
        pdf.cell(40, 10, "Protocolo", 1, 0, "C", True)
        pdf.cell(80, 10, "Estado", 1, 1, "C", True)

        # Conteúdo da tabela
        for r in scan_results:
            pdf.cell(40, 10, str(r["ip"]), 1)
            pdf.cell(30, 10, str(r["porta"]), 1)
            pdf.cell(40, 10, str(r["protocolo"]), 1)
            pdf.cell(80, 10, str(r["estado"]), 1, ln=True)

        pdf.output(caminho)
        messagebox.showinfo("Exportação", f"Resultados exportados com sucesso para {caminho}.")

# Execução com interface gráfica Tkinter
def gui_mode():
    def start_scan():
        try:
            ip = ip_entry.get()
            ports = process_ports(ports_entry.get())
            results_text.delete(1.0, tk.END)
            scan_results.clear()

            if tcp_var.get():
                results_text.insert(tk.END, f"[+] Iniciando varredura TCP em {ip}...\n")
                for port in ports:
                    threading.Thread(target=scan_tcp, args=(ip, port, results_text)).start()

            if udp_var.get():
                results_text.insert(tk.END, f"[+] Iniciando varredura UDP em {ip}...\n")
                for port in ports:
                    threading.Thread(target=scan_udp, args=(ip, port, results_text)).start()
        except Exception as e:
            results_text.insert(tk.END, f"[ERRO] Falha ao iniciar varredura: {str(e)}\n")

    def clear_fields():
        ip_entry.delete(0, tk.END)
        ports_entry.delete(0, tk.END)
        results_text.delete(1.0, tk.END)
        scan_results.clear()

    root = tk.Tk()
    root.title("Scanner de Portas TCP/UDP")

    tk.Label(root, text="Endereço IP:").pack()
    ip_entry = tk.Entry(root, width=30)
    ip_entry.pack()

    tk.Label(root, text="Portas (ex: 22,80,443 ou 1-1000):").pack()
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
    tk.Button(button_frame, text="Exportar para CSV", command=exportar_csv).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Exportar para PDF", command=exportar_pdf).pack(side=tk.LEFT, padx=5)

    global results_text
    results_text = scrolledtext.ScrolledText(root, width=60, height=15)
    results_text.pack()

    root.mainloop()

# Ponto de entrada principal
def main():
    try:
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
    except Exception as e:
        print(f"[ERRO FATAL] Falha ao executar o programa: {str(e)}")

if __name__ == "__main__":
    main()