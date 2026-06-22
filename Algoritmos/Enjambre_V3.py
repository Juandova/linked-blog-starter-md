"""
Simulación de control de enjambre centralizado — matriz N×M de drones
Controles:
  T           → Despegue del enjambre
  R           → Aterrizaje del enjambre
  UP / DOWN   → Adelante / Atrás
  A / D       → Izquierda / Derecha
  LEFT/RIGHT  → Yaw −/+
  ESPACIO     → Subir (eje Z)
  SHIFT       → Bajar (eje Z)
  ESC         → Salir

Dependencias:
  pip install matplotlib keyboard numpy
"""

import math
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
from matplotlib.animation import FuncAnimation

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("[AVISO] 'keyboard' no instalado. pip install keyboard")
    print("        Usando modo demo con movimiento automático.\n")


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
    """
    Genera los offsets de formación para una matriz rows×cols.
    dx = separación entre columnas (eje Y del enjambre)
    dy = separación entre filas   (eje X del enjambre)
    El centroide queda en el centro geométrico de la matriz.
    """
    offsets = []
    # Centrar la rejilla
    x_start = -((cols - 1) / 2.0) * dx
    y_start =  ((rows - 1) / 2.0) * dy
    for r in range(rows):
        for c in range(cols):
            ox = x_start + c * dx
            oy = y_start - r * dy
            offsets.append([ox, oy, 0.0])
    return np.array(offsets, dtype=float)


# ──────────────────────────────────────────────
#  INTERFAZ DE CONFIGURACIÓN (tkinter)
# ──────────────────────────────────────────────
BG  = "#1a1a2e"
FG  = "#e0e0e0"
ACC = "#5DCAA5"
BG2 = "#252545"
FONT_MONO = ("Consolas", 10)
FONT_TITLE = ("Consolas", 12, "bold")
FONT_SUB   = ("Consolas", 9)


def styled_label(parent, text, title=False, sub=False, **kwargs):
    color = ACC if title else ("#888780" if sub else FG)
    font  = FONT_TITLE if title else (FONT_SUB if sub else FONT_MONO)
    return tk.Label(parent, text=text, bg=BG, fg=color, font=font, **kwargs)


def styled_entry(parent, default, width=8):
    var = tk.StringVar(value=str(default))
    e = tk.Entry(parent, textvariable=var, width=width,
                 bg=BG2, fg=FG, insertbackground=FG,
                 relief="flat", font=FONT_MONO,
                 highlightthickness=1, highlightcolor=ACC,
                 highlightbackground="#333355")
    return var, e


def styled_spin(parent, from_, to, var, width=6):
    return tk.Spinbox(parent, from_=from_, to=to, textvariable=var,
                      width=width, bg=BG2, fg=FG, buttonbackground=BG2,
                      insertbackground=FG, relief="flat", font=FONT_MONO,
                      highlightthickness=1, highlightcolor=ACC,
                      highlightbackground="#333355")


