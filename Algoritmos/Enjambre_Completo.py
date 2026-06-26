"""
Simulación de control de enjambre — matriz N×M de drones
Modos de control:
  [A] Centralizado  : centroide único, offsets rígidos, yaw global
  [B] Distribuido   : cada dron tiene su propio yaw; la formación puede deformarse

Controles:
  T           → Despegue
  R           → Aterrizaje
  UP / DOWN   → Adelante / Atrás
  A / D       → Izquierda / Derecha
  LEFT/RIGHT  → Yaw −/+
  ESPACIO     → Subir (eje Z)
  SHIFT       → Bajar (eje Z)
  ESC         → Salir

Dependencias:
  pip install matplotlib keyboard numpy
"""

import math, time, threading
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
from matplotlib.animation import FuncAnimation

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("[AVISO] 'keyboard' no instalado — modo demo activo.\n")


# ──────────────────────────────────────────────
#  PARÁMETROS FÍSICOS
# ──────────────────────────────────────────────
DT            = 1 / 30
V_XY          = 1.5
V_Z           = 0.8
YAW_RATE      = math.radians(60)
TAKEOFF_ALT   = 2.0
TAKEOFF_SPEED = 0.5


def build_formation_offsets(rows, cols, dx, dy):
    """Rejilla rows×cols centrada en el origen."""
    offsets = []
    x_start = -((cols - 1) / 2.0) * dx
    y_start  =  ((rows - 1) / 2.0) * dy
    for r in range(rows):
        for c in range(cols):
            offsets.append([x_start + c*dx, y_start - r*dy, 0.0])
    return np.array(offsets, dtype=float)


# ──────────────────────────────────────────────
#  ESTILOS TKINTER
# ──────────────────────────────────────────────
BG, FG, ACC, BG2 = "#1a1a2e", "#e0e0e0", "#5DCAA5", "#252545"
FONT_MONO  = ("Consolas", 10)
FONT_TITLE = ("Consolas", 12, "bold")
FONT_SUB   = ("Consolas", 9)
ROW_COLORS = ['#5DCAA5','#7F77DD','#EF9F27','#D85A30',
              '#378ADD','#993556','#888780','#9FE1CB','#F7C59F','#B5EAD7']

def mk_label(parent, text, title=False, sub=False, **kw):
    color = ACC if title else ("#888780" if sub else FG)
    font  = FONT_TITLE if title else (FONT_SUB if sub else FONT_MONO)
    return tk.Label(parent, text=text, bg=BG, fg=color, font=font, **kw)

def mk_entry(parent, default, width=8):
    var = tk.StringVar(value=str(default))
    e = tk.Entry(parent, textvariable=var, width=width,
                 bg=BG2, fg=FG, insertbackground=FG, relief="flat",
                 font=FONT_MONO, highlightthickness=1,
                 highlightcolor=ACC, highlightbackground="#333355")
    return var, e

def mk_spin(parent, from_, to, var, width=6):
    return tk.Spinbox(parent, from_=from_, to=to, textvariable=var,
                      width=width, bg=BG2, fg=FG, buttonbackground=BG2,
                      insertbackground=FG, relief="flat", font=FONT_MONO,
                      highlightthickness=1, highlightcolor=ACC,
                      highlightbackground="#333355")


# ──────────────────────────────────────────────
#  DIÁLOGO DE CONFIGURACIÓN
# ──────────────────────────────────────────────
CONTROL_MODES = [
    "Centralizado  — yaw global, formación rígida",
    "Distribuido   — yaw individual, formación deformable",
]

