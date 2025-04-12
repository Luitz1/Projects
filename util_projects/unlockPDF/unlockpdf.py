import os
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox

def unlock_pdf(input_pdf, output_pdf, password):
    """
    Unlock a PDF file protected with password and keep a copy without password.

    : Param input_pdf: Protected PDF file.
    : Param output_pdf: Route where the PDF will be stored without password.
    : Param Password: PDF file password.
    """
    try:
        with open(input_pdf, 'rb') as infile:
            reader = PyPDF2.PdfReader(infile)

            # Descifrar con la contraseña
            if reader.decrypt(password):
                writer = PyPDF2.PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)
                
                # Crear carpeta "out" si no existe
                output_folder = os.path.dirname(output_pdf)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                
                # Guardar el PDF desbloqueado
                with open(output_pdf, 'wb') as outfile:
                    writer.write(outfile)
                
                return f"El archivo PDF ha sido desbloqueado y guardado en: {output_pdf}"
            else:
                return "La contraseña proporcionada es incorrecta."
    except Exception as e:
        return f"Ocurrió un error: {e}"

def browse_file():
    """Permite al usuario seleccionar un archivo PDF protegido."""
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def unlock_and_save():
    """Obtiene los datos del formulario, desbloquea el PDF y guarda la copia sin contraseña."""
    input_pdf = entry_file.get()
    password = entry_password.get()
    
    if not input_pdf or not password:
        messagebox.showerror("Error", "Por favor, selecciona un archivo PDF e ingresa la contraseña.")
        return
    
    output_pdf = os.path.join("out", os.path.basename(input_pdf))
    result = unlock_pdf(input_pdf, output_pdf, password)
    messagebox.showinfo("Resultado", result)
    
    root.destroy()

# Crear ventana principal
root = tk.Tk()
root.title("Desbloquear PDF")
root.geometry("400x200")

# Etiquetas y campos de entrada
label_file = tk.Label(root, text="Archivo PDF:")
label_file.pack(pady=5)
entry_file = tk.Entry(root, width=40)
entry_file.pack(pady=5)
btn_browse = tk.Button(root, text="Buscar", command=browse_file)
btn_browse.pack(pady=5)

label_password = tk.Label(root, text="Contraseña:")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*", width=40)
entry_password.pack(pady=5)

# Botón para desbloquear
btn_unlock = tk.Button(root, text="Desbloquear y Guardar", command=unlock_and_save)
btn_unlock.pack(pady=20)

# Ejecutar aplicación
root.mainloop()