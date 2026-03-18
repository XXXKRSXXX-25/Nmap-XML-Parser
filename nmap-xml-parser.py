#!/usr/bin/env python3
import sys
import argparse
import xml.etree.ElementTree as ET
import json
import csv
import re
from concurrent.futures import ThreadPoolExecutor

# ANSI colors
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

WEB_PORTS = {
    "80", "443", "8080", "8443", "8000",
    "8888", "3000", "5000", "7001", "9000"
}


def parse_list_filter(value):
    if not value:
        return None
    return set(v.strip().lower() for v in value.split(","))


def parse_file(xml_input, args):
    results = []

    try:
        context = ET.iterparse(xml_input, events=("end",))

        for _, elem in context:
            if elem.tag == "host":

                status = elem.find("status")
                if status is None or status.get("state") != "up":
                    elem.clear()
                    continue

                # Get IP
                ip = None
                for addr in elem.findall("address"):
                    if addr is not None and addr.get("addrtype") == "ipv4":
                        ip = addr.get("addr")
                        break

                if ip is None:
                    elem.clear()
                    continue

                # Extract domain ONCE per host (optimized)
                domain = ""
                hostnames = elem.find("hostnames")
                if hostnames is not None:
                    hostname = hostnames.find("hostname")
                    if hostname is not None:
                        domain = hostname.get("name", "")

                ports = elem.find("ports")
                if ports is None:
                    elem.clear()
                    continue

                for port in ports.findall("port"):
                    state = port.find("state")
                    if state is None or state.get("state") != "open":
                        continue

                    portid = port.get("portid")
                    if not portid:
                        continue

                    # Web filter
                    if args.web and portid not in WEB_PORTS:
                        continue

                    # Port filter
                    if args.ports and portid not in args.ports:
                        continue

                    service_name = ""
                    version = ""

                    service = port.find("service")
                    if service is not None:
                        service_name = service.get("name", "").lower()

                        product = service.get("product", "")
                        ver = service.get("version", "")
                        extra = service.get("extrainfo", "")

                        version = " ".join(
                            x for x in [product, ver, extra] if x
                        ).strip()

                    # Service filter
                    if args.service_filter and service_name not in args.service_filter:
                        continue

                    # Regex match
                    if args.match:
                        text = f"{service_name} {version}".lower()
                        if not re.search(args.match, text):
                            continue

                    results.append({
                        "ip": ip,
                        "port": portid,
                        "service": service_name,
                        "version": version,
                        "domain": domain
                    })

                elem.clear()

    except Exception as e:
        print(f"[ERROR] {xml_input}: {e}", file=sys.stderr)

    return results


def parse_nmap(inputs, args):
    all_results = []

    if len(inputs) > 1:
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = [executor.submit(parse_file, f, args) for f in inputs]
            for future in futures:
                all_results.extend(future.result())
    else:
        all_results.extend(parse_file(inputs[0], args))

    return all_results


def output_results(results, args):
    # JSON
    if args.json:
        write_output(json.dumps(results, indent=2), args)
        return

    # CSV
    if args.csv:
        fields = ["ip", "port", "service", "version", "domain"]
        if args.output:
            with open(args.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(results)
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=fields)
            writer.writeheader()
            writer.writerows(results)
        return

    # Default output
    lines = []
    for r in results:
        line = f"{r['ip']}:{r['port']}"

        # Domain
        if args.domain and r.get("domain"):
            line += f"/{r['domain']}"

        # Service + version
        if args.service and r["service"]:
            line += f"/{r['service']}"
            if r["version"]:
                line += f"({r['version']})"

        # Color output
        if args.color and not args.output:
            dom = f"/{r['domain']}" if args.domain and r.get("domain") else ""
            svc = ""
            if args.service:
                svc = f"/{r['service']}"
                if r["version"]:
                    svc += f"({r['version']})"

            line = f"{GREEN}{r['ip']}{RESET}:{CYAN}{r['port']}{RESET}{dom}{YELLOW}{svc}{RESET}"

        lines.append(line)

    write_output("\n".join(lines), args)


def write_output(data, args):
    if args.output:
        with open(args.output, "w") as f:
            f.write(data + "\n")
    else:
        print(data)


def main():
    parser = argparse.ArgumentParser(
        description="Ultimate Nmap XML parser 🔥 by Ravi Solanki",
        usage="%(prog)s -l scan.xml [options]"
    )

    parser.add_argument("-l", "--list", nargs="+", help="Input XML file(s)")
    parser.add_argument("-d", "--domain", action="store_true", help="Show domain")
    parser.add_argument("-o", "--output", help="Output file")

    parser.add_argument("-p", "--ports", help="Filter ports (80,443)")
    parser.add_argument("-s", "--service", action="store_true")

    parser.add_argument("--service-filter", help="Filter services (http,ssh)")
    parser.add_argument("--match", help="Regex match (apache)")

    parser.add_argument("--web", action="store_true", help="Only web ports")

    parser.add_argument("--json", action="store_true")
    parser.add_argument("--csv", action="store_true")
    parser.add_argument("--color", action="store_true")

    parser.add_argument("-t", "--threads", type=int, default=4)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    args.ports = parse_list_filter(args.ports)
    args.service_filter = parse_list_filter(args.service_filter)

    inputs = args.list if args.list else [sys.stdin]

    results = parse_nmap(inputs, args)
    output_results(results, args)


if __name__ == "__main__":
    main()