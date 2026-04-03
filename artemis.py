#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TOOL DEFINITIVE - Massive OSINT Suite v1.0
50 Tools | Kali Linux & Termux Compatible
"""

import os, sys, socket, json, time, re, subprocess, ssl, hashlib, threading, ipaddress
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Auto-install requests ──────────────────────────────────────────────────
try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests",
                    "--break-system-packages", "-q"], capture_output=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"],
                   capture_output=True)
    import requests
    requests.packages.urllib3.disable_warnings()

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════════════════════════
VERSION     = "1.0"
TIMEOUT     = 10
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 389,
    443, 445, 465, 587, 636, 993, 995, 1080, 1433, 1521,
    2222, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 8888,
    9200, 9300, 27017, 28017
]

# ══════════════════════════════════════════════════════════════════════════
#  COLORS  (lime / green / dark green / black palette)
# ══════════════════════════════════════════════════════════════════════════
class C:
    LM = '\033[92m'    # lime / bright green
    GR = '\033[32m'    # green
    DK = '\033[2;32m'  # dark green
    BD = '\033[1m'     # bold
    RS = '\033[0m'     # reset
    YW = '\033[93m'    # yellow (warnings)
    RE = '\033[91m'    # red (errors)
    WH = '\033[97m'    # white
    DM = '\033[2m'     # dim
    BK = '\033[90m'    # dark gray

def lm(s): return f"{C.LM}{s}{C.RS}"
def gr(s): return f"{C.GR}{s}{C.RS}"
def dk(s): return f"{C.DK}{s}{C.RS}"
def yw(s): return f"{C.YW}{s}{C.RS}"
def rd(s): return f"{C.RE}{s}{C.RS}"
def bd(s): return f"{C.BD}{s}{C.RS}"
def dm(s): return f"{C.DM}{s}{C.RS}"

# ══════════════════════════════════════════════════════════════════════════
#  LOGO & BANNER
# ══════════════════════════════════════════════════════════════════════════
LOGO = (
    f"{C.LM}⠀⣠⡶⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    f"{C.LM}⠀⣰⣿⠃⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀\n"
    f"{C.GR}⢸⣿⣯⠀⠀⠀⠀⠀⠀⢠⣴⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀\n"
    f"{C.GR}⢼⣿⣿⣆⠀⢀⣀⣀⣴⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀\n"
    f"{C.GR}⢸⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
    f"{C.DK}⠀⢻⣿⠋⠙⢿⣿⣿⡀⠀⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀\n"
    f"{C.DK}⠀⢸⠿⢆⣀⣼⣿⣿⣿⣿⡏⠀⢹⠀⠀⠀⠀⠀⠀⠀⠀\n"
    f"{C.DK}⠀⠀⡀⣨⡙⠟⣩⣙⣡⣬⣴⣤⠏⠀⠀⠀⠀⠀⠀⣀⡀\n"
    f"{C.LM}⠀⠀⠙⠿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⣀⣤⣾⣿⣿⡇\n"
    f"{C.LM}⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣇⠀⢸⣿⣿⠿⠿⠛⠃\n"
    f"{C.GR}⠀⠀⠀⠀⢠⣿⣿⢹⣿⢹⣿⣿⣿⢰⣿⠿⠃⠀⠀⠀⠀\n"
    f"{C.GR}⠀⢀⣀⣤⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡛⠀⠀⠀⠀⠀⠀\n"
    f"{C.DK}⠀⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠛⠓⠀⠀⠀⠀⠀\n"
    f"{C.DK}⠀⠀⠀⠀⠀⠀⠀⠉⠀⠉⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀{C.RS}"
)

def print_banner():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{LOGO}")
    print(f"  {C.BD}{C.LM}╔══════════════════════════════════════════════════╗{C.RS}")
    print(f"  {C.BD}{C.LM}║  {C.GR}TOOL DEFINITIVE{C.LM} ── OSINT MASSIVE SUITE v{VERSION}     ║{C.RS}")
    print(f"  {C.BD}{C.LM}║  {C.DK}50 Tools  │  Kali Linux & Termux Compatible {C.LM}    ║{C.RS}")
    print(f"  {C.BD}{C.LM}║  {C.DM}{now}{C.LM}                             ║{C.RS}")
    print(f"  {C.BD}{C.LM}╚══════════════════════════════════════════════════╝{C.RS}\n")

# ══════════════════════════════════════════════════════════════════════════
#  TARGET RESOLVER
# ══════════════════════════════════════════════════════════════════════════
def resolve_target(raw: str) -> dict:
    t = raw.strip()
    info = {
        'raw': t, 'host': '', 'ip': '',
        'domain': '', 'is_ip': False,
        'url': '', 'scheme': 'http'
    }
    if t.startswith(('http://', 'https://')):
        p = urlparse(t)
        info['url']    = t
        info['host']   = p.hostname or ''
        info['scheme'] = p.scheme
    else:
        info['host'] = t.split('/')[0]
        info['url']  = f"http://{info['host']}"
        info['scheme'] = 'http'
    try:
        ipaddress.ip_address(info['host'])
        info['is_ip'] = True
        info['ip']    = info['host']
        info['domain']= info['host']
    except:
        info['domain'] = info['host']
        try:
            info['ip'] = socket.gethostbyname(info['host'])
        except:
            info['ip'] = ''
    return info

# ══════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════
def run_cmd(cmd: list, timeout: int = 45) -> tuple:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired:
        return '', 'TIMEOUT', 1
    except FileNotFoundError:
        return '', f"NOT_FOUND:{cmd[0]}", 127
    except Exception as ex:
        return '', str(ex), 1

def cmd_exists(name: str) -> bool:
    from shutil import which
    return which(name) is not None

def http_get(url: str, **kw) -> requests.Response:
    kw.setdefault('timeout', TIMEOUT)
    kw.setdefault('verify', False)
    kw.setdefault('headers', {
        'User-Agent': 'Mozilla/5.0 (ToolDefinitive/1.0 OSINT)'
    })
    return requests.get(url, **kw)

# Result constructors
def ok(data: str)  -> dict: return {'status': 'ok',    'data': str(data)}
def err(data: str) -> dict: return {'status': 'error', 'data': str(data)}
def wr(data: str)  -> dict: return {'status': 'warn',  'data': str(data)}
def sk(data: str)  -> dict: return {'status': 'skip',  'data': str(data)}

# ══════════════════════════════════════════════════════════════════════════
#  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  50 TOOL FUNCTIONS  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
# ══════════════════════════════════════════════════════════════════════════

# ── [01] DNS A Records ────────────────────────────────────────────────────
def t01_dns_a(t):
    if t['is_ip']:
        return sk("Target is IP — skipping A record lookup")
    try:
        res = socket.getaddrinfo(t['domain'], None, socket.AF_INET)
        ips = sorted(set(r[4][0] for r in res))
        return ok("A Records: " + ", ".join(ips))
    except Exception as ex:
        # fallback: dig
        out, _, rc = run_cmd(['dig', '+short', 'A', t['domain']], 15)
        if rc == 0 and out.strip():
            return ok("A Records:\n" + out.strip())
        return err(str(ex))

# ── [02] DNS MX Records ───────────────────────────────────────────────────
def t02_dns_mx(t):
    if t['is_ip']:
        return sk("N/A for IP")
    out, _, rc = run_cmd(['dig', 'MX', t['domain'], '+short'], 15)
    if rc == 0 and out.strip():
        return ok("MX Records:\n" + out.strip())
    out2, _, rc2 = run_cmd(['nslookup', '-type=MX', t['domain']], 15)
    if rc2 == 0 and 'mail exchanger' in out2.lower():
        return ok("MX Records:\n" + out2.strip())
    return wr("No MX records found or dig/nslookup unavailable")

# ── [03] DNS NS Records ───────────────────────────────────────────────────
def t03_dns_ns(t):
    if t['is_ip']:
        return sk("N/A for IP")
    out, _, rc = run_cmd(['dig', 'NS', t['domain'], '+short'], 15)
    if rc == 0 and out.strip():
        return ok("NS Records:\n" + out.strip())
    out2, _, _ = run_cmd(['nslookup', '-type=NS', t['domain']], 15)
    return ok("NS Records:\n" + out2.strip()) if 'nameserver' in out2.lower() else wr("No NS records found")

# ── [04] DNS TXT Records ──────────────────────────────────────────────────
def t04_dns_txt(t):
    if t['is_ip']:
        return sk("N/A for IP")
    out, _, rc = run_cmd(['dig', 'TXT', t['domain'], '+short'], 15)
    if rc == 0 and out.strip():
        return ok("TXT Records (SPF/DKIM/DMARC):\n" + out.strip())
    return wr("No TXT records found")

# ── [05] DNS AAAA (IPv6) Records ──────────────────────────────────────────
def t05_dns_aaaa(t):
    if t['is_ip']:
        return sk("N/A for IP")
    out, _, rc = run_cmd(['dig', 'AAAA', t['domain'], '+short'], 15)
    if rc == 0 and out.strip():
        return ok("AAAA (IPv6) Records:\n" + out.strip())
    try:
        res = socket.getaddrinfo(t['domain'], None, socket.AF_INET6)
        ips = sorted(set(r[4][0] for r in res))
        return ok("IPv6: " + ", ".join(ips))
    except:
        return wr("No IPv6 records found")

# ── [06] DNS CNAME Records ────────────────────────────────────────────────
def t06_dns_cname(t):
    if t['is_ip']:
        return sk("N/A for IP")
    out, _, rc = run_cmd(['dig', 'CNAME', t['domain'], '+short'], 15)
    if rc == 0 and out.strip():
        return ok("CNAME: " + out.strip())
    return wr("No CNAME record found")

# ── [07] Reverse DNS (PTR) ────────────────────────────────────────────────
def t07_reverse_dns(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved for reverse DNS")
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return ok(f"Reverse DNS: {ip}  →  {host}")
    except socket.herror:
        return wr(f"No PTR record for {ip}")
    except Exception as ex:
        return err(str(ex))

# ── [08] Zone Transfer Attempt ────────────────────────────────────────────
def t08_zone_transfer(t):
    if t['is_ip']:
        return sk("N/A for IP")
    domain = t['domain']
    out_ns, _, _ = run_cmd(['dig', 'NS', domain, '+short'], 15)
    ns_list = [x.rstrip('.') for x in out_ns.strip().split('\n') if x.strip()]
    if not ns_list:
        return wr("Could not retrieve NS records — zone transfer skipped")
    results = []
    for ns in ns_list[:4]:
        out, _, rc = run_cmd(['dig', 'AXFR', f'@{ns}', domain], 20)
        if rc == 0 and len(out) > 300 and 'Transfer failed' not in out:
            results.append(f"{ns}: !! ZONE TRANSFER POSSIBLE !!\n{out[:500]}")
        else:
            results.append(f"{ns}: Transfer denied ✓")
    return ok('\n'.join(results))

# ── [09] WHOIS / RDAP ─────────────────────────────────────────────────────
def t09_whois_rdap(t):
    target = t['ip'] if t['is_ip'] else t['domain']
    # Try system whois
    if cmd_exists('whois'):
        out, _, rc = run_cmd(['whois', target], 30)
        if rc == 0 and len(out.strip()) > 50:
            keep_keys = ['registrar','created','expir','updated','name server',
                         'organization','country','netname','cidr','abuse',
                         'email','org-name','owner','admin','tech','registrant',
                         'status','dnssec']
            lines = [l for l in out.split('\n')
                     if any(k in l.lower() for k in keep_keys) and ':' in l]
            return ok('\n'.join(lines[:40]) if lines else out[:1500])
    # Fallback: RDAP API
    try:
        if t['is_ip']:
            r = http_get(f"https://rdap.arin.net/registry/ip/{target}")
        else:
            r = http_get(f"https://rdap.verisign.com/com/v1/domain/{target}")
        if r.status_code == 200:
            d = r.json()
            info = [
                f"Handle:  {d.get('handle','N/A')}",
                f"Name:    {d.get('name','N/A')}",
                f"Type:    {d.get('type','N/A')}",
            ]
            for ev in d.get('events', [])[:5]:
                info.append(f"{ev.get('eventAction','')}: {ev.get('eventDate','')[:10]}")
            return ok('\n'.join(info))
    except Exception as ex:
        return err(f"RDAP failed: {ex}")
    return err("whois/RDAP unavailable")

# ── [10] IP Geolocation (ip-api.com) ─────────────────────────────────────
def t10_ip_geoloc(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        fields = "status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        r = http_get(f"http://ip-api.com/json/{ip}?fields={fields}")
        if r.status_code == 200:
            d = r.json()
            if d.get('status') == 'success':
                return ok(
                    f"IP:        {d.get('query')}\n"
                    f"Country:   {d.get('country')} ({d.get('countryCode','')})\n"
                    f"Region:    {d.get('regionName')}\n"
                    f"City:      {d.get('city')} {d.get('zip','')}\n"
                    f"Coords:    {d.get('lat')}, {d.get('lon')}\n"
                    f"Timezone:  {d.get('timezone')}\n"
                    f"ISP:       {d.get('isp')}\n"
                    f"Org:       {d.get('org')}\n"
                    f"ASN:       {d.get('as')}"
                )
            return wr(d.get('message', 'Rate limited or private IP'))
    except Exception as ex:
        return err(str(ex))
    return err("ip-api.com request failed")

# ── [11] IPInfo.io ────────────────────────────────────────────────────────
def t11_ipinfo(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        r = http_get(f"https://ipinfo.io/{ip}/json")
        if r.status_code == 200:
            d = r.json()
            if d.get('bogon'):
                return wr(f"Bogon/private IP: {ip}")
            return ok(
                f"IP:       {d.get('ip')}\n"
                f"Hostname: {d.get('hostname','N/A')}\n"
                f"City:     {d.get('city','N/A')}\n"
                f"Region:   {d.get('region','N/A')}\n"
                f"Country:  {d.get('country','N/A')}\n"
                f"Org:      {d.get('org','N/A')}\n"
                f"Postal:   {d.get('postal','N/A')}\n"
                f"Timezone: {d.get('timezone','N/A')}"
            )
    except Exception as ex:
        return err(str(ex))
    return err("ipinfo.io request failed")

# ── [12] Shodan InternetDB (free, no key) ────────────────────────────────
def t12_shodan_idb(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        r = http_get(f"https://internetdb.shodan.io/{ip}")
        if r.status_code == 200:
            d = r.json()
            if 'detail' in d:
                return wr(str(d['detail']))
            ports = ', '.join(str(p) for p in d.get('ports', []))
            hosts = ', '.join(d.get('hostnames', [])[:5])
            cpes  = ', '.join(d.get('cpes',  [])[:5])
            vulns = ', '.join(d.get('vulns', [])[:10])
            tags  = ', '.join(d.get('tags',  []))
            return ok(
                f"IP:        {d.get('ip')}\n"
                f"Open Ports:{ports or 'none'}\n"
                f"Hostnames: {hosts or 'none'}\n"
                f"CPEs:      {cpes  or 'none'}\n"
                f"Tags:      {tags  or 'none'}\n"
                f"Vulns:     {vulns or 'none'}"
            )
        return wr(f"HTTP {r.status_code}")
    except Exception as ex:
        return err(str(ex))

# ── [13] BGP / ASN Info (BGPView) ────────────────────────────────────────
def t13_bgp_asn(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        r = http_get(f"https://api.bgpview.io/ip/{ip}")
        if r.status_code == 200:
            data = r.json().get('data', {})
            pfxs = data.get('prefixes', [])
            lines = [f"IP: {ip}"]
            for pfx in pfxs[:3]:
                for asn in pfx.get('asns', [])[:2]:
                    lines += [
                        f"ASN:      {asn.get('asn')} — {asn.get('name','')}",
                        f"Country:  {asn.get('country_code','')}",
                        f"Prefix:   {pfx.get('prefix','')}",
                        f"RIR:      {pfx.get('rir_allocation',{}).get('rir_name','')}",
                        f"Desc:     {pfx.get('description','')}",
                        "---"
                    ]
            return ok('\n'.join(lines)) if len(lines) > 1 else wr("No BGP/ASN data found")
    except Exception as ex:
        return err(str(ex))
    return err("BGPView request failed")

# ── [14] GreyNoise Community ──────────────────────────────────────────────
def t14_greynoise(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        r = http_get(f"https://api.greynoise.io/v3/community/{ip}")
        if r.status_code == 200:
            d = r.json()
            return ok(
                f"IP:      {d.get('ip')}\n"
                f"Noise:   {d.get('noise')}\n"
                f"Riot:    {d.get('riot')}\n"
                f"Name:    {d.get('name','N/A')}\n"
                f"Message: {d.get('message','')}\n"
                f"Link:    {d.get('link','')}"
            )
        if r.status_code == 404:
            return wr("IP not in GreyNoise dataset (not seen scanning the internet)")
        return wr(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as ex:
        return err(str(ex))

# ── [15] AbuseIPDB (public lookup) ───────────────────────────────────────
def t15_abuseipdb(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        r = http_get(f"https://www.abuseipdb.com/check/{ip}",
                     headers={'User-Agent': 'Mozilla/5.0 (OSINT/1.0)'})
        if r.status_code == 200:
            txt = r.text
            score_m   = re.search(r'(\d+)\s*%', txt)
            report_m  = re.search(r'(\d[\d,]*)\s+report', txt, re.I)
            country_m = re.search(r'country["\s:]+([A-Z]{2})', txt, re.I)
            score    = score_m.group(1)   + '%' if score_m   else 'N/A'
            reports  = report_m.group(1)        if report_m  else 'N/A'
            country  = country_m.group(1)       if country_m else 'N/A'
            return ok(
                f"AbuseIPDB  →  {ip}\n"
                f"Abuse Score: {score}\n"
                f"Reports:     {reports}\n"
                f"Country:     {country}\n"
                f"Details:     https://www.abuseipdb.com/check/{ip}"
            )
        return wr(f"HTTP {r.status_code}")
    except Exception as ex:
        return err(str(ex))

# ── [16] ThreatCrowd ─────────────────────────────────────────────────────
def t16_threatcrowd(t):
    try:
        if t['is_ip']:
            url = f"https://www.threatcrowd.org/searchApi/v2/ip/report/?ip={t['ip']}"
        else:
            url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={t['domain']}"
        r = http_get(url)
        if r.status_code == 200:
            d = r.json()
            lines = [f"Response Code: {d.get('response_code','N/A')}"]
            if d.get('resolutions'):
                lines.append(f"Resolutions ({len(d['resolutions'])}):")
                for res in d['resolutions'][:8]:
                    lines.append(f"  → {res.get('ip_address', res.get('domain',''))} "
                                 f"({res.get('last_resolved','')[:10]})")
            if d.get('hashes'):
                lines.append(f"Related malware hashes: {len(d['hashes'])}")
            if d.get('emails'):
                lines.append(f"Emails: {', '.join(d['emails'][:5])}")
            if d.get('votes') is not None:
                lines.append(f"Malicious votes: {d['votes']}")
            return ok('\n'.join(lines))
        return wr(f"HTTP {r.status_code}")
    except Exception as ex:
        return err(str(ex))

# ── [17] crt.sh Certificate Transparency ─────────────────────────────────
def t17_crtsh(t):
    if t['is_ip']:
        return sk("N/A for IP addresses")
    domain = t['domain']
    try:
        r = http_get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=20)
        if r.status_code == 200:
            data = r.json()
            subs = set()
            for entry in data:
                for name in entry.get('name_value', '').split('\n'):
                    name = name.strip().lstrip('*.')
                    if name and domain in name:
                        subs.add(name)
            if subs:
                sorted_subs = sorted(subs)
                return ok(f"crt.sh found {len(sorted_subs)} subdomains:\n" +
                          '\n'.join(sorted_subs[:60]))
            return wr("No certificates found in crt.sh")
    except Exception as ex:
        return err(str(ex))
    return err("crt.sh request failed")

# ── [18] HackerTarget DNS / DNSDumpster ──────────────────────────────────
def t18_dnsdumpster(t):
    if t['is_ip']:
        return sk("N/A for IP")
    domain = t['domain']
    try:
        r = http_get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=20)
        if r.status_code == 200:
            txt = r.text.strip()
            if 'error' in txt.lower() or 'API' in txt:
                return wr(f"HackerTarget: {txt[:200]}")
            lines = txt.split('\n')
            hosts = []
            for line in lines:
                if ',' in line:
                    host, ip_addr = line.split(',', 1)
                    hosts.append(f"  {host.strip():<45} {ip_addr.strip()}")
            return ok(f"HackerTarget — {len(hosts)} DNS records:\n" + '\n'.join(hosts[:40]))
    except Exception as ex:
        return err(str(ex))
    return err("HackerTarget request failed")

# ── [19] HTTP Headers Analysis ───────────────────────────────────────────
def t19_http_headers(t):
    for url in [t['url'], f"https://{t['host']}"]:
        try:
            r = http_get(url, allow_redirects=True)
            lines = [
                f"Status:    {r.status_code} {r.reason}",
                f"Final URL: {r.url}",
                "─" * 45
            ]
            for k, v in r.headers.items():
                lines.append(f"{k}: {v}")
            return ok('\n'.join(lines))
        except requests.exceptions.SSLError:
            continue
        except Exception as ex:
            last_err = str(ex)
    return err(last_err)

# ── [20] SSL Certificate Info ─────────────────────────────────────────────
def t20_ssl_cert(t):
    host = t['host']
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE
        with socket.create_connection((host, 443), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert   = ssock.getpeercert()
                cipher = ssock.cipher()
        subject = dict(x[0] for x in cert.get('subject', []))
        issuer  = dict(x[0] for x in cert.get('issuer',  []))
        sans    = cert.get('subjectAltName', [])
        lines   = [
            f"Subject CN:  {subject.get('commonName','N/A')}",
            f"Subject Org: {subject.get('organizationName','N/A')}",
            f"Issuer:      {issuer.get('organizationName','N/A')} ({issuer.get('countryName','')})",
            f"Valid From:  {cert.get('notBefore','N/A')}",
            f"Valid To:    {cert.get('notAfter','N/A')}",
            f"Cipher:      {cipher[0]} ({cipher[1]} bit)" if cipher else "",
            f"SANs ({len(sans)}): {', '.join(v for _,v in sans[:10])}",
        ]
        return ok('\n'.join(l for l in lines if l))
    except ssl.SSLError as ex:
        return wr(f"SSL error: {ex}")
    except ConnectionRefusedError:
        return wr("Port 443 closed — no SSL service detected")
    except Exception as ex:
        return err(str(ex))

# ── [21] Security Headers Audit ──────────────────────────────────────────
def t21_security_headers(t):
    try:
        r = http_get(t['url'])
        h = {k.lower(): v for k, v in r.headers.items()}
        checks = {
            'strict-transport-security': 'HSTS',
            'content-security-policy':   'CSP',
            'x-frame-options':           'X-Frame-Options',
            'x-xss-protection':          'X-XSS-Protection',
            'x-content-type-options':    'X-Content-Type-Options',
            'referrer-policy':           'Referrer-Policy',
            'permissions-policy':        'Permissions-Policy',
        }
        present, missing = [], []
        for header, name in checks.items():
            if header in h:
                present.append(f"  [PRESENT] {name}: {h[header][:80]}")
            else:
                missing.append(f"  [MISSING] {name}")
        score = len(present)
        grade = 'A' if score>=6 else 'B' if score>=4 else 'C' if score>=2 else 'F'
        lines = [f"Security Headers Audit — Grade: {grade} ({score}/7 headers present)"]
        lines += present + missing
        return ok('\n'.join(lines))
    except Exception as ex:
        return err(str(ex))

# ── [22] CORS Misconfiguration ───────────────────────────────────────────
def t22_cors_check(t):
    try:
        r = http_get(t['url'], headers={
            'Origin': 'https://evil-site.com',
            'User-Agent': 'Mozilla/5.0'
        })
        acao = r.headers.get('Access-Control-Allow-Origin', '')
        acac = r.headers.get('Access-Control-Allow-Credentials', '')
        acam = r.headers.get('Access-Control-Allow-Methods', '')
        lines = [
            f"Allow-Origin:      {acao or 'Not set'}",
            f"Allow-Credentials: {acac or 'Not set'}",
            f"Allow-Methods:     {acam or 'Not set'}",
            "─" * 40
        ]
        if acao == '*':
            lines.append("⚠ WARNING: Wildcard (*) CORS — any origin allowed")
        elif 'evil-site.com' in acao:
            lines.append("⚠ CRITICAL: Reflects arbitrary Origin (CORS hijack possible!)")
        elif acao and acac.lower() == 'true':
            lines.append("⚠ WARNING: Credentialed CORS with reflected origin")
        else:
            lines.append("✓ CORS appears properly configured")
        return ok('\n'.join(lines))
    except Exception as ex:
        return err(str(ex))

# ── [23] robots.txt ───────────────────────────────────────────────────────
def t23_robots_txt(t):
    url = t['url'].rstrip('/') + '/robots.txt'
    try:
        r = http_get(url)
        if r.status_code == 200 and len(r.text.strip()) > 5:
            lines = r.text.strip().split('\n')
            disallowed = [l for l in lines if l.lower().startswith('disallow')]
            return ok(f"robots.txt found ({len(lines)} lines, {len(disallowed)} Disallow entries):\n{r.text[:2000]}")
        return wr(f"HTTP {r.status_code} — robots.txt not found or empty")
    except Exception as ex:
        return err(str(ex))

# ── [24] sitemap.xml ─────────────────────────────────────────────────────
def t24_sitemap(t):
    base = t['url'].rstrip('/')
    for path in ['/sitemap.xml', '/sitemap_index.xml', '/sitemap.txt', '/sitemap']:
        try:
            r = http_get(base + path, timeout=8)
            if r.status_code == 200 and len(r.text.strip()) > 20:
                url_count = r.text.count('<url>')
                loc_count = r.text.count('<loc>')
                return ok(
                    f"Sitemap found: {base + path}\n"
                    f"<url> entries:  {url_count}\n"
                    f"<loc> entries:  {loc_count}\n"
                    f"Preview:\n{r.text[:600]}"
                )
        except:
            pass
    return wr("No sitemap.xml found at common paths")

# ── [25] Wayback Machine ──────────────────────────────────────────────────
def t25_wayback(t):
    domain = t['domain']
    try:
        r = http_get(f"https://archive.org/wayback/available?url={domain}", timeout=15)
        if r.status_code == 200:
            snap = r.json().get('archived_snapshots', {}).get('closest', {})
            if snap:
                return ok(
                    f"Wayback Machine snapshot found!\n"
                    f"URL:       {snap.get('url')}\n"
                    f"Timestamp: {snap.get('timestamp')}\n"
                    f"Status:    {snap.get('status')}\n"
                    f"More:      https://web.archive.org/web/*/{domain}"
                )
            return wr(f"No Wayback Machine snapshots for {domain}")
    except Exception as ex:
        return err(str(ex))
    return err("Wayback request failed")

# ── [26] VirusTotal (public lookup) ──────────────────────────────────────
def t26_virustotal(t):
    target = t['domain'] if not t['is_ip'] else t['ip']
    try:
        r = http_get(
            f"https://www.virustotal.com/ui/search?query={target}&limit=5",
            headers={
                'x-tool': 'vt-ui-main',
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            }
        )
        if r.status_code == 200:
            items = r.json().get('data', [])
            if items:
                attrs = items[0].get('attributes', {})
                stats = attrs.get('last_analysis_stats', {})
                rep   = attrs.get('reputation', 'N/A')
                cats  = attrs.get('categories', {})
                return ok(
                    f"VirusTotal → {target}\n"
                    f"Malicious:  {stats.get('malicious',0)}\n"
                    f"Suspicious: {stats.get('suspicious',0)}\n"
                    f"Harmless:   {stats.get('harmless',0)}\n"
                    f"Undetected: {stats.get('undetected',0)}\n"
                    f"Reputation: {rep}\n"
                    f"Categories: {', '.join(list(cats.values())[:3])}"
                )
        return wr(f"VT HTTP {r.status_code} — visit: https://www.virustotal.com/gui/search/{target}")
    except Exception as ex:
        return err(str(ex))

# ── [27] URLScan.io ───────────────────────────────────────────────────────
def t27_urlscan(t):
    domain = t['domain']
    try:
        r = http_get(f"https://urlscan.io/api/v1/search/?q=domain:{domain}&size=5", timeout=15)
        if r.status_code == 200:
            d = r.json()
            total   = d.get('total', 0)
            results = d.get('results', [])
            lines   = [f"URLScan.io — {total} scans found for: {domain}"]
            for res in results[:5]:
                page = res.get('page', {})
                ts   = res.get('task', {}).get('time', '')[:10]
                lines.append(f"  [{ts}] {page.get('url','')[:70]}  [{page.get('status','')}]")
            if total:
                lines.append(f"  Full results: https://urlscan.io/search/#domain:{domain}")
            return ok('\n'.join(lines))
        return wr(f"HTTP {r.status_code}")
    except Exception as ex:
        return err(str(ex))

# ── [28] Ping ─────────────────────────────────────────────────────────────
def t28_ping(t):
    host = t['host']
    flag = '-n' if os.name == 'nt' else '-c'
    out, _, rc = run_cmd(['ping', flag, '4', '-W', '2', host], 20)
    if rc == 0:
        m = re.search(r'(?:avg|rtt)[^=]+=\s*[\d.]+/([\d.]+)', out)
        avg = (m.group(1) + ' ms') if m else 'see output'
        return ok(f"Host is REACHABLE | Avg RTT: {avg}\n{out.strip()}")
    return wr(f"Host appears DOWN or ICMP filtered\n{out.strip()}")

# ── [29] Traceroute ───────────────────────────────────────────────────────
def t29_traceroute(t):
    host = t['host']
    if cmd_exists('traceroute'):
        out, _, rc = run_cmd(['traceroute', '-m', '20', '-w', '2', host], 90)
    elif cmd_exists('tracert'):
        out, _, rc = run_cmd(['tracert', '-h', '20', host], 90)
    else:
        return sk("traceroute/tracert not installed  (pkg install traceroute)")
    if out.strip():
        return ok(f"Traceroute → {host}:\n{out[:2500]}")
    return wr("Traceroute produced no output")

# ── [30] Banner Grabbing ─────────────────────────────────────────────────
def t30_banner_grab(t):
    ip     = t['ip'] or t['host']
    probes = {
        21:  b'',
        22:  b'',
        25:  b'',
        80:  b'HEAD / HTTP/1.0\r\nHost: ' + t['host'].encode() + b'\r\n\r\n',
        110: b'',
        143: b'',
        443: None,  # skip, SSL handled
        8080: b'HEAD / HTTP/1.0\r\n\r\n',
    }
    results = []
    for port, probe in probes.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            if s.connect_ex((ip, port)) == 0:
                if probe is not None:
                    if probe:
                        s.send(probe)
                    banner = s.recv(512).decode(errors='ignore').strip()
                    banner = ' '.join(banner.split())[:120]
                    results.append(f"  Port {port:5d}: {banner or '[connected, empty banner]'}")
                else:
                    results.append(f"  Port {port:5d}: [open]")
            s.close()
        except:
            pass
    return ok("Banners:\n" + '\n'.join(results)) if results else wr("No banners grabbed (no open ports)")

# ── [31] Common Port Scanner (Python) ────────────────────────────────────
def t31_port_scan(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    open_ports = []
    lock = threading.Lock()

    def probe(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.5)
            if s.connect_ex((ip, port)) == 0:
                with lock:
                    open_ports.append(port)
            s.close()
        except:
            pass

    threads = [threading.Thread(target=probe, args=(p,), daemon=True) for p in COMMON_PORTS]
    for th in threads: th.start()
    for th in threads: th.join(timeout=6)

    if open_ports:
        return ok(f"Open ports on {ip} [{len(open_ports)}/{len(COMMON_PORTS)} checked]:\n"
                  + ', '.join(str(p) for p in sorted(open_ports)))
    return wr(f"No common ports open on {ip}")

# ── [32] HTML Meta Tags & Title ──────────────────────────────────────────
def t32_meta_tags(t):
    try:
        r    = http_get(t['url'])
        body = r.text
        title_m = re.search(r'<title[^>]*>(.*?)</title>', body, re.I|re.S)
        title   = title_m.group(1).strip()[:100] if title_m else 'N/A'
        metas   = re.findall(r'<meta[^>]+>', body, re.I)
        lines   = [f"Title: {title}", "─"*40, "Meta Tags:"]
        for meta in metas[:20]:
            name = re.search(r'(?:name|property)=["\']([^"\']+)["\']', meta, re.I)
            cont = re.search(r'content=["\']([^"\']{0,120})["\']', meta, re.I)
            if name and cont:
                lines.append(f"  {name.group(1):<30} {cont.group(1)}")
        generator_m = re.search(r'<meta[^>]+generator[^>]+content=["\']([^"\']+)', body, re.I)
        if generator_m:
            lines.append(f"\n  Generator: {generator_m.group(1)}")
        return ok('\n'.join(lines))
    except Exception as ex:
        return err(str(ex))

# ── [33] Favicon Hash (Shodan Dork) ──────────────────────────────────────
def t33_favicon_hash(t):
    base = t['url'].rstrip('/')
    for fav_url in [base + '/favicon.ico', base + '/favicon.png']:
        try:
            r = http_get(fav_url, timeout=8)
            if r.status_code == 200 and r.content:
                import base64
                md5_hash = hashlib.md5(r.content).hexdigest()
                # Calculate MurmurHash3 if mmh3 available
                try:
                    import mmh3
                    b64 = base64.encodebytes(r.content)
                    fhash = mmh3.hash(b64)
                    return ok(
                        f"Favicon: {fav_url}\n"
                        f"Size:    {len(r.content)} bytes\n"
                        f"MD5:     {md5_hash}\n"
                        f"Shodan hash (mmh3): {fhash}\n"
                        f"Shodan dork: http.favicon.hash:{fhash}"
                    )
                except ImportError:
                    return ok(
                        f"Favicon: {fav_url}\n"
                        f"Size:    {len(r.content)} bytes\n"
                        f"MD5:     {md5_hash}\n"
                        f"Note: install mmh3 for Shodan hash  (pip install mmh3)"
                    )
        except:
            pass
    return wr("No favicon found at common paths")

# ── [34] HackerTarget Subdomains ─────────────────────────────────────────
def t34_hackertarget_subs(t):
    if t['is_ip']:
        return sk("N/A for IP")
    domain = t['domain']
    try:
        r = http_get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=20)
        if r.status_code == 200:
            txt = r.text.strip()
            if 'error' in txt.lower() or 'API count' in txt:
                return wr(txt[:200])
            lines = txt.split('\n')
            subs  = [l.split(',')[0] for l in lines if ',' in l]
            return ok(f"HackerTarget subdomains ({len(subs)}):\n" + '\n'.join(subs[:50]))
    except Exception as ex:
        return err(str(ex))
    return err("HackerTarget request failed")

# ── [35] Reverse IP Lookup ───────────────────────────────────────────────
def t35_reverse_ip(t):
    ip = t['ip']
    if not ip:
        return err("No IP resolved")
    try:
        r = http_get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=20)
        if r.status_code == 200:
            txt = r.text.strip()
            if 'error' in txt.lower():
                return wr(txt[:200])
            hosts = [h for h in txt.split('\n') if h.strip()]
            return ok(f"Reverse IP — {len(hosts)} domain(s) on {ip}:\n" + '\n'.join(hosts[:40]))
    except Exception as ex:
        return err(str(ex))
    return err("Reverse IP lookup failed")

# ── [36] Technology Fingerprinting ───────────────────────────────────────
def t36_tech_detect(t):
    try:
        r    = http_get(t['url'])
        body = r.text.lower()[:8000]
        h    = {k.lower(): v.lower() for k, v in r.headers.items()}
        tech = []
        if 'server' in h:        tech.append(f"Server:       {h['server']}")
        if 'x-powered-by' in h:  tech.append(f"X-Powered-By: {h['x-powered-by']}")
        if 'x-generator' in h:   tech.append(f"X-Generator:  {h['x-generator']}")

        patterns = {
            'WordPress':   ['wp-content','wp-includes','wordpress'],
            'Joomla':      ['joomla','/components/com_'],
            'Drupal':      ['drupal','sites/default/files'],
            'Laravel':     ['laravel_session','x-powered-by: php'],
            'Django':      ['csrfmiddlewaretoken','django'],
            'Ruby/Rails':  ['x-powered-by: phusion','x-runtime'],
            'React':       ['__react','react-dom','_reactroot'],
            'Vue.js':      ['__vue__','vue.js'],
            'Angular':     ['ng-version','angular.js'],
            'jQuery':      ['jquery'],
            'Bootstrap':   ['bootstrap.css','bootstrap.min'],
            'Cloudflare':  ['cf-ray','__cfduid','cloudflare'],
            'AWS S3':      ['x-amz-','amazonaws'],
            'nginx':       ['nginx'],
            'Apache':      ['apache'],
            'IIS':         ['x-aspnet-version','x-powered-by: asp'],
            'PHP':         ['x-powered-by: php'],
            'Node.js':     ['x-powered-by: express'],
        }
        for name, kws in patterns.items():
            if any(kw in body or kw in str(h) for kw in kws):
                tech.append(f"Detected:     {name}")
        return ok('\n'.join(tech) if tech else "No specific technologies fingerprinted")
    except Exception as ex:
        return err(str(ex))

# ══════════════════════════════════════════════════════════════════════════
#  ░░░░░░░░░░░░  KALI / ADVANCED TOOLS (37–50)  ░░░░░░░░░░░░
# ══════════════════════════════════════════════════════════════════════════

# ── [37] Nmap Quick Scan ─────────────────────────────────────────────────
def t37_nmap_quick(t):
    if not cmd_exists('nmap'):
        return sk("nmap not installed  (pkg install nmap  /  apt install nmap)")
    out, _, rc = run_cmd(
        ['nmap', '-T4', '--top-ports', '1000', '--open', '-oN', '-', t['host']], 180)
    return ok(out[:3500]) if rc == 0 and out.strip() else err(out or "nmap returned no output")

# ── [38] Nmap Service/Version Detection ──────────────────────────────────
def t38_nmap_service(t):
    if not cmd_exists('nmap'):
        return sk("nmap not installed")
    out, _, rc = run_cmd(
        ['nmap', '-sV', '-T4', '--top-ports', '200', t['host']], 240)
    return ok(out[:3500]) if rc == 0 else err(out)

# ── [39] Nmap OS Detection (Kali/root) ───────────────────────────────────
def t39_nmap_os(t):
    if not cmd_exists('nmap'):
        return sk("nmap not installed  [Kali: apt install nmap]")
    out, _, rc = run_cmd(
        ['nmap', '-O', '-T4', '--top-ports', '100', t['host']], 180)
    if 'requires root' in (out+_).lower():
        return wr("OS detection requires root. Run: sudo python3 tool_definitive.py")
    return ok(out[:2500]) if rc == 0 else err(out)

# ── [40] Nmap Vuln Scripts ────────────────────────────────────────────────
def t40_nmap_vuln(t):
    if not cmd_exists('nmap'):
        return sk("nmap not installed  [Kali]")
    out, _, rc = run_cmd(
        ['nmap', '--script', 'vuln', '-T3', '--top-ports', '100', t['host']], 420)
    return ok(out[:5000]) if rc == 0 else err(out or _)

# ── [41] Masscan Full Port Range ──────────────────────────────────────────
def t41_masscan(t):
    if not cmd_exists('masscan'):
        return sk("masscan not installed  [Kali: apt install masscan]")
    ip = t['ip']
    if not ip:
        return err("No IP resolved for masscan")
    out, _, rc = run_cmd(
        ['masscan', '-p', '1-65535', '--rate', '500', ip], 600)
    return ok(out[:3000]) if rc == 0 else err(out or _)

# ── [42] Nikto Web Scanner ────────────────────────────────────────────────
def t42_nikto(t):
    if not cmd_exists('nikto'):
        return sk("nikto not installed  [Kali: apt install nikto]")
    out, _, rc = run_cmd(
        ['nikto', '-h', t['url'], '-maxtime', '90s', '-nointeractive',
         '-Format', 'txt'], 180)
    return ok(out[:5000]) if rc == 0 else err(out or _)

# ── [43] WhatWeb Fingerprinting ──────────────────────────────────────────
def t43_whatweb(t):
    if not cmd_exists('whatweb'):
        return sk("whatweb not installed  [Kali: apt install whatweb]")
    out, _, rc = run_cmd(
        ['whatweb', '-a', '3', '--color', 'never', t['url']], 90)
    return ok(out[:3000]) if rc == 0 else err(out or _)

# ── [44] WafW00f WAF Detection ────────────────────────────────────────────
def t44_wafw00f(t):
    if not cmd_exists('wafw00f'):
        return sk("wafw00f not installed  [pip install wafw00f  or  apt install wafw00f]")
    out, _, rc = run_cmd(['wafw00f', t['url']], 60)
    return ok(out[:2000]) if rc == 0 else err(out or _)

# ── [45] Subfinder Subdomain Enum ────────────────────────────────────────
def t45_subfinder(t):
    if t['is_ip']:
        return sk("N/A for IP")
    if not cmd_exists('subfinder'):
        return sk("subfinder not installed  [go install / apt]")
    out, _, rc = run_cmd(
        ['subfinder', '-d', t['domain'], '-silent', '-timeout', '30'], 120)
    if out.strip():
        subs = out.strip().split('\n')
        return ok(f"Subfinder — {len(subs)} subdomains:\n{out[:3000]}")
    return wr("No subdomains found by subfinder")

# ── [46] Amass Passive Enum ───────────────────────────────────────────────
def t46_amass(t):
    if t['is_ip']:
        return sk("N/A for IP")
    if not cmd_exists('amass'):
        return sk("amass not installed  [Kali: apt install amass]")
    out, _, rc = run_cmd(
        ['amass', 'enum', '-passive', '-d', t['domain'], '-timeout', '4'], 300)
    if out.strip():
        subs = [l for l in out.strip().split('\n') if t['domain'] in l]
        return ok(f"Amass — {len(subs)} subdomains:\n" + '\n'.join(subs[:60]))
    return wr("Amass returned no results")

# ── [47] theHarvester ─────────────────────────────────────────────────────
def t47_theharvester(t):
    if t['is_ip']:
        return sk("N/A for IP")
    cmd_name = next(
        (c for c in ['theHarvester','theharvester'] if cmd_exists(c)), None)
    if not cmd_name:
        return sk("theHarvester not installed  [Kali: apt install theharvester]")
    out, _, rc = run_cmd(
        [cmd_name, '-d', t['domain'], '-b', 'all', '-l', '100'], 180)
    return ok(out[:4000]) if rc == 0 else err(out or _)

# ── [48] dnsrecon ─────────────────────────────────────────────────────────
def t48_dnsrecon(t):
    if t['is_ip']:
        return sk("N/A for IP")
    if not cmd_exists('dnsrecon'):
        return sk("dnsrecon not installed  [Kali: apt install dnsrecon]")
    out, _, rc = run_cmd(
        ['dnsrecon', '-d', t['domain'], '-t', 'std'], 180)
    return ok(out[:3500]) if rc == 0 else err(out or _)

# ── [49] dnsenum ─────────────────────────────────────────────────────────
def t49_dnsenum(t):
    if t['is_ip']:
        return sk("N/A for IP")
    if not cmd_exists('dnsenum'):
        return sk("dnsenum not installed  [Kali: apt install dnsenum]")
    out, _, rc = run_cmd(
        ['dnsenum', '--nocolor', '--noreverse', '--threads', '5', t['domain']], 240)
    return ok(out[:3500]) if rc == 0 else err(out or _)

# ── [50] Gobuster Directory Bruteforce ───────────────────────────────────
def t50_gobuster(t):
    if not cmd_exists('gobuster'):
        return sk("gobuster not installed  [Kali: apt install gobuster]")
    wordlists = [
        '/usr/share/wordlists/dirb/small.txt',
        '/usr/share/wordlists/dirb/common.txt',
        '/usr/share/wordlists/dirbuster/directory-list-2.3-small.txt',
    ]
    wl = next((w for w in wordlists if os.path.exists(w)), None)
    if not wl:
        return sk("No wordlist found for gobuster. Install wordlists: apt install wordlists")
    out, _, rc = run_cmd(
        ['gobuster', 'dir', '-u', t['url'], '-w', wl, '-q',
         '-t', '20', '--timeout', '5s', '-x', 'php,html,txt,asp,aspx'], 180)
    return ok(out[:4000]) if rc == 0 else err(out or _)

# ══════════════════════════════════════════════════════════════════════════
#  TOOL REGISTRY  —  (id, name, category, platform, func, description)
# ══════════════════════════════════════════════════════════════════════════
TOOLS = [
    # ── DNS ─────────────────────────────────────────────────────────────
    ( 1, "DNS A Records",           "DNS",        "both",  t01_dns_a,           "Resolve IPv4 A records"),
    ( 2, "DNS MX Records",          "DNS",        "both",  t02_dns_mx,          "Mail exchanger records"),
    ( 3, "DNS NS Records",          "DNS",        "both",  t03_dns_ns,          "Name server records"),
    ( 4, "DNS TXT Records",         "DNS",        "both",  t04_dns_txt,         "TXT (SPF/DKIM/DMARC)"),
    ( 5, "DNS AAAA (IPv6)",         "DNS",        "both",  t05_dns_aaaa,        "IPv6 AAAA records"),
    ( 6, "DNS CNAME",               "DNS",        "both",  t06_dns_cname,       "Canonical name records"),
    ( 7, "Reverse DNS (PTR)",       "DNS",        "both",  t07_reverse_dns,     "Reverse DNS / PTR lookup"),
    ( 8, "Zone Transfer (AXFR)",    "DNS",        "both",  t08_zone_transfer,   "Attempt DNS zone transfer"),
    # ── WHOIS ───────────────────────────────────────────────────────────
    ( 9, "WHOIS / RDAP",            "WHOIS",      "both",  t09_whois_rdap,      "Registration & ownership info"),
    # ── IP Intelligence ─────────────────────────────────────────────────
    (10, "IP Geolocation",          "IP Intel",   "both",  t10_ip_geoloc,       "ip-api.com geolocation"),
    (11, "IPInfo.io",               "IP Intel",   "both",  t11_ipinfo,          "ipinfo.io full lookup"),
    (12, "Shodan InternetDB",       "IP Intel",   "both",  t12_shodan_idb,      "Shodan free (no API key)"),
    (13, "BGP / ASN Info",          "IP Intel",   "both",  t13_bgp_asn,         "BGPView ASN & prefix data"),
    (35, "Reverse IP Lookup",       "IP Intel",   "both",  t35_reverse_ip,      "Domains co-hosted on IP"),
    # ── Reputation ──────────────────────────────────────────────────────
    (14, "GreyNoise Community",     "Reputation", "both",  t14_greynoise,       "GreyNoise IP context"),
    (15, "AbuseIPDB",               "Reputation", "both",  t15_abuseipdb,       "Abuse reports & score"),
    (16, "ThreatCrowd",             "Reputation", "both",  t16_threatcrowd,     "ThreatCrowd threat intel"),
    (26, "VirusTotal",              "Reputation", "both",  t26_virustotal,      "VirusTotal detections"),
    (27, "URLScan.io",              "Reputation", "both",  t27_urlscan,         "URLScan.io scan history"),
    # ── Subdomain Enum ──────────────────────────────────────────────────
    (17, "crt.sh Cert Transparency","Subdomains", "both",  t17_crtsh,           "Certificate transparency logs"),
    (18, "DNSDumpster / HackerTgt", "Subdomains", "both",  t18_dnsdumpster,     "DNS enumeration via HT API"),
    (34, "HackerTarget Subdomains", "Subdomains", "both",  t34_hackertarget_subs,"HackerTarget subdomain API"),
    (45, "Subfinder",               "Subdomains", "kali",  t45_subfinder,       "Fast passive subdomain enum"),
    (46, "Amass",                   "Subdomains", "kali",  t46_amass,           "Amass passive enum"),
    (47, "theHarvester",            "Subdomains", "kali",  t47_theharvester,    "Email & subdomain harvester"),
    # ── Web Analysis ────────────────────────────────────────────────────
    (19, "HTTP Headers",            "Web",        "both",  t19_http_headers,    "Full HTTP response headers"),
    (20, "SSL Certificate",         "Web",        "both",  t20_ssl_cert,        "SSL/TLS cert & cipher info"),
    (21, "Security Headers",        "Web",        "both",  t21_security_headers,"HSTS/CSP/etc. audit"),
    (22, "CORS Check",              "Web",        "both",  t22_cors_check,      "CORS misconfiguration probe"),
    (23, "robots.txt",              "Web",        "both",  t23_robots_txt,      "Fetch & parse robots.txt"),
    (24, "sitemap.xml",             "Web",        "both",  t24_sitemap,         "Find & parse sitemap"),
    (32, "HTML Meta Tags",          "Web",        "both",  t32_meta_tags,       "Page title & meta analysis"),
    (33, "Favicon Hash",            "Web",        "both",  t33_favicon_hash,    "Favicon hash for Shodan dork"),
    (36, "Tech Detection",          "Web",        "both",  t36_tech_detect,     "CMS/framework fingerprint"),
    (43, "WhatWeb",                 "Web",        "kali",  t43_whatweb,         "WhatWeb deep fingerprint"),
    (44, "WAF Detection (wafw00f)", "Web",        "kali",  t44_wafw00f,         "Web Application Firewall detect"),
    # ── Network ─────────────────────────────────────────────────────────
    (25, "Wayback Machine",         "Network",    "both",  t25_wayback,         "Internet Archive snapshots"),
    (28, "Ping",                    "Network",    "both",  t28_ping,            "ICMP echo test"),
    (29, "Traceroute",              "Network",    "both",  t29_traceroute,      "Network path tracing"),
    (30, "Banner Grabbing",         "Network",    "both",  t30_banner_grab,     "TCP service banners"),
    (31, "Port Scanner (Python)",   "Network",    "both",  t31_port_scan,       "Common ports quick scan"),
    # ── Port Scanning (nmap/masscan) ────────────────────────────────────
    (37, "Nmap Quick Scan",         "Port Scan",  "both",  t37_nmap_quick,      "nmap top 1000 ports"),
    (38, "Nmap Service Versions",   "Port Scan",  "both",  t38_nmap_service,    "nmap -sV service detect"),
    (39, "Nmap OS Detection",       "Port Scan",  "kali",  t39_nmap_os,         "nmap -O OS fingerprint"),
    (40, "Nmap Vuln Scripts",       "Port Scan",  "kali",  t40_nmap_vuln,       "nmap --script vuln"),
    (41, "Masscan Full Range",      "Port Scan",  "kali",  t41_masscan,         "masscan all 65535 ports"),
    # ── Web Vulnerabilities ─────────────────────────────────────────────
    (42, "Nikto Web Scan",          "Web Vuln",   "kali",  t42_nikto,           "Nikto web vuln scanner"),
    (50, "Gobuster Dirs",           "Web Vuln",   "kali",  t50_gobuster,        "Directory/file bruteforce"),
    # ── DNS Recon (Kali) ────────────────────────────────────────────────
    (48, "dnsrecon",                "DNS Recon",  "kali",  t48_dnsrecon,        "dnsrecon standard enum"),
    (49, "dnsenum",                 "DNS Recon",  "kali",  t49_dnsenum,         "dnsenum full enumeration"),
]

# ══════════════════════════════════════════════════════════════════════════
#  RESULT PRINTER
# ══════════════════════════════════════════════════════════════════════════
STATUS_SYM = {
    'ok':    lambda: f"{C.LM}[✓]{C.RS}",
    'warn':  lambda: f"{C.YW}[!]{C.RS}",
    'error': lambda: f"{C.RE}[✗]{C.RS}",
    'skip':  lambda: f"{C.DM}[─]{C.RS}",
}

def print_result(tid, name, cat, result, elapsed):
    sym = STATUS_SYM.get(result['status'], lambda: "[?]")()
    print(f"\n{C.DK}{'─'*62}{C.RS}")
    print(f" {sym} {C.BD}{C.LM}[{tid:02d}]{C.RS} {C.BD}{name}{C.RS} "
          f"{C.DK}[{cat}]{C.RS} {C.DM}({elapsed:.1f}s){C.RS}")
    print(f"{C.DK}{'─'*62}{C.RS}")
    status = result['status']
    data   = result['data']
    if status == 'ok':
        for line in data.split('\n'):
            print(f"  {C.GR}{line}{C.RS}")
    elif status == 'warn':
        for line in data.split('\n'):
            print(f"  {C.YW}{line}{C.RS}")
    elif status == 'error':
        print(f"  {C.RE}{data}{C.RS}")
    else:
        print(f"  {C.DM}{data}{C.RS}")

# ══════════════════════════════════════════════════════════════════════════
#  REPORT SAVER
# ══════════════════════════════════════════════════════════════════════════
def save_report(target_raw, t, all_results, elapsed, filename):
    ansi_re = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    lines = [
        "=" * 70,
        "TOOL DEFINITIVE — OSINT REPORT",
        "=" * 70,
        f"Target:    {target_raw}",
        f"Host:      {t['host']}",
        f"IP:        {t['ip']}",
        f"Domain:    {t['domain']}",
        f"Date:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Duration:  {elapsed:.1f}s",
        f"Tools run: {len(all_results)}",
        "=" * 70,
        "",
    ]
    for tid, name, cat, result, et in all_results:
        lines.append(f"[{tid:02d}] {name}  ({cat})  [{result['status'].upper()}]  ({et:.1f}s)")
        lines.append("-" * 55)
        lines.append(result['data'])
        lines.append("")
    clean = '\n'.join(ansi_re.sub('', l) for l in lines)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(clean)

# ══════════════════════════════════════════════════════════════════════════
#  RUNNER
# ══════════════════════════════════════════════════════════════════════════
def run_osint(target_raw: str, platform: str, output_file: str = None):
    print_banner()

    print(f" {C.GR}[*]{C.RS} Resolving: {C.LM}{target_raw}{C.RS}")
    t = resolve_target(target_raw)

    print(f" {C.GR}[*]{C.RS} Host:    {C.LM}{t['host']}{C.RS}")
    if t['ip'] and t['ip'] != t['host']:
        print(f" {C.GR}[*]{C.RS} IP:      {C.LM}{t['ip']}{C.RS}")
    print(f" {C.GR}[*]{C.RS} Type:    {C.LM}{'IP Address' if t['is_ip'] else 'Domain/URL'}{C.RS}")
    print(f" {C.GR}[*]{C.RS} Mode:    {C.LM}{platform.upper()}{C.RS}")

    if not t['host']:
        print(f" {C.RE}[!] Could not parse target. Aborting.{C.RS}")
        return

    # Filter by platform
    if platform.lower() == 'kali':
        run_tools = TOOLS
    else:
        run_tools = [tool for tool in TOOLS if tool[3] in ('both', 'termux')]

    total      = len(run_tools)
    start_time = time.time()

    print(f" {C.GR}[*]{C.RS} Launching {C.LM}{total}{C.RS} tools...\n")

    all_results = []
    for idx, (tid, name, cat, plat, func, desc) in enumerate(run_tools, 1):
        sys.stdout.write(f"\r {C.DK}[{idx}/{total}] Running: {name:<35}{C.RS}")
        sys.stdout.flush()
        t0 = time.time()
        try:
            result = func(t)
        except Exception as ex:
            result = err(f"Unhandled exception: {ex}")
        elapsed = time.time() - t0
        print_result(tid, name, cat, result, elapsed)
        all_results.append((tid, name, cat, result, elapsed))

    # ── Summary ──────────────────────────────────────────────────────
    total_time = time.time() - start_time
    counts = {s: sum(1 for _,_,_,r,_ in all_results if r['status']==s)
              for s in ('ok','warn','error','skip')}

    print(f"\n{C.LM}{'═'*62}{C.RS}")
    print(f" {C.BD}{C.LM}SCAN COMPLETE — {target_raw}{C.RS}")
    print(f"{C.LM}{'═'*62}{C.RS}")
    print(f"  Duration : {C.LM}{total_time:.1f}s{C.RS}")
    print(f"  Tools run: {C.LM}{total}{C.RS}")
    print(f"  {C.LM}✓ OK:{counts['ok']:3d}{C.RS}  "
          f"{C.YW}! Warn:{counts['warn']:3d}{C.RS}  "
          f"{C.RE}✗ Err:{counts['error']:3d}{C.RS}  "
          f"{C.DM}─ Skip:{counts['skip']:3d}{C.RS}")
    if output_file:
        save_report(target_raw, t, all_results, total_time, output_file)
        print(f"\n  {C.GR}Report saved →{C.RS} {C.LM}{output_file}{C.RS}")
    print(f"{C.LM}{'═'*62}{C.RS}\n")

# ══════════════════════════════════════════════════════════════════════════
#  TOOLS LIST DISPLAY
# ══════════════════════════════════════════════════════════════════════════
def print_tools_list():
    print_banner()
    both_n = sum(1 for t in TOOLS if t[3] == 'both')
    kali_n = sum(1 for t in TOOLS if t[3] == 'kali')
    print(f"  {C.BD}{C.LM}TOOL LIST  [{len(TOOLS)} total]{C.RS}  "
          f"{C.GR}BOTH (Termux+Kali): {both_n}{C.RS}  "
          f"{C.LM}Kali-only: {kali_n}{C.RS}\n")

    # Group by category
    categories = {}
    for row in TOOLS:
        tid, name, cat, plat, _, desc = row
        categories.setdefault(cat, []).append((tid, name, plat, desc))

    for cat, tools in categories.items():
        print(f"  {C.BD}{C.LM}┌─ {cat} {'─'*(32-min(len(cat),30))}┐{C.RS}")
        for tid, name, plat, desc in tools:
            tag = f"{C.GR}[BOTH]{C.RS}" if plat == 'both' else f"{C.LM}[KALI]{C.RS}"
            print(f"  {C.DK}│{C.RS}  {C.GR}{tid:02d}{C.RS}. "
                  f"{C.LM}{name:<32}{C.RS} {tag}  {C.DM}{desc}{C.RS}")
        print(f"  {C.DK}└{'─'*44}┘{C.RS}")
        print()

# ══════════════════════════════════════════════════════════════════════════
#  HELP TEXT
# ══════════════════════════════════════════════════════════════════════════
HELP_TEXT = f"""
{C.LM}TOOL DEFINITIVE — Massive OSINT Suite  v{VERSION}{C.RS}
{C.GR}{'─'*55}{C.RS}

