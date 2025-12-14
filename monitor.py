import psutil
import platform
import socket
import datetime
import time
import getpass
import os

TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "report.html"


# ---------- SYSTEM INFO ----------
def get_system_info():
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot

    return {
        "machine_name": socket.gethostname(),
        "os_name": platform.platform(),
        "uptime": str(uptime).split('.')[0],
        "user_count": len(psutil.users()),
        "main_ip": socket.gethostbyname(socket.gethostname())
    }


# ---------- CPU INFO ----------
def get_cpu_info():
    freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0

    return {
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_frequency": int(freq),
        "cpu_usage": psutil.cpu_percent(interval=1)
    }


# ---------- MEMORY INFO ----------
def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "ram_total": round(mem.total / (1024**3), 2),
        "ram_used": round(mem.used / (1024**3), 2),
        "ram_percent": mem.percent
    }


# ---------- PROCESS INFO ----------
def get_top_processes():
    processes = []
    for process in psutil.process_iter(['pid', 'name']):
        try:
            name = process.info['name']
            if not name or name.strip() == "":
                continue
            # Mesure CPU percent sur 0.1 seconde
            cpu = process.cpu_percent(interval=0.1)
            processes.append({"name": name, "cpu_percent": cpu})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Tri par usage CPU décroissant
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    top = processes[:3]

    html_list = ""
    for p in top:
        html_list += f"<li>{p['name']} — {p['cpu_percent']}%</li>\n"

    return html_list




# ---------- FILE ANALYSIS ----------
path= r"C:\Users\nesri"
extensions = {".txt": 0, ".py": 0, ".pdf": 0, ".jpg": 0}
    
file_counts = {ext: 0 for ext in extensions}

for root, _, files in os.walk(path):
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                file_counts[ext] += 1

    # Calcul des pourcentages
    total_files = sum(file_counts.values())
    file_percentages = {
        ext: (count / total_files) * 100 if total_files > 0 else 0 for ext, count in file_counts.items()
        }


# ---------- TEMPLATE RENDERING ----------
def render_html(data):
    with open(TEMPLATE_FILE, "r") as t:
        template = t.read()

    for key, value in data.items():
        template = template.replace(f"{{{{ {key} }}}}", str(value))

    with open(OUTPUT_FILE, "w") as out:
        out.write(template)

    print(f"HTML report generated: {OUTPUT_FILE}")


# ---------- MAIN ----------
if __name__ == "__main__":
    system = get_system_info()
    cpu = get_cpu_info()
    memory = get_memory_info()
    top_proc = get_top_processes()

     # À adapter

    data = {
        **system,
        **cpu,
        **memory,
        "top_processes": top_proc,
        "txt_count": file_counts[".txt"],
        "py_count": file_counts[".py"],
        "pdf_count": file_counts[".pdf"],
        "jpg_count": file_counts[".jpg"],
        'txt_percentage': round(file_percentages['.txt'], 2),
        'py_percentage': round(file_percentages['.py'], 2),
        'pdf_percentage': round(file_percentages['.pdf'], 2),
        'jpg_percentage': round(file_percentages['.jpg'], 2),
        "generation_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    render_html(data)