class ConfigDialog:
    def __init__(self):
        self.result = None
        self.root = tk.Tk()
        self.root.title("Configuración del enjambre")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._build_ui()
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _sep(self):
        tk.Frame(self.root, bg="#2a2a4a", height=1).pack(fill="x", padx=20, pady=6)

    def _row_frame(self):
        f = tk.Frame(self.root, bg=BG)
        f.pack(fill="x", padx=24, pady=3)
        return f

    def _build_ui(self):
        root = self.root

        # ── Título ──
        styled_label(root, "🚁  Control de enjambre", title=True).pack(pady=(18, 2))
        styled_label(root, "Configura la simulación antes de comenzar", sub=True).pack(pady=(0, 10))
        self._sep()

        # ── Posición inicial del centroide ──
        styled_label(root, "Posición inicial del centroide (m)", title=True).pack(anchor="w", padx=24, pady=(8, 0))
        styled_label(root, "Punto de referencia central del enjambre", sub=True).pack(anchor="w", padx=24)

        for lbl, attr, default in [("X (m)", "_cx", 0.0),
                                    ("Y (m)", "_cy", 0.0),
                                    ("Z (m, ≥ 0)", "_cz", 0.0)]:
            f = self._row_frame()
            styled_label(f, f"{lbl}:").pack(side="left")
            var, entry = styled_entry(f, default)
            entry.pack(side="left", padx=(8, 0))
            setattr(self, attr, var)

        self._sep()

        # ── Matriz de drones ──
        styled_label(root, "Formación en matriz", title=True).pack(anchor="w", padx=24, pady=(8, 0))
        styled_label(root, "Número de filas y columnas de la rejilla", sub=True).pack(anchor="w", padx=24)

        self._rows = tk.IntVar(value=2)
        self._cols = tk.IntVar(value=3)

        for lbl, var in [("Filas:", self._rows), ("Columnas:", self._cols)]:
            f = self._row_frame()
            styled_label(f, lbl).pack(side="left")
            styled_spin(f, 1, 20, var).pack(side="left", padx=(8, 0))

        self._sep()

        # ── Offset entre drones ──
        styled_label(root, "Separación entre drones (m)", title=True).pack(anchor="w", padx=24, pady=(8, 0))
        styled_label(root, "Distancia entre drones adyacentes", sub=True).pack(anchor="w", padx=24)

        for lbl, attr, default in [("Offset X (columnas):", "_dx", 2.0),
                                    ("Offset Y (filas):",    "_dy", 2.0)]:
            f = self._row_frame()
            styled_label(f, lbl).pack(side="left")
            var, entry = styled_entry(f, default)
            entry.pack(side="left", padx=(8, 0))
            setattr(self, attr, var)

        self._sep()

        # ── Preview canvas ──
        styled_label(root, "Vista previa de la formación", sub=True).pack(pady=(2, 4))
        self._canvas = tk.Canvas(root, width=260, height=120,
                                 bg="#12122a", highlightthickness=0)
        self._canvas.pack(pady=4)

        for v in (self._rows, self._cols):
            v.trace_add("write", lambda *_: self._draw_preview())
        self._draw_preview()

        # ── Botón iniciar ──
        btn = tk.Button(root, text="▶  Iniciar simulación",
                        bg=ACC, fg=BG, font=("Consolas", 10, "bold"),
                        relief="flat", padx=12, pady=6,
                        activebackground="#3eaa85", cursor="hand2",
                        command=self._confirm)
        btn.pack(pady=(8, 20))

    def _draw_preview(self):
        c = self._canvas
        c.delete("all")
        try:
            rows = max(1, int(self._rows.get()))
            cols = max(1, int(self._cols.get()))
        except Exception:
            return
        rows = min(rows, 10)
        cols = min(cols, 10)
        n = rows * cols
        # Calcular tamaño de celda para que quepan en el canvas
        margin = 16
        cw, ch = 260 - 2*margin, 120 - 2*margin
        cell_w = cw / max(cols, 1)
        cell_h = ch / max(rows, 1)
        r_dot = min(cell_w, cell_h) * 0.32
        r_dot = max(4, min(r_dot, 14))
        colors_row = ['#5DCAA5', '#7F77DD', '#EF9F27', '#D85A30',
                      '#378ADD', '#993556', '#888780', '#9FE1CB',
                      '#F7C59F', '#B5EAD7']
        for r in range(rows):
            for ci in range(cols):
                idx = r * cols + ci
                x = margin + (ci + 0.5) * cell_w
                y = margin + (r  + 0.5) * cell_h
                col = colors_row[r % len(colors_row)]
                c.create_oval(x-r_dot, y-r_dot, x+r_dot, y+r_dot,
                              fill=col, outline="")
                if r_dot >= 7:
                    c.create_text(x, y, text=f"D{idx+1}",
                                  fill="white", font=("Consolas", int(r_dot*0.7)))
        c.create_text(130, 110, text=f"{rows}×{cols} = {n} drones",
                      fill="#888780", font=FONT_SUB)

    def _confirm(self):
        try:
            cx  = float(self._cx.get())
            cy  = float(self._cy.get())
            cz  = float(self._cz.get())
            if cz < 0:
                raise ValueError("Z no puede ser negativa")
            rows = int(self._rows.get())
            cols = int(self._cols.get())
            if rows < 1 or cols < 1:
                raise ValueError("Filas y columnas deben ser ≥ 1")
            dx = float(self._dx.get())
            dy = float(self._dy.get())
            if dx <= 0 or dy <= 0:
                raise ValueError("Los offsets deben ser > 0")
        except ValueError as e:
            messagebox.showerror("Error de configuración", str(e),
                                 parent=self.root)
            return
        self.result = dict(cx=cx, cy=cy, cz=cz,
                           rows=rows, cols=cols, dx=dx, dy=dy)
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.result