{C.BD}USAGE:{C.RS}
  {C.LM}python3 tool_definitive.py [OPTIONS]{C.RS}

{C.BD}OPTIONS:{C.RS}
  {C.GR}-t TARGET{C.RS}    IP address, domain, or full URL
  {C.GR}-m MODE  {C.RS}    {C.LM}kali{C.RS} | {C.LM}termux{C.RS}  (default: auto-detect)
  {C.GR}-o FILE  {C.RS}    Save report to text file
  {C.GR}--tools  {C.RS}    Show all 50 tools with details
  {C.GR}--menu   {C.RS}    Launch interactive menu (default if no args)
  {C.GR}-h       {C.RS}    This help message

{C.BD}MODES:{C.RS}
  {C.LM}kali   {C.RS}  All 50 tools — includes nmap/nikto/masscan/amass/etc.
  {C.LM}termux {C.RS}  37 tools  — Python + API based (no Kali-specific binaries)
  {C.DK}(auto-detects Termux by checking PREFIX/com.termux){C.RS}

{C.BD}EXAMPLES:{C.RS}
  {C.GR}python3 tool_definitive.py -t example.com -m kali{C.RS}
  {C.GR}python3 tool_definitive.py -t 8.8.8.8 -m termux{C.RS}
  {C.GR}python3 tool_definitive.py -t https://target.com -m kali -o rep.txt{C.RS}
  {C.GR}python3 tool_definitive.py --tools{C.RS}
  {C.GR}python3 tool_definitive.py --menu{C.RS}

