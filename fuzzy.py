import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# --- Fuzzy değişkenler ---
topa_sahiplik = ctrl.Antecedent(np.arange(0, 101, 1), 'topa_sahiplik')
atak_sayisi = ctrl.Antecedent(np.arange(0, 51, 1), 'atak_sayisi')
savunma_basari = ctrl.Antecedent(np.arange(0, 101, 1), 'savunma_basari')
orta_yuzdesi = ctrl.Antecedent(np.arange(0, 101, 1), 'orta_yuzdesi')
motivasyon = ctrl.Antecedent(np.arange(0, 11, 1), 'motivasyon')

mac_performans = ctrl.Consequent(np.arange(0, 101, 1), 'mac_performans')
beklenen_gol = ctrl.Consequent(np.arange(1, 11, 0.1), 'beklenen_gol')  # 1-10 arası

# Üyelik fonksiyonları - Türkçe isimlerle (Kötü, Orta, İyi)
for var in [topa_sahiplik, atak_sayisi, savunma_basari, orta_yuzdesi]:
    var['kotu'] = fuzz.trimf(var.universe, [var.universe[0], var.universe[0], var.universe[len(var.universe)//2]])
    var['orta'] = fuzz.trimf(var.universe, [var.universe[0], var.universe[len(var.universe)//2], var.universe[-1]])
    var['iyi'] = fuzz.trimf(var.universe, [var.universe[len(var.universe)//2], var.universe[-1], var.universe[-1]])

# Motivasyon özel - 0-10 arası, yine aynı şekilde
motivasyon['kotu'] = fuzz.trimf(motivasyon.universe, [0, 0, 5])
motivasyon['orta'] = fuzz.trimf(motivasyon.universe, [0, 5, 10])
motivasyon['iyi'] = fuzz.trimf(motivasyon.universe, [5, 10, 10])

# Çıktılar
mac_performans['dusuk'] = fuzz.trimf(mac_performans.universe, [0, 0, 50])
mac_performans['orta'] = fuzz.trimf(mac_performans.universe, [30, 50, 70])
mac_performans['yuksek'] = fuzz.trimf(mac_performans.universe, [50, 100, 100])

beklenen_gol['dusuk'] = fuzz.trimf(beklenen_gol.universe, [1, 1, 4])
beklenen_gol['orta'] = fuzz.trimf(beklenen_gol.universe, [1, 5, 8])
beklenen_gol['yuksek'] = fuzz.trimf(beklenen_gol.universe, [5, 10, 10])

# Kurallar (60 adet)
rules = [
    ctrl.Rule(topa_sahiplik['iyi'] & atak_sayisi['iyi'] & motivasyon['iyi'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['orta'] & atak_sayisi['iyi'], mac_performans['orta']),
    ctrl.Rule(savunma_basari['orta'] | orta_yuzdesi['orta'], mac_performans['orta']),
    ctrl.Rule(motivasyon['kotu'] | savunma_basari['kotu'], mac_performans['dusuk']),
    ctrl.Rule(topa_sahiplik['kotu'] & atak_sayisi['kotu'], mac_performans['dusuk']),
    ctrl.Rule(orta_yuzdesi['iyi'] & motivasyon['iyi'], mac_performans['yuksek']),
    ctrl.Rule(savunma_basari['iyi'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(savunma_basari['iyi'] & atak_sayisi['iyi'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['orta'] & savunma_basari['orta'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['kotu'] & motivasyon['kotu'], mac_performans['dusuk']),
    
    ctrl.Rule(motivasyon['iyi'] & savunma_basari['kotu'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['kotu'] & motivasyon['iyi'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['iyi'] & savunma_basari['iyi'], mac_performans['yuksek']),
    ctrl.Rule(atak_sayisi['kotu'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(savunma_basari['orta'] & orta_yuzdesi['iyi'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['iyi'] & savunma_basari['iyi'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['iyi'] & orta_yuzdesi['iyi'], mac_performans['yuksek']),
    ctrl.Rule(atak_sayisi['orta'] & savunma_basari['orta'], mac_performans['orta']),
    ctrl.Rule(atak_sayisi['iyi'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['kotu'] & savunma_basari['kotu'], mac_performans['dusuk']),

    ctrl.Rule(mac_performans['yuksek'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['orta'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['dusuk'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['yuksek'] & motivasyon['iyi'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['orta'] & motivasyon['orta'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['dusuk'] & motivasyon['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['orta'] & savunma_basari['iyi'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['yuksek'] & atak_sayisi['iyi'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['dusuk'] & atak_sayisi['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['orta'] & topa_sahiplik['iyi'], beklenen_gol['orta']),

    ctrl.Rule(mac_performans['yuksek'] & orta_yuzdesi['iyi'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['dusuk'] & orta_yuzdesi['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['orta'] & orta_yuzdesi['orta'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['yuksek'] & savunma_basari['iyi'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['yuksek'] & topa_sahiplik['iyi'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['orta'] & atak_sayisi['orta'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['dusuk'] & topa_sahiplik['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['dusuk'] & savunma_basari['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['orta'] & motivasyon['iyi'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['yuksek'] & motivasyon['orta'], beklenen_gol['yuksek']),

    ctrl.Rule(topa_sahiplik['iyi'] & motivasyon['orta'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['orta'] & motivasyon['kotu'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['kotu'] & motivasyon['orta'], mac_performans['dusuk']),
    ctrl.Rule(orta_yuzdesi['orta'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(savunma_basari['iyi'] & orta_yuzdesi['orta'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['kotu'] & savunma_basari['orta'], mac_performans['dusuk']),
    ctrl.Rule(atak_sayisi['kotu'] & savunma_basari['iyi'], mac_performans['orta']),
    ctrl.Rule(atak_sayisi['orta'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(atak_sayisi['iyi'] & savunma_basari['kotu'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['iyi'] & savunma_basari['orta'], mac_performans['yuksek']),

    ctrl.Rule(mac_performans['yuksek'] & orta_yuzdesi['orta'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['orta'] & savunma_basari['orta'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['dusuk'] & motivasyon['orta'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['orta'] & orta_yuzdesi['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['yuksek'] & atak_sayisi['orta'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['dusuk'] & orta_yuzdesi['orta'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['orta'] & motivasyon['kotu'], beklenen_gol['dusuk']),
    ctrl.Rule(mac_performans['yuksek'] & savunma_basari['orta'], beklenen_gol['yuksek']),
    ctrl.Rule(mac_performans['orta'] & topa_sahiplik['orta'], beklenen_gol['orta']),
    ctrl.Rule(mac_performans['dusuk'] & topa_sahiplik['orta'], beklenen_gol['dusuk']),
    ctrl.Rule(topa_sahiplik['iyi'] & atak_sayisi['orta'] & savunma_basari['orta'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['orta'] & atak_sayisi['orta'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['kotu'] & savunma_basari['iyi'] & motivasyon['iyi'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['iyi'] & atak_sayisi['kotu'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(savunma_basari['kotu'] & atak_sayisi['orta'] & motivasyon['iyi'], mac_performans['orta']),
    
    ctrl.Rule(topa_sahiplik['iyi'] & orta_yuzdesi['kotu'] & motivasyon['iyi'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['orta'] & savunma_basari['iyi'] & atak_sayisi['iyi'], mac_performans['yuksek']),
    ctrl.Rule(atak_sayisi['orta'] & orta_yuzdesi['orta'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(savunma_basari['orta'] & motivasyon['kotu'] & atak_sayisi['kotu'], mac_performans['dusuk']),
    ctrl.Rule(topa_sahiplik['kotu'] & orta_yuzdesi['orta'] & savunma_basari['orta'], mac_performans['dusuk']),
    
    ctrl.Rule(topa_sahiplik['iyi'] & motivasyon['kotu'] & atak_sayisi['iyi'], mac_performans['orta']),
    ctrl.Rule(savunma_basari['iyi'] & motivasyon['iyi'] & orta_yuzdesi['orta'], mac_performans['yuksek']),
    ctrl.Rule(atak_sayisi['kotu'] & motivasyon['orta'] & savunma_basari['orta'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['orta'] & atak_sayisi['kotu'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(orta_yuzdesi['iyi'] & savunma_basari['kotu'] & motivasyon['orta'], mac_performans['orta']),
    
    ctrl.Rule(topa_sahiplik['kotu'] & atak_sayisi['iyi'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['orta'] & motivasyon['iyi'] & savunma_basari['iyi'], mac_performans['yuksek']),
    ctrl.Rule(atak_sayisi['orta'] & savunma_basari['kotu'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(topa_sahiplik['iyi'] & savunma_basari['orta'] & motivasyon['orta'], mac_performans['yuksek']),
    ctrl.Rule(orta_yuzdesi['kotu'] & atak_sayisi['orta'] & motivasyon['iyi'], mac_performans['orta']),
    
    ctrl.Rule(motivasyon['orta'] & savunma_basari['iyi'] & atak_sayisi['orta'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['kotu'] & orta_yuzdesi['iyi'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(topa_sahiplik['iyi'] & atak_sayisi['iyi'] & motivasyon['kotu'], mac_performans['orta']),
    ctrl.Rule(savunma_basari['orta'] & orta_yuzdesi['orta'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(atak_sayisi['iyi'] & motivasyon['iyi'] & savunma_basari['iyi'], mac_performans['yuksek']),
    
    ctrl.Rule(topa_sahiplik['orta'] & atak_sayisi['orta'] & savunma_basari['kotu'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['iyi'] & motivasyon['orta'] & atak_sayisi['orta'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['kotu'] & motivasyon['kotu'] & savunma_basari['kotu'], mac_performans['dusuk']),
    ctrl.Rule(atak_sayisi['orta'] & orta_yuzdesi['kotu'] & savunma_basari['orta'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['iyi'] & atak_sayisi['orta'] & motivasyon['orta'], mac_performans['yuksek']),
    
    ctrl.Rule(savunma_basari['iyi'] & orta_yuzdesi['iyi'] & motivasyon['iyi'], mac_performans['yuksek']),
    ctrl.Rule(topa_sahiplik['orta'] & motivasyon['orta'] & savunma_basari['orta'], mac_performans['orta']),
    ctrl.Rule(orta_yuzdesi['kotu'] & atak_sayisi['kotu'] & motivasyon['kotu'], mac_performans['dusuk']),
    ctrl.Rule(topa_sahiplik['iyi'] & savunma_basari['kotu'] & motivasyon['orta'], mac_performans['orta']),
    ctrl.Rule(atak_sayisi['orta'] & motivasyon['iyi'] & savunma_basari['orta'], mac_performans['orta']),
    
    ctrl.Rule(orta_yuzdesi['orta'] & savunma_basari['orta'] & motivasyon['kotu'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['kotu'] & atak_sayisi['orta'] & motivasyon['iyi'], mac_performans['orta']),
    ctrl.Rule(atak_sayisi['iyi'] & orta_yuzdesi['iyi'] & motivasyon['orta'], mac_performans['yuksek']),
    ctrl.Rule(savunma_basari['orta'] & motivasyon['orta'] & atak_sayisi['iyi'], mac_performans['orta']),
    ctrl.Rule(topa_sahiplik['orta'] & savunma_basari['iyi'] & motivasyon['kotu'], mac_performans['orta']),
]

# Kontrol sistemi
futbol_ctrl = ctrl.ControlSystem(rules)
futbol_sim = ctrl.ControlSystemSimulation(futbol_ctrl)


# --- Tkinter arayüz ---
app = tk.Tk()
app.title("Futbol Takımı Performans Tahmini")
app.state('zoomed')
app.configure(bg="#004d00")

entries = {}
input_vars = [
    ("Topa Sahiplik (%)", "topa_sahiplik"),
    ("Atak Sayısı", "atak_sayisi"),
    ("Savunma Başarı (%)", "savunma_basari"),
    ("Orta Yüzdesi (%)", "orta_yuzdesi"),
    ("Motivasyon (1-10)", "motivasyon"),
]

def create_label_entry(row, text, var_name):
    lbl = tk.Label(app, text=text, fg="#e6ffe6", bg="#004d00", font=("Segoe UI", 12, "bold"), anchor="e")
    lbl.grid(row=row, column=0, sticky="e", padx=(15,8), pady=8)
    ent = tk.Entry(app, font=("Segoe UI", 12), width=12, bd=2, relief="groove")
    ent.grid(row=row, column=1, sticky="w", padx=(8,15), pady=8)
    entries[var_name] = ent
    # Değer yazıldıkça girdi grafiği güncellensin
    ent.bind("<KeyRelease>", lambda event, vn=var_name: update_input_marker(vn))

for i, (label, var) in enumerate(input_vars):
    create_label_entry(i, label, var)

label_sonuc_mac = tk.Label(app, text="", fg="#ffcc00", bg="#004d00", font=("Segoe UI", 16, "bold"))
label_sonuc_mac.grid(row=6, column=0, columnspan=2, pady=15)
label_sonuc_gol = tk.Label(app, text="", fg="#ffcc00", bg="#004d00", font=("Segoe UI", 16, "bold"))
label_sonuc_gol.grid(row=7, column=0, columnspan=2, pady=15)

btn_hesapla = tk.Button(app, text="Hesapla", bg="#339933", fg="white", font=("Segoe UI", 14, "bold"),
                        activebackground="#267326", relief="raised", bd=3, command=lambda: hesapla())
btn_hesapla.grid(row=8, column=0, columnspan=2, sticky="ew", padx=20, pady=15)

# Notebook ile 2 sayfa oluşturuyoruz
notebook = ttk.Notebook(app)
notebook.grid(row=0, column=2, rowspan=10, sticky="nsew", padx=15, pady=15)

# 1. sayfa: Girdi Grafikleri
frame_girdi = ttk.Frame(notebook)
notebook.add(frame_girdi, text="Girdi Grafikleri")

# 2. sayfa: Çıktı Grafikleri
frame_cikti = ttk.Frame(notebook)
notebook.add(frame_cikti, text="Çıktı Grafikleri")

# Figürler ve Canvaslar
fig_girdi = plt.Figure(figsize=(10, 6), dpi=110, facecolor="#f0f5f0")
canvas_girdi = FigureCanvasTkAgg(fig_girdi, master=frame_girdi)
canvas_girdi.get_tk_widget().pack(fill=tk.BOTH, expand=True)

fig_cikti = plt.Figure(figsize=(10, 6), dpi=110, facecolor="#f0f5f0")
canvas_cikti = FigureCanvasTkAgg(fig_cikti, master=frame_cikti)
canvas_cikti.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Kırmızı çizgiler için saklama
input_marker_lines = {}

def plot_girdi_grafikleri():
    fig_girdi.clf()
    inputs = [topa_sahiplik, atak_sayisi, savunma_basari, orta_yuzdesi, motivasyon]
    titles = ['Topa Sahiplik (%)', 'Atak Sayısı', 'Savunma Başarı (%)', 'Orta Yüzdesi (%)', 'Motivasyon (1-10)']
    rows, cols = 3, 2
    for i in range(len(inputs)):
        ax = fig_girdi.add_subplot(rows, cols, i+1)
        ax.set_facecolor("#f9fff9")
        for term in inputs[i].terms:
            ax.plot(inputs[i].universe, inputs[i][term].mf, label=term.capitalize())
        ax.set_title(titles[i], fontsize=10)
        ax.legend(fontsize=7)
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)
        input_marker_lines[inputs[i].label] = None
    for i in range(len(inputs)+1, rows*cols+1):
        fig_girdi.add_subplot(rows, cols, i).axis('off')

    fig_girdi.suptitle("Girdi Grafikler", fontsize=16, fontweight='bold', color='#004d00')
    fig_girdi.tight_layout(rect=[0, 0, 1, 0.95])
    canvas_girdi.draw()

def membership_value(universe, mf_array, val):
    return np.interp(val, universe, mf_array)

def plot_cikti_grafikleri():
    fig_cikti.clf()
    ax1 = fig_cikti.add_subplot(1, 2, 1)
    ax2 = fig_cikti.add_subplot(1, 2, 2)

    ax1.set_facecolor("#f9fff9")
    ax2.set_facecolor("#f9fff9")

    # Maç Performans üyelik fonksiyonları
    for term in mac_performans.terms:
        y = mac_performans[term].mf
        ax1.plot(mac_performans.universe, y, label=term.capitalize())
    mac_val = futbol_sim.output['mac_performans']
    mf_vals = [membership_value(mac_performans.universe, mac_performans[term].mf, mac_val) for term in mac_performans.terms]
    ax1.vlines(mac_val, 0, max(mf_vals), colors='red', linestyles='--', linewidth=2, label='Tahmin')
    ax1.set_title("Maç Performans")
    ax1.set_xlabel("Değer")
    ax1.set_ylabel("Üyelik Derecesi")
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.7)

    # Beklenen Gol üyelik fonksiyonları
    for term in beklenen_gol.terms:
        y = beklenen_gol[term].mf
        ax2.plot(beklenen_gol.universe, y, label=term.capitalize())
    gol_val = futbol_sim.output['beklenen_gol']
    mf_vals_gol = [membership_value(beklenen_gol.universe, beklenen_gol[term].mf, gol_val) for term in beklenen_gol.terms]
    ax2.vlines(gol_val, 0, max(mf_vals_gol), colors='red', linestyles='--', linewidth=2, label='Tahmin')
    ax2.set_title("Beklenen Gol Sayısı")
    ax2.set_xlabel("Değer")
    ax2.set_ylabel("Üyelik Derecesi")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    fig_cikti.suptitle("Çıktı Grafikler", fontsize=16, fontweight='bold', color='#004d00')
    fig_cikti.tight_layout(rect=[0, 0, 1, 0.95])
    canvas_cikti.draw()

def update_input_marker(var_name):
    try:
        val = float(entries[var_name].get())
    except ValueError:
        val = None

    inputs = [topa_sahiplik, atak_sayisi, savunma_basari, orta_yuzdesi, motivasyon]
    ax_idx = None
    for i, inp in enumerate(inputs):
        if inp.label == var_name:
            ax_idx = i
            break
    if ax_idx is None:
        return

    ax = fig_girdi.axes[ax_idx]

    # Var olan çizgiyi kaldır
    if input_marker_lines.get(var_name) is not None:
        try:
            input_marker_lines[var_name].remove()
        except:
            pass

    # Yeni kırmızı çizgi (yalnızca değer uygunsa çiz)
    if val is not None and ax.get_xlim()[0] <= val <= ax.get_xlim()[1]:
        input_marker_lines[var_name] = ax.axvline(val, color='r', linestyle='--', linewidth=2)
    else:
        input_marker_lines[var_name] = None

    canvas_girdi.draw()

def hesapla():
    try:
        for var_name in entries:
            val = float(entries[var_name].get())
            if var_name == 'motivasyon' and not (1 <= val <= 10):
                messagebox.showerror("Hata", "Motivasyon değeri 1 ile 10 arasında olmalı!")
                return
            futbol_sim.input[var_name] = val
    except ValueError:
        messagebox.showerror("Hata", "Lütfen tüm girişleri doğru biçimde girin!")
        return

    futbol_sim.compute()

    label_sonuc_mac.config(text=f"Maç Performans Tahmini: {futbol_sim.output['mac_performans']:.2f}")
    label_sonuc_gol.config(text=f"Beklenen Gol Sayısı: {futbol_sim.output['beklenen_gol']:.2f}")

    plot_cikti_grafikleri()
    notebook.select(frame_cikti)

# Başlangıçta sadece girdi grafiklerini çiz
plot_girdi_grafikleri()

app.mainloop()