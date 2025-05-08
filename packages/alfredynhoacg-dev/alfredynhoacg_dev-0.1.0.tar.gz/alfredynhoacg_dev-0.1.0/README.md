# Mi Librería

Esta es mi primera librería en Python. Incluye una función para saludar.

## Instalación

```bash
pip install alfred



from mi_libreria import saludar

print(saludar("Mundo"))


---

### **4. Crear el archivo `pyproject.toml`**
Este archivo define cómo construir tu proyecto. Crea un archivo `pyproject.toml` con el siguiente contenido:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"