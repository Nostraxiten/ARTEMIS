# ARTEMIS: ADVANCED NETWORK ANALYSIS AND RECONNAISSANCE FRAMEWORK

## DESCRIPCIÓN TÉCNICA
ARTEMIS es un framework de auditoría de seguridad y análisis de redes desarrollado íntegramente en Python. Esta herramienta ha sido diseñada para centralizar vectores de ataque y reconocimiento en una única interfaz automatizada, optimizando el flujo de trabajo tanto en entornos profesionales de pruebas de penetración como en entornos de aprendizaje de ciberseguridad.

El núcleo de ARTEMIS implementa una arquitectura modular que permite la integración de herramientas líderes en la industria para realizar escaneos de vulnerabilidades, enumeración de servicios y análisis de tráfico de red de forma sistemática.

## CAPACIDADES Y COMPATIBILIDAD
La herramienta detecta automáticamente el entorno de ejecución para desplegar el arsenal correspondiente a las capacidades del hardware y del sistema operativo:

### ENTORNO KALI LINUX (ESTACIÓN DE TRABAJO)
Para despliegues en distribuciones basadas en Debian orientadas a la seguridad, ARTEMIS integra un total de 50 herramientas de análisis profundo. Esto incluye, entre otros:

* Escaneo avanzado de puertos y detección de versiones (Nmap).
* Enumeración de servicios DNS, SMB y protocolos de red.
* Análisis de vulnerabilidades web y de infraestructura.
* Herramientas de explotación y post-explotación integradas.

### ENTORNO TERMUX (DISPOSITIVOS MÓVILES)
Para operaciones de movilidad y portabilidad, la versión de Termux incluye una suite optimizada de más de 30 herramientas seleccionadas por su eficiencia en procesadores ARM, permitiendo realizar auditorías de red desde dispositivos Android sin sacrificar la profundidad técnica del análisis.

## DINÁMICA DE EJECUCIÓN Y REGISTRO
Debido a la exhaustividad de los procesos de análisis y a la cantidad de herramientas de terceros que se invocan, el tiempo de ejecución es prolongado. El sistema procesa grandes volúmenes de datos, por lo que se requiere una ejecución continua y estable.

## GENERACIÓN DE REPORTES
ARTEMIS incluye una función de persistencia de datos. Durante la ejecución, el usuario tiene la opción de exportar todos los resultados obtenidos a un archivo de registro en formato de texto plano (.txt). Este reporte técnico detalla cronológicamente cada hallazgo realizado por las herramientas integradas para su posterior revisión o inclusión en informes de auditoría.

## INSTALACIÓN Y REQUISITOS
Para garantizar el correcto funcionamiento del framework, es imperativo cumplir con las dependencias del sistema y de Python.

1. Clonación del repositorio:
```bash
git clone https://github.com/nostraxiten/ARTEMIS.git
cd ARTEMIS

2. Dependencias Kali:

sudo apt update && sudo apt install -y nmap dnsutils whois traceroute gobuster theharvester subfinder amass wafw00f nikto whatweb masscan dnsrecon dnsenum

2.1. Dependencia Termux:

pkg update && pkg install -y nmap dnsutils whois traceroute gobuster subfinder amass nikto whatweb dnsrecon dnsutils

3. Ejecución:

python artemis.py


AVISO LEGAL Y ÉTICO

El uso de ARTEMIS para realizar actividades de acceso no autorizado en sistemas de los cuales no se posee autorización explícita es ilegal. Este software ha sido desarrollado con fines exclusivamente académicos y de auditoría ética. El desarrollador no asume responsabilidad alguna por daños o consecuencias legales derivados del uso inadecuado o malintencionado de esta herramienta.

PROYECTO ARTEMIS