# ──────────────────────────────────────────────
#  ESTADO DEL ENJAMBRE
# ──────────────────────────────────────────────
class SwarmState:
    LANDED     = 'LANDED'
    TAKING_OFF = 'TAKING OFF'
    FLYING     = 'FLYING'
    LANDING    = 'LANDING'

    def __init__(self, cx0, cy0, cz0, formation_offsets):
        self.cx = cx0
        self.cy = cy0
        self.cz = cz0
        self.yaw = 0.0
        self.status = self.LANDED
        self.formation_offsets = formation_offsets
        self.n_drones = len(formation_offsets)

        # Posiciones iniciales
        self.positions = formation_offsets.copy()
        self.positions[:, 0] += cx0
        self.positions[:, 1] += cy0
        self.positions[:, 2]  = cz0

        self.trail = [(cx0, cy0, cz0)]
        self._lock = threading.Lock()

    def _rotated_offset(self, off):
        c, s = math.cos(self.yaw), math.sin(self.yaw)
        return (c*off[0] - s*off[1],
                s*off[0] + c*off[1],
                off[2])

    def update(self, keys):
        with self._lock:
            if self.status == self.LANDED:
                if keys.get('takeoff'):
                    self.status = self.TAKING_OFF

            elif self.status == self.TAKING_OFF:
                self.cz += TAKEOFF_SPEED * DT
                if self.cz >= TAKEOFF_ALT:
                    self.cz = TAKEOFF_ALT
                    self.status = self.FLYING

            elif self.status == self.FLYING:
                if keys.get('land'):
                    self.status = self.LANDING
                else:
                    if keys.get('yaw_left'):
                        self.yaw += YAW_RATE * DT
                    if keys.get('yaw_right'):
                        self.yaw -= YAW_RATE * DT
                    c, s = math.cos(self.yaw), math.sin(self.yaw)
                    vx = (keys.get('fwd', 0) - keys.get('bwd', 0)) * V_XY
                    vy = (keys.get('left', 0) - keys.get('right', 0)) * V_XY
                    vz = (keys.get('up', 0)   - keys.get('down', 0))  * V_Z
                    self.cx += (c*vx - s*vy) * DT
                    self.cy += (s*vx + c*vy) * DT
                    self.cz  = max(0.1, self.cz + vz * DT)

            elif self.status == self.LANDING:
                self.cz -= TAKEOFF_SPEED * DT
                if self.cz <= 0.0:
                    self.cz = 0.0
                    self.status = self.LANDED

            for i, off in enumerate(self.formation_offsets):
                rx, ry, rz = self._rotated_offset(off)
                self.positions[i] = [self.cx+rx, self.cy+ry, self.cz+rz]

            if math.dist(self.trail[-1], (self.cx, self.cy, self.cz)) > 0.05:
                self.trail.append((self.cx, self.cy, self.cz))
                if len(self.trail) > 300:
                    self.trail.pop(0)


