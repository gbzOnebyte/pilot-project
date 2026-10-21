"""Prototipo de 'buzón de verificación' de correos sospechosos.

Recibe un correo (.eml o texto plano) y devuelve un nivel de riesgo y las reglas activadas.
Usa las mismas 6 reglas del experimento y, si existe, el modelo entrenado
(`modelo_hibrido.joblib`, generado por el cuaderno).

AVISO: es una prueba de concepto académica. El modelo se entrenó con datos públicos en inglés
y con sesgo de fuente; NO debe usarse para bloquear correos reales sin validación local
(ver IMPLEMENTACION.md).

Uso:
    python verificador.py correo.eml
    python verificador.py correo.txt --modelo ../modelo_hibrido.joblib
"""
import argparse
import re
import sys
from email import policy
from email.parser import BytesParser
from pathlib import Path

URGENCIA = r"urgent|immediately|within 24|expire|suspend|deactivat|final notice|act now|urgente|inmediatamente|suspendid|expira"
CREDENCIALES = r"password|username|login|log in|sign in|verify your|confirm your|credential|contraseña|verifique|confirme"
ACCION = r"click here|click the link|follow the link|update your|haga clic|actualice"
CUENTA = r"your account|mailbox|helpdesk|help desk|it-service|security alert|su cuenta|buzón"
IP_URL = r"https?://\d{1,3}(\.\d{1,3}){3}"

REGLAS = {
    "R1 lenguaje de urgencia": lambda t, u: bool(re.search(URGENCIA, t)),
    "R2 pide credenciales": lambda t, u: bool(re.search(CREDENCIALES, t)),
    "R3 invita a hacer clic/actualizar": lambda t, u: bool(re.search(ACCION, t)),
    "R4 menciona cuenta/buzón/soporte": lambda t, u: bool(re.search(CUENTA, t)),
    "R5 contiene enlaces": lambda t, u: u > 0 or "http" in t,
    "R6 enlace con dirección IP": lambda t, u: bool(re.search(IP_URL, t)),
}

# Umbrales de ejemplo: deben definirse junto con el área de TI durante el piloto.
UMBRAL_MEDIO, UMBRAL_ALTO = 0.35, 0.65


def leer_correo(ruta: Path) -> str:
    if ruta.suffix.lower() == ".eml":
        msg = BytesParser(policy=policy.default).parsebytes(ruta.read_bytes())
        cuerpo = msg.get_body(preferencelist=("plain", "html"))
        texto = cuerpo.get_content() if cuerpo else ""
        return f"{msg.get('subject', '')} {texto}"
    return ruta.read_text(encoding="utf-8", errors="ignore")


def analizar(texto: str, paquete_modelo=None) -> dict:
    t = texto.lower()
    urls = len(re.findall(r"https?://", t))
    activadas = [n for n, f in REGLAS.items() if f(t, urls)]
    puntaje = len(activadas)
    p_reglas = puntaje / len(REGLAS)
    p_ml = None
    if paquete_modelo is not None:
        p_ml = float(paquete_modelo["pipeline"].predict_proba([texto])[0, 1])
        alpha = paquete_modelo["alpha"]
        p_final = (1 - alpha) * p_ml + alpha * p_reglas
    else:
        p_final = p_reglas
    nivel = "ALTO" if p_final >= UMBRAL_ALTO else "MEDIO" if p_final >= UMBRAL_MEDIO else "BAJO"
    return {"nivel": nivel, "p_final": p_final, "p_ml": p_ml, "puntaje_reglas": puntaje, "reglas": activadas}


def main():
    ap = argparse.ArgumentParser(description="Verificador de correos sospechosos (prototipo)")
    ap.add_argument("correo", type=Path, help="archivo .eml o .txt con el correo")
    ap.add_argument("--modelo", type=Path, default=Path("modelo_hibrido.joblib"))
    a = ap.parse_args()
    paquete = None
    if a.modelo.exists():
        import joblib
        paquete = joblib.load(a.modelo)
    else:
        print("(Sin modelo entrenado: se usan solo las reglas.)", file=sys.stderr)
    r = analizar(leer_correo(a.correo), paquete)
    print(f"Nivel de riesgo: {r['nivel']}  (puntaje combinado {r['p_final']:.2f})")
    if r["p_ml"] is not None:
        print(f"Probabilidad del modelo: {r['p_ml']:.2f}")
    print(f"Reglas activadas ({r['puntaje_reglas']}/{len(REGLAS)}):")
    for n in r["reglas"] or ["ninguna"]:
        print("  -", n)
    print("Recomendación: no haga clic en enlaces ni entregue credenciales; ante la duda, consulte a TI.")


if __name__ == "__main__":
    main()