class ConfigDialog:
    def __init__(self):
        self.result = None
        self.root = tk.Tk()
        self.root.title("Configuración del enjambre")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._build_ui()
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _sep(self):
        tk.Frame(self.root, bg="#2a2a4a", height=1).pack(fill="x", padx=20, pady=6)

    def _row(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill="x", padx=24, pady=3)
        return f

    def _build_ui(self):
        root = self.root

        mk_label(root, "🚁  Control de enjambre", title=True).pack(pady=(18,2))
        mk_label(root, "Configura la simulación antes de comenzar", sub=True).pack(pady=(0,10))
        self._sep()

        # ── Modo de control ──
        mk_label(root, "Modo de control", title=True).pack(anchor="w", padx=24, pady=(8,0))
        mk_label(root, "Selecciona el algoritmo de control del enjambre", sub=True).pack(anchor="w", padx=24)

        f = self._row()
        mk_label(f, "Algoritmo:").pack(side="left")
        self._mode_var = tk.StringVar(value=CONTROL_MODES[0])
        self._mode_menu = tk.OptionMenu(f, self._mode_var, *CONTROL_MODES)
        self._mode_menu.config(bg=BG2, fg=FG, activebackground=ACC,
                               activeforeground=BG, relief="flat",
                               font=FONT_MONO, highlightthickness=0,
                               indicatoron=True, bd=0)
        self._mode_menu["menu"].config(bg=BG2, fg=FG, font=FONT_MONO,
                                       activebackground=ACC, activeforeground=BG)
        self._mode_menu.pack(side="left", padx=(8,0))

        # Descripción dinámica del modo
        self._mode_desc = mk_label(root, "", sub=True, wraplength=320, justify="left")
        self._mode_desc.pack(anchor="w", padx=24, pady=(2,0))
        self._mode_var.trace_add("write", lambda *_: self._update_mode_desc())
        self._update_mode_desc()

        self._sep()

        # ── Posición inicial del centroide ──
        mk_label(root, "Posición inicial del centroide (m)", title=True).pack(anchor="w", padx=24, pady=(8,0))
        mk_label(root, "Punto de referencia central del enjambre", sub=True).pack(anchor="w", padx=24)
        for lbl, attr, default in [("X (m)","_cx",0.0),("Y (m)","_cy",0.0),("Z (m, ≥ 0)","_cz",0.0)]:
            f = self._row()
            mk_label(f, f"{lbl}:").pack(side="left")
            var, entry = mk_entry(f, default)
            entry.pack(side="left", padx=(8,0))
            setattr(self, attr, var)

        self._sep()

        # ── Matriz de drones ──
        mk_label(root, "Formación en matriz", title=True).pack(anchor="w", padx=24, pady=(8,0))
        mk_label(root, "Número de filas y columnas de la rejilla", sub=True).pack(anchor="w", padx=24)
        self._rows = tk.IntVar(value=2)
        self._cols = tk.IntVar(value=3)
        for lbl, var in [("Filas:", self._rows), ("Columnas:", self._cols)]:
            f = self._row()
            mk_label(f, lbl).pack(side="left")
            mk_spin(f, 1, 20, var).pack(side="left", padx=(8,0))

        self._sep()

        # ── Offset entre drones ──
        mk_label(root, "Separación entre drones (m)", title=True).pack(anchor="w", padx=24, pady=(8,0))
        mk_label(root, "Distancia entre drones adyacentes", sub=True).pack(anchor="w", padx=24)
        for lbl, attr, default in [("Offset X (columnas):","_dx",2.0),("Offset Y (filas):","_dy",2.0)]:
            f = self._row()
            mk_label(f, lbl).pack(side="left")
            var, entry = mk_entry(f, default)
            entry.pack(side="left", padx=(8,0))
            setattr(self, attr, var)

        self._sep()

        # ── Preview ──
        mk_label(root, "Vista previa de la formación", sub=True).pack(pady=(2,4))
        self._canvas = tk.Canvas(root, width=260, height=120,
                                 bg="#12122a", highlightthickness=0)
        self._canvas.pack(pady=4)
        for v in (self._rows, self._cols):
            v.trace_add("write", lambda *_: self._draw_preview())
        self._draw_preview()

        # ── Botón ──
        tk.Button(root, text="▶  Iniciar simulación",
                  bg=ACC, fg=BG, font=("Consolas",10,"bold"),
                  relief="flat", padx=12, pady=6,
                  activebackground="#3eaa85", cursor="hand2",
                  command=self._confirm).pack(pady=(8,20))

    def _update_mode_desc(self):
        idx = CONTROL_MODES.index(self._mode_var.get())
        descs = [
            "Un centroide controla todo el enjambre. La formación es rígida:\ncada dron mantiene su offset y todos giran con el mismo yaw.",
            "Cada dron tiene su propio yaw independiente.\n←/→ rota cada dron sobre sí mismo. ↑ mueve cada dron\nen la dirección que él apunta → la formación puede deformarse.",
        ]
        self._mode_desc.config(text=descs[idx])

    def _draw_preview(self):
        c = self._canvas
        c.delete("all")
        try:
            rows, cols = max(1,int(self._rows.get())), max(1,int(self._cols.get()))
        except Exception:
            return
        rows, cols = min(rows,10), min(cols,10)
        margin = 16
        cw, ch = 260-2*margin, 120-2*margin
        cw_cell, ch_cell = cw/max(cols,1), ch/max(rows,1)
        r_dot = max(4, min(cw_cell, ch_cell)*0.32, 1)
        r_dot = min(r_dot, 14)
        for r in range(rows):
            for ci in range(cols):
                idx = r*cols+ci
                x = margin+(ci+0.5)*cw_cell
                y = margin+(r +0.5)*ch_cell
                col = ROW_COLORS[r % len(ROW_COLORS)]
                c.create_oval(x-r_dot,y-r_dot,x+r_dot,y+r_dot, fill=col, outline="")
                if r_dot >= 7:
                    c.create_text(x, y, text=f"D{idx+1}",
                                  fill="white", font=("Consolas",int(r_dot*0.7)))
        n = rows*cols
        c.create_text(130,110, text=f"{rows}×{cols} = {n} drones",
                      fill="#888780", font=FONT_SUB)

    def _confirm(self):
        try:
            cx = float(self._cx.get())
            cy = float(self._cy.get())
            cz = float(self._cz.get())
            if cz < 0: raise ValueError("Z no puede ser negativa")
            rows = int(self._rows.get())
            cols = int(self._cols.get())
            if rows < 1 or cols < 1: raise ValueError("Filas y columnas deben ser ≥ 1")
            dx = float(self._dx.get())
            dy = float(self._dy.get())
            if dx <= 0 or dy <= 0: raise ValueError("Los offsets deben ser > 0")
        except ValueError as e:
            messagebox.showerror("Error de configuración", str(e), parent=self.root)
            return
        mode_idx = CONTROL_MODES.index(self._mode_var.get())
        self.result = dict(cx=cx, cy=cy, cz=cz, rows=rows, cols=cols,
                           dx=dx, dy=dy, mode=mode_idx)
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.result


