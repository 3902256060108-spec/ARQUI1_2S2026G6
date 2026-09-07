from pathlib import Path
import subprocess


BASE_DIR = Path(__file__).resolve().parent.parent

ARM64_DIR = BASE_DIR / "arm64"

DATOS_FILE = ARM64_DIR / "datos.txt"
RESULTADO_FILE = ARM64_DIR / "resultado.txt"
ARM64_EXECUTABLE = ARM64_DIR / "main"


def generar_datos(temperaturas):
    with open(DATOS_FILE, "w", encoding="utf-8") as archivo:
        for temperatura in temperaturas:
            archivo.write(f"{int(temperatura)}\n")

        archivo.write("$\n")


def ejecutar_arm64():
    if not ARM64_EXECUTABLE.exists():
        raise FileNotFoundError(
            f"No existe el ejecutable ARM64: {ARM64_EXECUTABLE}"
        )

    resultado = subprocess.run(
        [str(ARM64_EXECUTABLE)],
        cwd=ARM64_DIR,
        capture_output=True,
        text=True
    )

    if resultado.returncode != 0:
        raise RuntimeError(
            "El programa ARM64 terminó con error.\n"
            f"Código: {resultado.returncode}\n"
            f"Error: {resultado.stderr}"
        )


def leer_resultados():
    if not RESULTADO_FILE.exists():
        raise FileNotFoundError(
            f"No existe resultado.txt: {RESULTADO_FILE}"
        )

    resultados = {}

    with open(RESULTADO_FILE, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            clave, valor = linea.split("=", 1)
            resultados[clave] = int(valor)

    return resultados


if __name__ == "__main__":
    temperaturas_prueba = [
        25,
        27,
        23,
        26,
        24
    ]

    print("Generando datos.txt...")
    generar_datos(temperaturas_prueba)

    print("Ejecutando módulo ARM64...")
    ejecutar_arm64()

    print("Leyendo resultado.txt...")
    resultados = leer_resultados()

    print("\nResultados calculados por ARM64:")

    for clave, valor in resultados.items():
        print(f"{clave} = {valor}")