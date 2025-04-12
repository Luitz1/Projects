import os
from PIL import Image

# Carpeta de entrada y salida
input_folder = os.path.join(os.path.dirname(__file__), "in")
output_folder = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(output_folder, exist_ok=True)
os.makedirs(input_folder, exist_ok=True)

# Selección de DPI
print("Selecciona el DPI para el PDF:")
print("1. 150 DPI")
print("2. 300 DPI")
print("3. 500 DPI")
dpi_option = input("Elige una opción (1/2/3): ")
dpi_map = {"1": 150, "2": 300, "3": 500}
dpi = dpi_map.get(dpi_option, 300)

# Leer imágenes
image_files = sorted(
    [f for f in os.listdir(input_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
)

if not image_files:
    print("No se encontraron imágenes en la carpeta 'in'.")
    exit()

images = []
for image_file in image_files:
    img_path = os.path.join(input_folder, image_file)
    with Image.open(img_path) as img:
        images.append(img.convert("RGB"))

# Función para generar nombre único de archivo
def generar_nombre_unico(base_path, base_name="output", ext=".pdf"):
    i = 1
    nuevo_path = os.path.join(base_path, f"{base_name}{ext}")
    while os.path.exists(nuevo_path):
        nuevo_path = os.path.join(base_path, f"{base_name}_{i}{ext}")
        i += 1
    return nuevo_path

# Guardar PDF con nombre único
output_pdf_path = generar_nombre_unico(output_folder)
if images:
    images[0].save(
        output_pdf_path,
        save_all=True,
        append_images=images[1:],
        resolution=dpi,
    )
    print(f"PDF generado: {output_pdf_path}")
else:
    print("No se pudieron procesar las imágenes.")

