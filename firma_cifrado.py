
from getpass import getpass
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# 1. Generar clave privada ECDSA con la curva P-256
clave_privada = ec.generate_private_key(ec.SECP256R1())

# 2. Obtener la clave publica correspondiente
clave_publica = clave_privada.public_key()

# 3. Solicitar una contraseña para proteger la clave privada
password = getpass("Crea una contraseña para tu clave privada: ")

if not password:
    raise ValueError("La contraseña no puede estar vacia.")

# 4. Preparar la clave privada cifrada
clave_privada_pem = clave_privada.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(
        password.encode("utf-8")
    )
)

# 5. Guardar la clave privada sin sobrescribir una existente
with open("clave_privada.pem", "xb") as archivo:
    archivo.write(clave_privada_pem)

# 6. Guardar la clave publica correspondiente
with open("clave_publica.pem", "xb") as archivo:
    archivo.write(
        clave_publica.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Claves ECDSA generadas correctamente.")
