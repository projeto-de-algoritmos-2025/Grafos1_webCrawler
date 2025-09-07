import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def botao_clicado():
    messagebox.showinfo("Aviso", "Ola")

janela = tk.Tk()
janela.title("WebCrawler")
janela.geometry("400x400")

botao = tk.Button(janela, text="Clique aqui", command=botao_clicado)
botao.pack(pady=10)

imagem = Image.open("site_map.png")
foto = ImageTk.PhotoImage(imagem)
label_imagem = tk.Label(janela, image=foto)
label_imagem.pack(pady=10)

janela.mainloop()

