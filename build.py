import os
import shutil
import subprocess

print("▶ Compilando Jobbi con PyInstaller...")
subprocess.run(["pyinstaller", "jobbi.spec", "--noconfirm"], check=True)

print("▶ Copiando .env a dist/Jobbi/...")
origen  = os.path.join(os.path.dirname(__file__), ".env")
destino = os.path.join(os.path.dirname(__file__), "dist", "Jobbi", ".env")

if os.path.exists(origen):
    shutil.copy2(origen, destino)
    print(f"✅ .env copiado a {destino}")
else:
    print(f"⚠️  No se encontró .env en {origen}")

print("✅ Build completo. Ejecutable en dist/Jobbi/Jobbi.exe")