# ──────────────────────────────────────────────
#  MODO 0 — CONTROL CENTRALIZADO
# ──────────────────────────────────────────────
class SwarmCentralized:
    """Centroide único + offsets rígidos rotados por un yaw global."""
    LANDED='LANDED'; TAKING_OFF='TAKING OFF'; FLYING='FLYING'; LANDING='LANDING'

    def __init__(self, cx0, cy0, cz0, formation_offsets):
        self.cx, self.cy, self.cz = cx0, cy0, cz0
        self.yaw = 0.0
        self.status = self.LANDED
        self.formation_offsets = formation_offsets
        self.n = len(formation_offsets)
        self.positions = formation_offsets.copy()
        self.positions[:,0] += cx0
        self.positions[:,1] += cy0
        self.positions[:,2]  = cz0
        self.yaws = np.zeros(self.n)   # todos igual al yaw global (solo informativo)
        self.trail = [(cx0,cy0,cz0)]
        self._lock = threading.Lock()

    def _rot(self, off, yaw):
        c,s = math.cos(yaw), math.sin(yaw)
        return c*off[0]-s*off[1], s*off[0]+c*off[1], off[2]

    def update(self, keys):
        with self._lock:
            if self.status == self.LANDED:
                if keys.get('takeoff'): self.status = self.TAKING_OFF

            elif self.status == self.TAKING_OFF:
                self.cz += TAKEOFF_SPEED*DT
                if self.cz >= TAKEOFF_ALT:
                    self.cz = TAKEOFF_ALT; self.status = self.FLYING

            elif self.status == self.FLYING:
                if keys.get('land'):
                    self.status = self.LANDING
                else:
                    if keys.get('yaw_left'):  self.yaw += YAW_RATE*DT
                    if keys.get('yaw_right'): self.yaw -= YAW_RATE*DT
                    c,s = math.cos(self.yaw), math.sin(self.yaw)
                    vx = (keys.get('fwd',0)-keys.get('bwd',0))*V_XY
                    vy = (keys.get('left',0)-keys.get('right',0))*V_XY
                    vz = (keys.get('up',0)-keys.get('down',0))*V_Z
                    self.cx += (c*vx - s*vy)*DT
                    self.cy += (s*vx + c*vy)*DT
                    self.cz  = max(0.1, self.cz + vz*DT)

            elif self.status == self.LANDING:
                self.cz -= TAKEOFF_SPEED*DT
                if self.cz <= 0.0:
                    self.cz = 0.0; self.status = self.LANDED

            self.yaws[:] = self.yaw
            for i, off in enumerate(self.formation_offsets):
                rx,ry,rz = self._rot(off, self.yaw)
                self.positions[i] = [self.cx+rx, self.cy+ry, self.cz+rz]

            if math.dist(self.trail[-1],(self.cx,self.cy,self.cz)) > 0.05:
                self.trail.append((self.cx,self.cy,self.cz))
                if len(self.trail) > 300: self.trail.pop(0)

    # Propiedades comunes para el visualizador
    @property
    def centroid(self): return self.cx, self.cy, self.cz
    @property
    def status_str(self): return self.status
    @property
    def mode_str(self): return "CENTRALIZADO"


