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
    machine_name = socket.gethostname()

    return {
        "machine_name": machine_name,  
        "os_name": platform.platform(), # on recupere la version de systeme d'exploitation utiliser par ma machine
         "uptime": str(uptime).split('.')[0], # je cast ma date en string et j'applique la fonction split pour enlever les microsecondes de ma date 
        "user_count": len(psutil.users()), # on compte le nombre des users connectes a la machine 
        "main_ip": socket.gethostbyname(machine_name)  #renvoi l'adresse IP en donnant le nom de la machine en parametre
    }


# ---------- CPU INFO ----------
def get_cpu_info():
    freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
    # on recupere la frequence du CPU (la condition if c'est pour verifier la variable pour que ça ne sois pas null (condition de secours))
    return {
        "cpu_cores": psutil.cpu_count(logical=True),# retourne le nombre de coeurs du CPU (logical "nombre de coeurs logiques (threads)")
        "cpu_frequency": int(freq), # retourne la frequence de CPU 
        "cpu_usage": psutil.cpu_percent(interval=60) # retourne le pourcetande d'utilisation du CPU sur un intervalle de 1 minute
    }


# ---------- MEMORY INFO ----------
def get_memory_info():
    mem = psutil.virtual_memory() # la variable permet de recuperer la memoire total physique disponible 
    return {
        "ram_total": round(mem.total / (1024**3), 2),# on recupere RAM totale (en GB) pour ça on utise la fonction round et on prend 2 chiffre apres la virgule 
        "ram_used": round(mem.used / (1024**3), 2), # on recupere RAM utilisée (en GB) 
        "ram_percent": mem.percent # on recupere le pourcentage de la RAM utiliser 
    }


# ---------- PROCESS INFO ----------
def get_top_processes():
    processes = []# on initialise une liste qui contiendra tous les processes 
    cpu_count = psutil.cpu_count(logical=True) # nombre de coeurs loqiques du CPU 

    #  Amorçage de la mesure CPU
    # le premier test pour mesurer correctement le pourcentage CPU
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    #  Petite pause pour laisser le temps de mesurer
    time.sleep(0.2)

    # deuxieme iteration pour recuperer le nom et l'utilisation CPU reelle 
    for process in psutil.process_iter(['pid', 'name']):
        try:
            name = process.info['name']

            # Exclusions
            if not name or name.strip() == "":
                continue

            # CPU normalisé sur 100 %
            cpu = process.cpu_percent(None) / cpu_count
            # ajouter uniquement si le processus consomme du CPU (> 0 %)
            if cpu > 0:
                processes.append({
                    "name": name,
                    "cpu_percent": round(cpu, 1)
                })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Trier par CPU décroissant
    processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
     # ne garde que les 3 processus les plus gourmants 
    top = processes[:3]

    # Génération HTML
    html_list = ""
    for p in top:
        #affichage avec le nom en gras et l'utilisation CPU avec " : "
        html_list += f"<li><strong>{p['name']}</strong> : {p['cpu_percent']}%</li>\n"


    return html_list # retourne la liste html complete 

# ---------- FILE ANALYSIS ----------
path= r"C:\Users\nesri"  # contient le chemin de dossier ("r" signifie raw string ignore les caracteres d'echappement )
extensions = {".txt": 0, ".py": 0, ".pdf": 0, ".jpg": 0} # dictionnaire qui  contient les types de fichiers qu'on veut compter (0 sert a initialiser le compteur )
    
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
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as t:
        template = t.read()

    for key, value in data.items():
        template = template.replace(f"{{{{ {key} }}}}", str(value))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write(template)

    print(f"HTML report generated: {OUTPUT_FILE}")


# ---------- MAIN ----------
# main c'est pour executer toutes les fonctions que j'ai declarer ci-dessous
if __name__ == "__main__":
    system = get_system_info()
    cpu = get_cpu_info()
    memory = get_memory_info()
    top_proc = get_top_processes()

    

    data = {
        **system,# "**" permet de fusionner 2 dictionnaires en un seul 
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



