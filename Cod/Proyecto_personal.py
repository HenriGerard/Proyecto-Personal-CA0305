# -*- coding: utf-8 -*-
"""
Created on Fri May 24 08:43:24 2024

@author: HGGH
"""

#!pip install yt-dlp
#!pip install beautifulsoup4

import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os
from pytube import YouTube

class Buscador:
    
    """
    Una clase para crear una aplicación GUI que busca y descarga imágenes y videos de la web.

    Atributos:
    ----------
    root : tk.Tk
        La ventana principal de la aplicación.
    var : tk.StringVar
        Variable para almacenar la opción seleccionada (imágenes o videos).
    bg_image : tk.PhotoImage
        Imagen de fondo de la ventana.
    bg_label : tk.Label
        Etiqueta que contiene la imagen de fondo.
    label : tk.Label
        Etiqueta principal que indica el propósito de la aplicación.
    label_adicional : tk.Label
        Etiqueta que indica que se debe ingresar una palabra clave o URL del video.
    entry_search : tk.Text
        Campo de texto para ingresar la palabra clave o URL del video.
    options_frame : tk.Frame
        Marco que contiene los botones de opción para seleccionar entre imágenes y videos.
    radio_images : tk.Radiobutton
        Botón de opción para seleccionar la búsqueda de imágenes.
    radio_videos : tk.Radiobutton
        Botón de opción para seleccionar la búsqueda de videos.
    label_num_images : tk.Label
        Etiqueta para el campo de entrada del número de imágenes a descargar.
    entry_num_images : tk.Entry
        Campo de entrada para ingresar el número de imágenes a descargar.
    search_button : tk.Button
        Botón para iniciar la búsqueda y descarga de imágenes o videos.

    Métodos:
    --------
    get_search_term():
        Obtiene el término de búsqueda ingresado por el usuario.
    get_num_images():
        Obtiene el número de imágenes ingresado por el usuario.
    get_save_path(search_term):
        Obtiene la ruta donde se guardarán las imágenes o videos descargados.
    download_images(search_term, save_path, num_images):
        Descarga las imágenes basadas en el término de búsqueda y las guarda en la ruta especificada.
    download_video(video_url, save_path):
        Descarga el video desde la URL proporcionada y lo guarda en la ruta especificada.
    on_search():
        Maneja el evento de búsqueda cuando se hace clic en el botón de buscar y descargar.
    run():
        Inicia el bucle principal de la aplicación.
    """

    def __init__(self):
        
        """
        Inicializa la clase Buscador y configura la interfaz gráfica de usuario.
        """
        
        self.root = tk.Tk()
        self.root.title("Buscador de Imágenes y Videos de Gerard")
        self.root.geometry("800x600")
        self.var = tk.StringVar(value="videos")

        self.bg_image = tk.PhotoImage(file=r"F:\Phyton\Proyecto_personal_final\Info\Pretil_Nocturno.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(self.root, text="Busca Imágenes y Videos", font=("Helvetica", 20, "bold"), fg="blue")
        self.label.pack(pady=10)

        self.label_adicional = tk.Label(self.root, text="Ingrese palabra clave o URL del video", font=("Helvetica", 12, "bold"), fg="black")
        self.label_adicional.pack(pady=10)

        self.entry_search = tk.Text(self.root, width=50, height=2, wrap=tk.WORD)
        self.entry_search.pack(pady=10)

        self.options_frame = tk.Frame(self.root)
        self.options_frame.pack(pady=10)

        self.radio_images = tk.Radiobutton(self.options_frame, text="Imágenes", variable=self.var, value="images", font=("Helvetica", 12))
        self.radio_images.pack(side=tk.LEFT, padx=10)
        self.radio_videos = tk.Radiobutton(self.options_frame, text="Videos", variable=self.var, value="videos", font=("Helvetica", 12))
        self.radio_videos.pack(side=tk.LEFT, padx=10)

        self.label_num_images = tk.Label(self.root, text="Número de Imágenes con máximo de 25:", font=("Helvetica", 12, "bold"), fg="black")
        self.label_num_images.pack(pady=10)
        self.entry_num_images = tk.Entry(self.root)
        self.entry_num_images.pack(pady=10)

        self.search_button = tk.Button(self.root, text="Buscar y Descargar", font=("Helvetica", 16), width=20, height=2, command=self.on_search)
        self.search_button.pack(side=tk.BOTTOM, pady=20)

    def get_search_term(self):
        
        """
        Obtiene el término de búsqueda ingresado por el usuario.

        Returns:
        --------
        str
            El término de búsqueda ingresado por el usuario.
        """
        
        return self.entry_search.get("1.0", tk.END).strip()

    def get_num_images(self):
        
        """
        Obtiene el número de imágenes ingresado por el usuario.

        Returns:
        --------
        int
            El número de imágenes ingresado por el usuario. Retorna 0 si la entrada no es válida.
        """
        try:
            return int(self.entry_num_images.get())
        except ValueError:
            return 0

    def get_save_path(self, search_term):
        
        """
       Obtiene la ruta donde se guardarán las imágenes o videos descargados.

       Parameters:
       -----------
       search_term : str
           El término de búsqueda ingresado por el usuario.

       Returns:
       --------
       str
           La ruta donde se guardarán las imágenes o videos descargados.
       """
       
        if self.var.get() == "images":
            return os.path.join(r'F:\Phyton\Proyecto_personal_final\Res\Imágenes', search_term)
        elif self.var.get() == "videos":
            return os.path.join(r'F:\Phyton\Proyecto_personal_final\Res\Videos')

    def download_images(self, search_term, save_path, num_images):
        
        """
        Descarga imágenes basadas en el término de búsqueda y las guarda en la ruta especificada.

        Parameters:
        -----------
        search_term : str
            El término de búsqueda ingresado por el usuario.
        save_path : str
            La ruta donde se guardarán las imágenes descargadas.
        num_images : int
            El número de imágenes a descargar ingresado por ek usuario.
        """
        
        url = f"https://www.bing.com/images/search?q={search_term}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        os.makedirs(save_path, exist_ok=True)
        images = soup.find_all('img', {'class': 'mimg'})
        
        downloaded_count = 0
        idx = 0
            
        while downloaded_count < num_images and idx < len(images):
            img = images[idx]
            img_url = img.get('src') or img.get('data-src')
            
            if img_url:
                img_name = os.path.join(save_path, f'{downloaded_count+1}.jpg')
                
                try:
                    img_data = requests.get(img_url).content
                    with open(img_name, 'wb') as img_file:
                        img_file.write(img_data)
                    print(f'Descargada {img_name}')
                    downloaded_count += 1
                    
                except Exception as e:
                    print(f'No se pudo descargar {img_url}: {e}')
            
            idx += 1

    def download_video(self, video_url, save_path):
        
        """
        Descarga el video desde la URL especificada y lo guarda en la ruta especificada.

        Parameters:
        -----------
        video_url : str
            La URL del video a descargar.
        save_path : str
            La ruta donde se guardará el video descargado.
        """
        
        yt = YouTube(video_url)
        stream = yt.streams.filter(file_extension='mp4').first()
        stream.download(save_path)

        video_path = os.path.join(save_path, stream.default_filename)
        print(f"Video descargado: {video_path}")
        
    def on_search(self):
        
        """
        Ejecuta la lógica de búsqueda y descarga cuando el usuario presiona el botón de búsqueda.
        """
        search_term = self.get_search_term()
        if not search_term:
            messagebox.showerror("Error", "Por favor, ingrese un término de búsqueda o URL del video.")
            return

        if self.var.get() == "images":
            num_images = self.get_num_images()
            if num_images <= 0:
                messagebox.showerror("Error", "Por favor, ingrese un número de imágenes mayor a cero.")
                return
            save_path = self.get_save_path(search_term)
            try:
                self.download_images(search_term, save_path, num_images)
                messagebox.showinfo("Éxito", f"Se descargaron {num_images} imágenes en la carpeta '{save_path}'")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un error al descargar las imágenes: {e}")
                print(f"Error al descargar las imágenes: {e}")
        elif self.var.get() == "videos":
            video_url = search_term
            save_path = self.get_save_path(search_term)
            os.makedirs(save_path, exist_ok=True)
            try:
                self.download_video(video_url, save_path)
                messagebox.showinfo("Éxito", f"Video descargado en la carpeta '{save_path}'")
            except Exception as e:
                messagebox.showerror("Error", f"Hubo un error al descargar el video: {e}")
                print(f"Error al descargar el video: {e}")
                

    def run(self):
        
        """
        Inicia el bucle principal de la aplicación.
        """
        self.root.mainloop()

buscador = Buscador()
buscador.run()
