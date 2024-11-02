import subprocess
import sys

# Lista delle librerie richieste
REQUIRED_LIBRARIES = [
    "requests",
    "beautifulsoup4",
]

def install_and_import(package):
    try:
        # Prova a importare il pacchetto
        __import__(package)
    except ImportError:
        # Se fallisce, installa il pacchetto
        print(f"Il pacchetto '{package}' non è installato. Installazione in corso...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    # Controlla e installa ciascun pacchetto della lista
    for library in REQUIRED_LIBRARIES:
        # BeautifulSoup si importa come `bs4`, quindi facciamo un controllo speciale
        package_name = "bs4" if library == "beautifulsoup4" else library
        install_and_import(package_name)
    print("Tutte le librerie sono installate e pronte.")

if __name__ == "__main__":
    main()
