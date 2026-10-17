# Sistema de Firmado Digital y Cifrado de Documentos

## 1. Descripción del proyecto

Este proyecto implementa un sistema de **firma digital, cifrado, descifrado y verificación de documentos médicos** utilizando Python y la biblioteca `cryptography`.

El objetivo es demostrar la aplicación de diferentes mecanismos criptográficos para proteger la información de un documento durante su almacenamiento y recepción.

Se utilizan los siguientes algoritmos:

| Algoritmo | Función |
|---|---|
| ECDSA (curva P-256) | Generación y verificación de firmas digitales |
| SHA-256 | Función hash utilizada en la firma digital |
| AES-256-CBC | Cifrado y descifrado del documento |
| RSA-OAEP | Protección y recuperación de la llave AES |
| PKCS7 | Relleno de datos para el cifrado AES-CBC |

El sistema permite demostrar tres propiedades de seguridad: **confidencialidad, integridad y autenticidad**.

## 2. Requisitos

Para ejecutar el proyecto se necesita:

- Python 3.13 o una versión compatible.
- Visual Studio Code o cualquier editor de Python.
- Biblioteca `cryptography`.
- Git (opcional, para clonar el repositorio).

## 3. Descargar el proyecto

Repositorio de GitHub:

https://github.com/Montu56/Firmado_Cifrado_Documento

Para clonarlo desde una terminal:

```bash
git clone https://github.com/Montu56/Firmado_Cifrado_Documento.git
```

Ingresar a la carpeta:

```bash
cd Firmado_Cifrado_Documento
```

También es posible descargar el proyecto desde GitHub utilizando la opción **Code → Download ZIP**.

## 4. Configuración del entorno

### Crear un entorno virtual (recomendado)

Desde la terminal de Visual Studio Code:

```bash
python -m venv venv
```

Activarlo en Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, puede utilizarse temporalmente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después, ejecutar nuevamente el comando de activación.

### Instalar las dependencias

```bash
python -m pip install cryptography
```

Con esto el entorno queda preparado.

## 5. Archivos principales

| Archivo | Descripción |
|---|---|
| `firma_cifrado.py` | Genera las claves pública y privada ECDSA |
| `firmar_documento.py` | Firma digitalmente el documento utilizando ECDSA y SHA-256 |
| `cifrar_documento.py` | Cifra el documento mediante AES-256-CBC |
| `proteger_clave_aes.py` | Protege la llave AES utilizando RSA-OAEP |
| `descifrar_documento.py` | Recupera la llave AES y descifra el documento |
| `verificar_firma.py` | Verifica la firma digital del documento recuperado |
| `documento.txt` | Documento original de prueba |

## 6. Instrucciones de ejecución

**Importante:** los siguientes pasos deben ejecutarse en orden, especialmente durante la primera ejecución.

### Paso 1. Generar las claves ECDSA

Ejecutar:

```bash
python firma_cifrado.py
```

El programa solicitará crear una contraseña para proteger la clave privada ECDSA.

Archivos generados:

- `clave_privada.pem`
- `clave_publica.pem`

La clave privada se utiliza para firmar documentos y la clave pública para verificar las firmas.

**Guardar la contraseña**, ya que se necesitará en el siguiente paso.

### Paso 2. Firmar el documento

Ejecutar:

```bash
python firmar_documento.py
```

Ingresar la contraseña de la clave privada ECDSA.

El programa:

1. Lee `documento.txt`.
2. Utiliza ECDSA y SHA-256 para generar la firma digital.
3. Guarda la firma en `firma_documento.bin`.

Resultado esperado:

```text
Documento firmado correctamente con ECDSA.
Firma guardada en firma_documento.bin
```

### Paso 3. Cifrar el documento con AES-256-CBC

Ejecutar:

```bash
python cifrar_documento.py
```

El programa:

1. Lee el documento original.
2. Genera una llave AES aleatoria de 256 bits.
3. Genera un IV aleatorio de 128 bits.
4. Aplica padding PKCS7.
5. Cifra el documento mediante AES-256-CBC.
6. Guarda el documento cifrado y la llave AES.

Archivos generados:

- `documento_cifrado.bin`
- `clave_aes.key`

El archivo cifrado contiene el IV seguido del contenido cifrado.

**Advertencia:** no ejecutar nuevamente este programa sobre una operación existente sin respaldar los archivos. Una nueva ejecución puede sobrescribir el documento cifrado y provocar una incompatibilidad con la llave AES anterior.

### Paso 4. Proteger la llave AES mediante RSA-OAEP

Ejecutar:

```bash
python proteger_clave_aes.py
```

El programa:

