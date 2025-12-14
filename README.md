# 🖥️ System Monitoring HTML Report (Python)

Ce projet est un script Python qui collecte des informations système, analyse des fichiers sur le disque et génère un rapport HTML à partir d’un template.

Il permet d’avoir une vue rapide sur l’état de la machine (CPU, RAM, processus) ainsi que sur la répartition des types de fichiers dans un dossier donné.

---

## 📌 Fonctionnalités

- 🔧 Informations système
  - Nom de la machine
  - Système d’exploitation
  - Temps de fonctionnement (uptime)
  - Nombre d’utilisateurs connectés
  - Adresse IP principale

- 🧠 CPU
  - Nombre de cœurs logiques
  - Fréquence CPU
  - Pourcentage d’utilisation

- 💾 Mémoire
  - RAM totale
  - RAM utilisée
  - Pourcentage d’utilisation

- ⚙️ Processus
  - Top 3 des processus les plus consommateurs de CPU

- 📁 Analyse de fichiers
  - Comptage des fichiers `.txt`, `.py`, `.pdf`, `.jpg`
  - Calcul du pourcentage de chaque type de fichier

- 📝 Génération automatique d’un rapport HTML

---

## 🛠️ Technologies utilisées

- Python 3
- Bibliothèques :
  - psutil
  - platform
  - socket
  - datetime
  - os

---

## 📂 Structure du projet

- main.py
- template.html
- report.html
- README.md