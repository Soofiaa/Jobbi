# crear_icono.py  (ejecutar una vez, luego borrar)
from PIL import Image, ImageDraw
import os

os.makedirs("assets", exist_ok=True)

img = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse([20, 20, 236, 236], fill="#4f8ef7")
draw.text((78, 80), "J", fill="white")
img.save("assets/icon.ico", format="ICO",
         sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])

print("✅ Ícono creado en assets/icon.ico")