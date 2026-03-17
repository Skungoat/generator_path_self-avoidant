from Reseau import *
import tkinter as tk
import time

class App:
    def __init__(self, root, n=100):
        self.root = root
        self.root.title("Explorateur de Chemin")
        self.n = n
        self.reseau = Reseau(n)
        self.start_pos = (n // 2, n // 2)
        
        # État initial
        self.red_visible = True
        self.is_running = False
        self.init_logic()

        # --- Widgets ---
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.frame_ctrl = tk.Frame(root, bg="#f0f0f0", pady=10)
        self.frame_ctrl.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.btn_start = tk.Button(self.frame_ctrl, text="Lancer", command=self.lancer)
        self.btn_start.pack(side=tk.LEFT, padx=10)

        self.btn_reset = tk.Button(self.frame_ctrl, text="Relancer", command=self.reset_all)
        self.btn_reset.pack(side=tk.LEFT, padx=10)

        self.btn_toggle = tk.Button(self.frame_ctrl, text="Masquer/Afficher Rouges", command=self.toggle_red)
        self.btn_toggle.pack(side=tk.LEFT, padx=10)

    def init_logic(self):
        """Réinitialise les variables de suivi"""
        self.reseau.reset_tab()
        self.reseau.set_pos(0, *self.start_pos)
        self.historique = [self.start_pos]
        self.traits_ids = []

    def reset_all(self):
        """Nettoie tout pour recommencer"""
        self.is_running = False
        self.canvas.delete("all")
        self.init_logic()
        self.btn_start.config(state="normal", text="Lancer")

    def toggle_red(self):
        self.red_visible = not self.red_visible
        state = "normal" if self.red_visible else "hidden"
        self.canvas.itemconfigure("red_path", state=state)

    def get_step(self):
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        return min(w, h) // self.n

    def lancer(self):
        if not self.is_running:
            self.is_running = True
            self.btn_start.config(state="disabled")
            self.explorer()

    def explorer(self):
        if not self.is_running or not self.historique:
            return

        curr_i, curr_j = self.historique[-1]
        ni, nj, etat = self.reseau.move_smart(curr_i, curr_j, self.start_pos, len(self.traits_ids))
        s = self.get_step()

        if etat == "AVANCE":
            line_id = self.canvas.create_line(
                curr_j*s + s//2, curr_i*s + s//2,
                nj*s + s//2, ni*s + s//2,
                fill="blue", width=2, tags="blue_path"
            )
            self.traits_ids.append(line_id)
            self.historique.append((ni, nj))
        
        elif etat == "BOUCLE":
            self.canvas.create_line(
                curr_j*s + s//2, curr_i*s + s//2,
                nj*s + s//2, ni*s + s//2,
                fill="green", width=3, tags="blue_path" 
            )
            self.is_running = False
            self.btn_start.config(text="Bouclé !")
            return

        elif etat == "BLOQUÉ":
            if len(self.historique) > 1:
                last_line = self.traits_ids.pop()
                self.canvas.itemconfig(last_line, fill="red", width=1, tags="red_path")
                if not self.red_visible:
                    self.canvas.itemconfig(last_line, state="hidden")
                self.historique.pop()
            else:
                self.is_running = False
                self.btn_start.config(text="Impasse")
                return

        self.root.after(1, self.explorer)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x800")
    app = App(root, n=100)
    root.mainloop()