# ──────────────────────────────────────────────
#  MODO 1 — CONTROL DISTRIBUIDO
# ──────────────────────────────────────────────
class SwarmDistributed:
    """
    Cada dron tiene su propio yaw.
    ←/→  → todos giran sobre sí mismos (no el bloque)
    ↑/↓  → cada uno avanza según su propio yaw → formación se deforma
    ↑Z/↓Z→ igual que centralizado (movimiento Z compartido)
    El centroide es la media de posiciones (informativo).
    """
    LANDED='LANDED'; TAKING_OFF='TAKING OFF'; FLYING='FLYING'; LANDING='LANDING'

    def __init__(self, cx0, cy0, cz0, formation_offsets):
        self.n = len(formation_offsets)
        self.status = self.LANDED
        self.formation_offsets = formation_offsets

        # Posición y yaw individual por dron
        self.positions = formation_offsets.copy()
        self.positions[:,0] += cx0
        self.positions[:,1] += cy0
        self.positions[:,2]  = cz0
        self.yaws = np.zeros(self.n)   # cada dron empieza apuntando a 0°

        # Altura compartida (el enjambre sube/baja junto)
        self._alt = cz0

        self._cx0, self._cy0 = cx0, cy0
        self.trail = [(cx0, cy0, cz0)]
        self._lock = threading.Lock()

    def update(self, keys):
        with self._lock:
            if self.status == self.LANDED:
                if keys.get('takeoff'): self.status = self.TAKING_OFF

            elif self.status == self.TAKING_OFF:
                self._alt += TAKEOFF_SPEED*DT
                if self._alt >= TAKEOFF_ALT:
                    self._alt = TAKEOFF_ALT; self.status = self.FLYING

            elif self.status == self.FLYING:
                if keys.get('land'):
                    self.status = self.LANDING
                else:
                    # Yaw individual: cada dron gira sobre sí mismo
                    if keys.get('yaw_left'):
                        self.yaws += YAW_RATE*DT
                    if keys.get('yaw_right'):
                        self.yaws -= YAW_RATE*DT

                    # Traslación: cada dron en la dirección de su propio yaw
                    vfwd  = (keys.get('fwd',0)  - keys.get('bwd',0))   * V_XY
                    vlat  = (keys.get('left',0)  - keys.get('right',0)) * V_XY
                    vz    = (keys.get('up',0)    - keys.get('down',0))  * V_Z

                    for i in range(self.n):
                        c, s = math.cos(self.yaws[i]), math.sin(self.yaws[i])
                        self.positions[i,0] += (c*vfwd - s*vlat)*DT
                        self.positions[i,1] += (s*vfwd + c*vlat)*DT

                    # Altura compartida (Z)
                    self._alt = max(0.1, self._alt + vz*DT)

            elif self.status == self.LANDING:
                self._alt -= TAKEOFF_SPEED*DT
                if self._alt <= 0.0:
                    self._alt = 0.0; self.status = self.LANDED

            # Actualizar Z de todos
            self.positions[:,2] = self._alt

            # Trail del centroide (media de posiciones)
            cx, cy, cz = self.centroid
            if math.dist(self.trail[-1],(cx,cy,cz)) > 0.05:
                self.trail.append((cx,cy,cz))
                if len(self.trail) > 300: self.trail.pop(0)

    @property
    def centroid(self):
        return (float(self.positions[:,0].mean()),
                float(self.positions[:,1].mean()),
                float(self.positions[:,2].mean()))
    @property
    def status_str(self): return self.status
    @property
    def mode_str(self): return "DISTRIBUIDO"


