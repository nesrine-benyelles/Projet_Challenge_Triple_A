import psutil
import platform
import socket
import datetime
import getpass
import os

TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "report.html"


# ---------- SYSTEM INFO ----------
def get_system_info():
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot

    return {
        "machine_name": platform.node(),
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
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(process.info)
        except:
            pass

    # Sort descending by CPU usage
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)
    top = processes[:3]

    html_list = ""
    for p in top:
        html_list += f"<li>{p['name']} — {p['cpu_percent']}%</li>\n"

    return html_list


# ---------- FILE ANALYSIS ----------
def analyze_files(path):
    extensions = {".txt": 0, ".py": 0, ".pdf": 0, ".jpg": 0}

    for root, dirs, files in os.walk(path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in extensions:
                extensions[ext] += 1

    total = sum(extensions.values())

    percent = {ext: round((count / total * 100), 2) if total > 0 else 0
               for ext, count in extensions.items()}

    return extensions, percent, total


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

    file_counts, file_percent, total = analyze_files("/home")  # À adapter

    data = {
        **system,
        **cpu,
        **memory,
        "top_processes": top_proc,
        "txt_count": file_counts[".txt"],
        "py_count": file_counts[".py"],
        "pdf_count": file_counts[".pdf"],
        "jpg_count": file_counts[".jpg"],
        "txt_percent": file_percent[".txt"],
        "py_percent": file_percent[".py"],
        "pdf_percent": file_percent[".pdf"],
        "jpg_percent": file_percent[".jpg"],
        "total_files": total,
        "generation_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    render_html(data)