{C.BD}INSTALL DEPS (Kali):{C.RS}
  {C.DK}sudo apt install nmap nikto whatweb wafw00f masscan amass dnsrecon{C.RS}
  {C.DK}sudo apt install dnsenum gobuster theharvester subfinder{C.RS}
  {C.DK}pip install requests{C.RS}

{C.BD}INSTALL DEPS (Termux):{C.RS}
  {C.DK}pkg install nmap traceroute dnsutils whois{C.RS}
  {C.DK}pip install requests{C.RS}

{C.GR}{'─'*55}{C.RS}
"""

# ══════════════════════════════════════════════════════════════════════════
#  INTERACTIVE MENU
# ══════════════════════════════════════════════════════════════════════════
def interactive_menu():
    while True:
        os.system('clear' if os.name != 'nt' else 'cls')
        print_banner()
        print(f"  {C.BD}{C.LM}╔══════════ MAIN MENU ══════════╗{C.RS}")
        print(f"  {C.BD}{C.LM}║{C.RS}  {C.GR}[1]{C.RS} Scan  ─  {C.LM}Kali mode{C.RS}       {C.BD}{C.LM}║{C.RS}")
        print(f"  {C.BD}{C.LM}║{C.RS}  {C.GR}[2]{C.RS} Scan  ─  {C.LM}Termux mode{C.RS}     {C.BD}{C.LM}║{C.RS}")
        print(f"  {C.BD}{C.LM}║{C.RS}  {C.GR}[3]{C.RS} List all {C.LM}50 tools{C.RS}        {C.BD}{C.LM}║{C.RS}")
        print(f"  {C.BD}{C.LM}║{C.RS}  {C.GR}[4]{C.RS} {C.LM}Help{C.RS} & install guide     {C.BD}{C.LM}║{C.RS}")
        print(f"  {C.BD}{C.LM}║{C.RS}  {C.GR}[0]{C.RS} {C.RE}Exit{C.RS}                     {C.BD}{C.LM}║{C.RS}")
        print(f"  {C.BD}{C.LM}╚═══════════════════════════════╝{C.RS}\n")

        choice = input(f"  {C.LM}→ {C.RS}").strip()

        if choice in ('1', '2'):
            mode = 'kali' if choice == '1' else 'termux'
            target = input(f"\n  {C.GR}[?] Target (IP / domain / URL):{C.RS} ").strip()
            if not target:
                print(f"  {C.RE}No target entered.{C.RS}")
                time.sleep(1)
                continue
            save = input(f"  {C.GR}[?] Save report to file? (filename or blank):{C.RS} ").strip()
            run_osint(target, mode, save or None)
            input(f"\n  {C.DM}Press Enter to return to menu...{C.RS}")

        elif choice == '3':
            os.system('clear' if os.name != 'nt' else 'cls')
            print_tools_list()
            input(f"\n  {C.DM}Press Enter to return to menu...{C.RS}")

        elif choice == '4':
            os.system('clear' if os.name != 'nt' else 'cls')
            print_banner()
            print(HELP_TEXT)
            input(f"\n  {C.DM}Press Enter to return to menu...{C.RS}")

        elif choice == '0':
            print(f"\n  {C.DK}Goodbye.{C.RS}\n")
            sys.exit(0)
        else:
            print(f"  {C.RE}Invalid option.{C.RS}")
            time.sleep(0.8)

# ══════════════════════════════════════════════════════════════════════════
#  PLATFORM DETECTION
# ══════════════════════════════════════════════════════════════════════════
def detect_platform() -> str:
    if 'com.termux' in os.environ.get('PREFIX', ''):
        return 'termux'
    if os.path.exists('/data/data/com.termux'):
        return 'termux'
    if os.path.exists('/etc/kali_version') or os.path.exists('/etc/kali-release'):
        return 'kali'
    return 'kali'  # default

# ══════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Tool Definitive — Massive OSINT Suite',
        add_help=False
    )
    parser.add_argument('-t', '--target',       help='Target IP, domain, or URL')
    parser.add_argument('-m', '--mode',         choices=['kali', 'termux'],
                        help='Platform mode')
    parser.add_argument('-o', '--output',       help='Output report filename')
    parser.add_argument('--tools',  action='store_true', help='List all tools')
    parser.add_argument('--menu',   action='store_true', help='Interactive menu')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')

    args = parser.parse_args()

    # No arguments → interactive menu
    if len(sys.argv) == 1 or args.menu:
        interactive_menu()
        return

    if args.help:
        print_banner()
        print(HELP_TEXT)
        return

    if args.tools:
        print_tools_list()
        return

    if args.target:
        platform = args.mode or detect_platform()
        run_osint(args.target, platform, args.output)
    else:
        print_banner()
        print(HELP_TEXT)


if __name__ == '__main__':
    main()
