from pathlib import Path
from getpass import getpass

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# 1. Localizar la llave AES
carpeta = Path(__file__).resolve().parent
ruta_aes = carpeta / "clave_aes.key"

if not ruta_aes.exists():
    raise SystemExit("Error: no se encuentra clave_aes.key")

clave_aes = ruta_aes.read_bytes()

if len(clave_aes) != 32:
    raise SystemExit("Error: la llave AES debe tener 256 bits.")

# Evitar sobrescribir claves existentes
archivos_salida = [
    carpeta / "rsa_privada.pem",
    carpeta / "rsa_publica.pem",
    carpeta / "clave_aes_envuelta.bin"
]

if any(ruta.exists() for ruta in archivos_salida):
    raise SystemExit("Ya existen archivos RSA. No se sobrescribieron.")

# 2. Generar claves RSA
clave_privada = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072
)

clave_publica = clave_privada.public_key()

# 3. Proteger la clave privada con contraseña
contrasena = getpass("Crea una contraseña para RSA: ")

if not contrasena:
    raise SystemExit("La contraseña no puede estar vacía.")

# 4. Guardar clave privada RSA
(carpeta / "rsa_privada.pem").write_bytes(
    clave_privada.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            contrasena.encode("utf-8")
        )
    )
)

# 5. Guardar clave pública RSA
(carpeta / "rsa_publica.pem").write_bytes(
    clave_publica.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
)

# 6. Proteger la llave AES mediante RSA-OAEP
clave_aes_envuelta = clave_publica.encrypt(
    clave_aes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 7. Guardar llave AES protegida
(carpeta / "clave_aes_envuelta.bin").write_bytes(
    clave_aes_envuelta
)

print("Claves RSA generadas correctamente.")
print("Llave AES protegida mediante RSA-OAEP.")
print("Archivo generado: clave_aes_envuelta.bin")