1. Lee la llave AES generada anteriormente.
2. Genera un par de claves RSA de 3072 bits.
3. Solicita crear una contraseña para proteger la clave privada RSA.
4. Cifra la llave AES utilizando la clave pública RSA y RSA-OAEP.
5. Guarda la llave AES cifrada.

Archivos generados:

- `rsa_privada.pem`
- `rsa_publica.pem`
- `clave_aes_envuelta.bin`

**Importante:** recordar la contraseña RSA. Se utilizará durante el descifrado.

Este programa evita sobrescribir las claves RSA existentes.

### Paso 5. Descifrar el documento

Ejecutar:

```bash
python descifrar_documento.py
```

Ingresar la contraseña de la clave privada RSA.

El programa realiza dos operaciones principales:

**Primera operación: RSA-OAEP**

Utiliza la clave privada RSA para recuperar la llave AES almacenada en `clave_aes_envuelta.bin`.

**Segunda operación: AES-256-CBC**

Utiliza la llave AES recuperada y el IV almacenado en el archivo cifrado para descifrar el documento.

Después elimina el padding PKCS7 y genera:

- `documento_descifrado.txt`

Resultado esperado:

```text
Llave AES recuperada correctamente.
Documento descifrado correctamente con AES-256-CBC.
Archivo generado: documento_descifrado.txt
```

### Paso 6. Verificar la firma digital

Ejecutar:

```bash
python verificar_firma.py
```

El programa utiliza:

- `documento_descifrado.txt`
- `firma_documento.bin`
- `clave_publica.pem`

Mediante ECDSA y SHA-256, verifica que la firma corresponda al contenido del documento recibido.

Resultado esperado:

```text
Firma valida: el documento no fue alterado.
```

Si la firma no corresponde al documento, se mostrará un mensaje indicando que es inválida.

## 7. Flujo completo del sistema

**Proceso del emisor:**

```text
documento.txt
    |
    | ECDSA + SHA-256
    v
firma_documento.bin

documento.txt
    |
    | AES-256-CBC
    v
documento_cifrado.bin

clave_aes.key
    |
    | RSA-OAEP (clave pública RSA)
    v
clave_aes_envuelta.bin
```

**Proceso del receptor:**

```text
clave_aes_envuelta.bin
    +
clave privada RSA
    |
    | RSA-OAEP
    v
Llave AES recuperada
    +
documento_cifrado.bin
    |
    | AES-256-CBC
    v
documento_descifrado.txt
    +
firma_documento.bin
    +
clave pública ECDSA
    |
    | ECDSA + SHA-256
    v
Verificación de la firma digital
```

## 8. Consideraciones de seguridad

- Las claves privadas ECDSA y RSA deben mantenerse confidenciales.
- La llave AES es una llave secreta simétrica, no una clave pública.
- Las contraseñas de las claves privadas deben guardarse de forma segura.
- Las claves privadas no deben subirse a repositorios públicos.
- La clave pública ECDSA debe obtenerse de una fuente confiable para verificar la identidad del firmante.
- AES-256-CBC proporciona confidencialidad, pero no autenticación del texto cifrado por sí solo.
- La firma ECDSA permite verificar la integridad del documento firmado y su relación con la clave pública utilizada.
- El archivo `clave_aes.key` se conserva sin cifrar únicamente para fines demostrativos.

**Nota:** esta implementación es un prototipo académico. Para utilizarla con expedientes médicos reales serían necesarias medidas adicionales, como gestión segura de claves, cifrado autenticado, controles de acceso y protección de datos personales.

## 9. Recomendaciones para los integrantes del equipo

Cada integrante que descargue el repositorio deberá:

1. Instalar Python y la biblioteca `cryptography`.
2. Ejecutar los programas en el orden indicado.
3. Generar sus propias claves y contraseñas para las pruebas locales.
4. Evitar compartir claves privadas o llaves AES sin protección.
5. Utilizar documentos ficticios para realizar las pruebas.

**Importante:** si se desea verificar la firma de otro integrante, debe utilizarse la clave pública ECDSA correspondiente a la clave privada con la que se firmó el documento. No funcionará una clave pública generada independientemente.

Asimismo, el prototipo actual simula el proceso de emisión y recepción dentro de un mismo entorno. Para intercambiar documentos entre diferentes equipos, es necesario gestionar las claves del receptor y los archivos transmitidos.

## 10. Estado actual del proyecto

El prototipo permite ejecutar el flujo completo:

**Generación de claves → Firma digital → Cifrado AES → Protección RSA de la llave AES → Descifrado → Verificación ECDSA.**

El sistema constituye una demostración de criptografía híbrida aplicada a la protección de documentos.