# ──────────────────────────────────────────────
#  LECTURA DE TECLADO
# ──────────────────────────────────────────────
def read_keys():
    if not KEYBOARD_AVAILABLE:
        t = time.time()
        return {'takeoff':(int(t)%20==1),'land':False,
                'fwd':int(3<t%20<8),'bwd':0,
                'left':int(8<t%20<12),'right':0,
                'yaw_left':int(12<t%20<16),'yaw_right':0,
                'up':int(t%20<3),'down':0}
    return {
        'takeoff':   keyboard.is_pressed('t'),
        'land':      keyboard.is_pressed('r'),
        'fwd':       keyboard.is_pressed('up'),
        'bwd':       keyboard.is_pressed('down'),
        'left':      keyboard.is_pressed('a'),
        'right':     keyboard.is_pressed('d'),
        'yaw_left':  keyboard.is_pressed('left'),
        'yaw_right': keyboard.is_pressed('right'),
        'up':        keyboard.is_pressed('space'),
        'down':      keyboard.is_pressed('shift'),
    }


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":

    cfg = ConfigDialog().run()
    if cfg is None:
        print("Cancelado."); exit(0)

    rows, cols = cfg["rows"], cfg["cols"]
    formation_offsets = build_formation_offsets(rows, cols, cfg["dx"], cfg["dy"])
    N = rows * cols

    drone_colors = []
    for r in range(rows):
        drone_colors.extend([ROW_COLORS[r % len(ROW_COLORS)]] * cols)

    # Instanciar el modelo según el modo elegido
    if cfg["mode"] == 0:
        swarm = SwarmCentralized(cfg["cx"], cfg["cy"], cfg["cz"], formation_offsets)
    else:
        swarm = SwarmDistributed(cfg["cx"], cfg["cy"], cfg["cz"], formation_offsets)

    _running = True

    def control_loop():
        while _running:
            t0 = time.perf_counter()
            swarm.update(read_keys())
            elapsed = time.perf_counter() - t0
            time.sleep(max(0.0, DT - elapsed))

    threading.Thread(target=control_loop, daemon=True).start()

    # ── Figura ──
    fig = plt.figure(figsize=(11, 7), facecolor='#1a1a2e')
    ax  = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#1a1a2e')
    fig.subplots_adjust(left=0, right=1, bottom=0.02, top=0.96)

    cx0, cy0 = cfg["cx"], cfg["cy"]
    span  = max(cols*cfg["dx"], rows*cfg["dy"])
    ARENA = max(10, span*1.8)
    ax.set_xlim(cx0-ARENA, cx0+ARENA)
    ax.set_ylim(cy0-ARENA, cy0+ARENA)
    ax.set_zlim(0, max(8, TAKEOFF_ALT*2))
    ax.set_xlabel('X (m)', color='#888')
    ax.set_ylabel('Y (m)', color='#888')
    ax.set_zlabel('Z (m)', color='#888')
    ax.tick_params(colors='#555')
    for sp in ax.spines.values(): sp.set_edgecolor('#333')

    xx, yy = np.meshgrid(np.linspace(cx0-ARENA, cx0+ARENA, 4),
                         np.linspace(cy0-ARENA, cy0+ARENA, 4))
    ax.plot_surface(xx, yy, np.zeros_like(xx), alpha=0.08, color='#5DCAA5')

    # Drones (scatter)
    scatters = [ax.scatter([],[],[], s=100, color=drone_colors[i],
                           depthshade=False, zorder=5)
                for i in range(N)]

    # Flechas de yaw individuales (solo modo distribuido)
    YAW_LEN = cfg["dx"] * 0.45
    yaw_arrows = []
    if cfg["mode"] == 1:
        for i in range(N):
            arr, = ax.plot([],[],[], '-', color='#EF9F27', lw=1.2, alpha=0.7)
            yaw_arrows.append(arr)

    # Centroide
    centroid_dot = ax.scatter([],[],[], s=200, color='#EF9F27',
                              marker='*', depthshade=False, zorder=6)
    centroid_lbl = ax.text(0,0,0,'C', fontsize=9, color='#EF9F27',
                           ha='center', va='bottom', fontweight='bold')

    # Líneas centroide → drones
    c_lines = [ax.plot([],[],[], '-', color='#EF9F27', lw=0.4, alpha=0.25)[0]
               for _ in range(N)]

    # Rejilla de formación (vecinos)
    grid_lines = []
    for r in range(rows):
        for c in range(cols):
            idx = r*cols+c
            if c+1 < cols:
                ln, = ax.plot([],[],[], '--', color='#555', lw=0.7)
                grid_lines.append((ln, idx, idx+1))
            if r+1 < rows:
                ln, = ax.plot([],[],[], '--', color='#555', lw=0.7)
                grid_lines.append((ln, idx, idx+cols))

    # Etiquetas de dron
    show_labels = N <= 30
    drone_labels = []
    if show_labels:
        for i in range(N):
            drone_labels.append(ax.text(0,0,0, f'D{i+1}', fontsize=6,
                                        color='white', ha='center', va='bottom'))

    trail_line, = ax.plot([],[],[], '-', color='#EF9F27', lw=1.0, alpha=0.5)

    hud = ax.text2D(0.02, 0.97, '', transform=ax.transAxes,
                    fontsize=9, color='#9FE1CB', va='top', fontfamily='monospace')
    ax.text2D(0.02, 0.04,
              "T despegue  |  R aterrizaje\n"
              "AD izq/der  |  ←/→ yaw  |  ↑/↓ adelante/atrás\n"
              "SPACE subir |  SHIFT bajar  |  ESC salir",
              transform=ax.transAxes, fontsize=7.5,
              color='#555', va='bottom', fontfamily='monospace')

    # Badge de modo (esquina superior derecha)
    mode_badge = ax.text2D(0.98, 0.97, swarm.mode_str,
                           transform=ax.transAxes, fontsize=9,
                           color=ACC if cfg["mode"]==0 else '#EF9F27',
                           va='top', ha='right', fontfamily='monospace',
                           fontweight='bold')

    def update(_frame):
        with swarm._lock:
            pos   = swarm.positions.copy()
            yaws  = swarm.yaws.copy()
            trail = list(swarm.trail)
            cx,cy,cz = swarm.centroid
            status   = swarm.status_str

        # Drones
        for i, sc in enumerate(scatters):
            sc._offsets3d = ([pos[i,0]], [pos[i,1]], [pos[i,2]])

        # Flechas de yaw (modo distribuido)
        for i, arr in enumerate(yaw_arrows):
            x0,y0,z0 = pos[i]
            arr.set_data([x0, x0+math.cos(yaws[i])*YAW_LEN],
                         [y0, y0+math.sin(yaws[i])*YAW_LEN])
            arr.set_3d_properties([z0, z0])

        if show_labels:
            for i, lbl in enumerate(drone_labels):
                lbl.set_position((pos[i,0], pos[i,1]))
                lbl.set_3d_properties(pos[i,2]+0.35, 'z')

        # Centroide
        centroid_dot._offsets3d = ([cx],[cy],[cz])
        centroid_lbl.set_position((cx,cy))
        centroid_lbl.set_3d_properties(cz+0.5, 'z')

        for i, ln in enumerate(c_lines):
            ln.set_data([cx,pos[i,0]], [cy,pos[i,1]])
            ln.set_3d_properties([cz,pos[i,2]])

        for ln,a,b in grid_lines:
            ln.set_data([pos[a,0],pos[b,0]], [pos[a,1],pos[b,1]])
            ln.set_3d_properties([pos[a,2],pos[b,2]])

        if trail:
            tx,ty,tz = zip(*trail)
            trail_line.set_data(tx,ty)
            trail_line.set_3d_properties(tz)

        yaw_deg = math.degrees(yaws[0]) % 360
        yaw_info = (f"Yaw global: {yaw_deg:.1f}°"
                    if cfg["mode"]==0
                    else f"Yaw D1: {yaw_deg:.1f}°  (individual)")
        hud.set_text(
            f"Modo     : {swarm.mode_str}\n"
            f"Estado   : {status}\n"
            f"Centroide: ({cx:+.1f}, {cy:+.1f}, {cz:.1f}) m\n"
            f"{yaw_info}\n"
            f"Formación: {rows}×{cols} = {N} drones"
        )

        arts = (scatters + yaw_arrows +
                [centroid_dot, centroid_lbl] + c_lines +
                [ln for ln,_,_ in grid_lines] +
                [trail_line, hud, mode_badge])
        if show_labels: arts += drone_labels
        return arts

    def on_close(_): 
        global _running
        _running = False

    fig.canvas.mpl_connect('close_event', on_close)
    if KEYBOARD_AVAILABLE:
        fig.canvas.mpl_connect('key_press_event',
            lambda e: plt.close('all') if e.key=='escape' else None)

    ani = FuncAnimation(fig, update, interval=int(DT*1000),
                        blit=False, cache_frame_data=False)
    plt.title(
        f"Enjambre {rows}×{cols} ({N} drones)  [{swarm.mode_str}]  |  "
        f"offset dx={cfg['dx']:.1f} m  dy={cfg['dy']:.1f} m",
        color='#9FE1CB', pad=10, fontsize=9)
    plt.show()
