# 🚀 Nmap XML Parser (Fast Recon Tool)

A high-performance Nmap XML parsing tool designed for **large-scale external penetration testing**. It converts raw Nmap XML output into clean, actionable results like:

```
ip:port
ip:port/service(version)
```

Built for speed, flexibility, and automation — perfect for integrating into modern recon workflows.

---

## 🔥 Features

* ⚡ **Fast streaming XML parsing** (memory efficient)
* 🧵 **Multi-file support with threading**
* 🎯 **Port filtering** (`-p 80,443`)
* 🔍 **Service filtering** (`--service-filter http,ssh`)
* 🧠 **Regex matching** (`--match apache`)
* 🌐 **Web port auto-detection** (`--web`)
* 📦 **JSON output** (`--json`)
* 📊 **CSV export** (`--csv`)
* 🎨 **Colorized terminal output** (`--color`)
* 🔎 **Service + version detection** (`-s`)
* 📂 Works with **stdin or files**

---

## 📥 Installation

```bash
git clone https://github.com/yourusername/nmap-xml-parser.git
cd nmap-xml-parser
chmod +x nmap-xml-parser.py
```

---

## ⚙️ Usage

```bash
python nmap-xml-parser.py -l scan.xml [options]
```

---

## 📌 Examples

### ✅ Basic

```bash
python nmap-xml-parser.py -l scan.xml
```

```
192.168.1.1:80
192.168.1.1:443
```

---

### 🔎 Show service + version

```bash
python nmap-xml-parser.py -l scan.xml -s
```

```
192.168.1.1:80/http(Apache 2.4.41)
```

---

### 🎯 Filter ports

```bash
python nmap-xml-parser.py -l scan.xml -p 80,443
```

---

### 🔍 Filter services

```bash
python nmap-xml-parser.py -l scan.xml --service-filter http,ssh
```

---

### 🧠 Regex match (Apache)

```bash
python nmap-xml-parser.py -l scan.xml --match apache -s
```

---

### 🌐 Only web services

```bash
python nmap-xml-parser.py -l scan.xml --web -s
```

---

### 🧵 Multi-file parsing

```bash
python nmap-xml-parser.py -l scan1.xml scan2.xml -t 8
```

---

### 📦 JSON output

```bash
python nmap-xml-parser.py -l scan.xml --json
```

---

### 📊 CSV export

```bash
python nmap-xml-parser.py -l scan.xml --csv -o output.csv
```

---

### 🎨 Color output

```bash
python nmap-xml-parser.py -l scan.xml -s --color
```

---

### 💣 Real-world usage

```bash
python nmap-xml-parser.py -l *.xml --web --match nginx -s --color -t 10
```

---

## ⚡ Use Case

This tool is highly effective during **large-scale external penetration testing**, where multiple Nmap scans generate massive XML outputs. It helps:

* Quickly identify exposed services
* Filter relevant attack surfaces
* Integrate with tools like `httpx`, `nuclei`, etc.
* Reduce manual effort in recon workflows

---

## 🛠️ Options

| Option             | Description            |
| ------------------ | ---------------------- |
| `-l`               | Input XML file(s)      |
| `-o`               | Output file            |
| `-p`               | Filter ports           |
| `-s`               | Show service + version |
| `--service-filter` | Filter by service      |
| `--match`          | Regex match            |
| `--web`            | Only web ports         |
| `--json`           | JSON output            |
| `--csv`            | CSV output             |
| `--color`          | Colorized output       |
| `-t`               | Threads                |

---

## 🧠 Why This Tool?

Compared to traditional pipelines (`xmllint + grep + sed`), this tool is:

* ⚡ Faster
* 🧼 Cleaner
* 🧠 Smarter filtering
* 🔗 Easily scriptable

---

## 📜 License

MIT License

---

## ⭐ Support

If you find this useful, give it a ⭐ on GitHub!