# ──────────────────────────────────────────────
#  LECTURA DE TECLADO
# ──────────────────────────────────────────────
def read_keys():
    if not KEYBOARD_AVAILABLE:
        t = time.time()
        return {
            'takeoff':   (int(t) % 20 == 1),
            'land':      False,
            'fwd':       int(3 < t % 20 < 8),
            'bwd':       0, 'left': int(8 < t % 20 < 12),
            'right':     0, 'yaw_left': int(12 < t % 20 < 16),
            'yaw_right': 0, 'up': int(t % 20 < 3), 'down': 0,
        }
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
#  COLORES DE DRONES (por fila)
# ──────────────────────────────────────────────
ROW_COLORS = ['#5DCAA5', '#7F77DD', '#EF9F27', '#D85A30',
              '#378ADD', '#993556', '#888780', '#9FE1CB',
              '#F7C59F', '#B5EAD7']


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
if __name__ == "__main__":

    cfg = ConfigDialog().run()
    if cfg is None:
        print("Configuración cancelada.")
        exit(0)

    rows, cols = cfg["rows"], cfg["cols"]
    formation_offsets = build_formation_offsets(rows, cols, cfg["dx"], cfg["dy"])
    N_DRONES = rows * cols

    # Color por fila
    drone_colors = []
    for r in range(rows):
        col = ROW_COLORS[r % len(ROW_COLORS)]
        drone_colors.extend([col] * cols)

    _swarm  = SwarmState(cfg["cx"], cfg["cy"], cfg["cz"], formation_offsets)
    _running = True

    def control_loop():
        while _running:
            t0 = time.perf_counter()
            _swarm.update(read_keys())
            elapsed = time.perf_counter() - t0
            time.sleep(max(0.0, DT - elapsed))

    threading.Thread(target=control_loop, daemon=True).start()

    # ── Visualización ──
    fig = plt.figure(figsize=(11, 7), facecolor='#1a1a2e')
    ax  = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#1a1a2e')
    fig.subplots_adjust(left=0, right=1, bottom=0.02, top=0.96)

    cx0, cy0 = cfg["cx"], cfg["cy"]
    # Arena proporcional al tamaño de la formación
    span = max(cols * cfg["dx"], rows * cfg["dy"])
    ARENA = max(10, span * 1.8)
    ax.set_xlim(cx0 - ARENA, cx0 + ARENA)
    ax.set_ylim(cy0 - ARENA, cy0 + ARENA)
    ax.set_zlim(0, max(8, TAKEOFF_ALT * 2))
    ax.set_xlabel('X (m)', color='#888')
    ax.set_ylabel('Y (m)', color='#888')
    ax.set_zlabel('Z (m)', color='#888')
    ax.tick_params(colors='#555')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')

    xx, yy = np.meshgrid(np.linspace(cx0-ARENA, cx0+ARENA, 4),
                         np.linspace(cy0-ARENA, cy0+ARENA, 4))
    ax.plot_surface(xx, yy, np.zeros_like(xx),
                    alpha=0.08, color='#5DCAA5', zorder=0)

    # Drones
    scatter_plots = [
        ax.scatter([], [], [], s=100, color=drone_colors[i],
                   depthshade=False, zorder=5)
        for i in range(N_DRONES)
    ]

    # Centroide
    centroid_dot = ax.scatter([], [], [], s=200, color='#EF9F27',
                              marker='*', depthshade=False, zorder=6)
    centroid_lbl = ax.text(0, 0, 0, 'C', fontsize=9, color='#EF9F27',
                           ha='center', va='bottom', fontweight='bold')

    # Líneas centroide → cada dron
    centroid_lines = [
        ax.plot([], [], [], '-', color='#EF9F27', lw=0.4, alpha=0.3)[0]
        for _ in range(N_DRONES)
    ]

    # Líneas de formación: conectar vecinos en la rejilla
    grid_lines = []
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            if c + 1 < cols:   # vecino derecho
                ln, = ax.plot([], [], [], '--', color='#555', lw=0.7)
                grid_lines.append((ln, idx, idx + 1))
            if r + 1 < rows:   # vecino inferior
                ln, = ax.plot([], [], [], '--', color='#555', lw=0.7)
                grid_lines.append((ln, idx, idx + cols))

    # Etiquetas de dron (solo si no hay demasiados)
    show_labels = N_DRONES <= 30
    drone_labels = []
    if show_labels:
        for i in range(N_DRONES):
            lbl = ax.text(0, 0, 0, f'D{i+1}', fontsize=6,
                          color='white', ha='center', va='bottom')
            drone_labels.append(lbl)

    # Trail
    trail_line, = ax.plot([], [], [], '-', color='#EF9F27', lw=1.0, alpha=0.6)

    # HUD
    hud = ax.text2D(0.02, 0.97, '', transform=ax.transAxes,
                    fontsize=9, color='#9FE1CB', va='top',
                    fontfamily='monospace')
    ax.text2D(0.02, 0.04,
              "T despegue  |  R aterrizaje\n"
              "AD izq/der  |  ←/→ yaw  |  ↑/↓ adelante/atrás\n"
              "SPACE subir |  SHIFT bajar  |  ESC salir",
              transform=ax.transAxes, fontsize=7.5,
              color='#555', va='bottom', fontfamily='monospace')

    def update(_frame):
        with _swarm._lock:
            pos   = _swarm.positions.copy()
            trail = list(_swarm.trail)
            cx, cy, cz = _swarm.cx, _swarm.cy, _swarm.cz
            yaw_deg    = math.degrees(_swarm.yaw) % 360
            status     = _swarm.status

        for i, sc in enumerate(scatter_plots):
            sc._offsets3d = ([pos[i,0]], [pos[i,1]], [pos[i,2]])

        if show_labels:
            for i, lbl in enumerate(drone_labels):
                lbl.set_position((pos[i,0], pos[i,1]))
                lbl.set_3d_properties(pos[i,2] + 0.35, 'z')

        centroid_dot._offsets3d = ([cx], [cy], [cz])
        centroid_lbl.set_position((cx, cy))
        centroid_lbl.set_3d_properties(cz + 0.5, 'z')

        for i, ln in enumerate(centroid_lines):
            ln.set_data([cx, pos[i,0]], [cy, pos[i,1]])
            ln.set_3d_properties([cz, pos[i,2]])

        for ln, a, b in grid_lines:
            ln.set_data([pos[a,0], pos[b,0]], [pos[a,1], pos[b,1]])
            ln.set_3d_properties([pos[a,2], pos[b,2]])

        if trail:
            tx, ty, tz = zip(*trail)
            trail_line.set_data(tx, ty)
            trail_line.set_3d_properties(tz)

        hud.set_text(
            f"Estado   : {status}\n"
            f"Centroide: ({cx:+.1f}, {cy:+.1f}, {cz:.1f}) m\n"
            f"Yaw      : {yaw_deg:.1f}°\n"
            f"Formación: {rows}×{cols} = {N_DRONES} drones\n"
            f"Offset   : dx={cfg['dx']:.1f} m  dy={cfg['dy']:.1f} m"
        )
        arts = (scatter_plots + [centroid_dot, centroid_lbl] +
                centroid_lines + [ln for ln,_,_ in grid_lines] +
                [trail_line, hud])
        if show_labels:
            arts += drone_labels
        return arts

    def on_close(_):
        global _running
        _running = False

    fig.canvas.mpl_connect('close_event', on_close)
    if KEYBOARD_AVAILABLE:
        fig.canvas.mpl_connect('key_press_event',
                               lambda e: plt.close('all') if e.key == 'escape' else None)

    ani = FuncAnimation(fig, update, interval=int(DT * 1000),
                        blit=False, cache_frame_data=False)
    plt.title(
        f"Enjambre {rows}×{cols} ({N_DRONES} drones)  |  "
        f"offset dx={cfg['dx']:.1f} m  dy={cfg['dy']:.1f} m  |  "
        f"origen ({cfg['cx']:.1f}, {cfg['cy']:.1f}, {cfg['cz']:.1f}) m",
        color='#9FE1CB', pad=10, fontsize=9)
    plt.show()
