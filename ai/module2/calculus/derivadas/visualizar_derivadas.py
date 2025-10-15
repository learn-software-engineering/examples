import numpy as np
import matplotlib.pyplot as plt

# Configurar el estilo
plt.style.use('seaborn-v0_8-darkgrid')

# Definir la función f(x) = x^2
def f(x):
    return x**2

# Derivada de f(x) = 2x
def f_prima(x):
    return 2*x

# ============= FIGURA 1: ¿QUÉ ES LA DERIVADA? =============
fig1 = plt.figure(figsize=(12, 8))
ax1 = fig1.add_subplot(111)

x0 = 2
h = 1.5

x = np.linspace(0, 5, 200)
y = f(x)

# Dibujar la función
ax1.plot(x, y, 'b-', linewidth=3, label='f(x) = x²', zorder=1)

# Puntos importantes
ax1.plot(x0, f(x0), 'ro', markersize=15, zorder=5, label=f'P₁({x0}, {f(x0)})')
ax1.plot(x0+h, f(x0+h), 'go', markersize=15, zorder=5, label=f'P₂({x0+h:.1f}, {f(x0+h):.2f})')

# Dibujar la secante
x_secante = np.array([x0, x0+h])
y_secante = np.array([f(x0), f(x0+h)])
ax1.plot(x_secante, y_secante, 'r--', linewidth=2.5, label='Recta Secante', zorder=3)

# Dibujar Δx y Δy con flechas
ax1.annotate('', xy=(x0+h, f(x0)), xytext=(x0, f(x0)),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=2.5))
ax1.text(x0+h/2, f(x0)-0.8, 'Δx = h', fontsize=14, color='purple',
         fontweight='bold', ha='center',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

ax1.annotate('', xy=(x0+h, f(x0+h)), xytext=(x0+h, f(x0)),
            arrowprops=dict(arrowstyle='<->', color='orange', lw=2.5))
ax1.text(x0+h+0.5, (f(x0)+f(x0+h))/2, 'Δy', fontsize=14, color='orange',
         fontweight='bold',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

# Título y fórmula
ax1.set_title('PASO 1: Pendiente de la Secante', fontsize=18, fontweight='bold', pad=20)
ax1.text(2.5, 18, r'Pendiente = $\frac{\Delta y}{\Delta x} = \frac{f(x_0+h) - f(x_0)}{h}$',
         fontsize=16, bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8),
         ha='center', fontweight='bold')

# Calcular y mostrar la pendiente
pendiente_secante = (f(x0+h) - f(x0)) / h
ax1.text(2.5, 1, f'Pendiente secante = {pendiente_secante:.2f}',
         fontsize=14, bbox=dict(boxstyle='round,pad=0.7', facecolor='lightcoral', alpha=0.8),
         ha='center', fontweight='bold')

ax1.set_xlabel('x', fontsize=14, fontweight='bold')
ax1.set_ylabel('f(x)', fontsize=14, fontweight='bold')
ax1.legend(fontsize=12, loc='upper left')
ax1.grid(True, alpha=0.4)
ax1.set_xlim(0.5, 5)
ax1.set_ylim(-1, 20)

plt.tight_layout()
plt.show()

# ============= FIGURA 2: EL LÍMITE =============
fig2 = plt.figure(figsize=(12, 8))
ax2 = fig2.add_subplot(111)

x = np.linspace(0, 5, 200)
y = f(x)
ax2.plot(x, y, 'b-', linewidth=3, label='f(x) = x²')
ax2.plot(x0, f(x0), 'ro', markersize=15, zorder=5)

# Diferentes valores de h
h_values = [1.5, 1.0, 0.6, 0.3, 0.1]
colors = ['red', 'orange', 'yellow', 'lime', 'cyan']
alphas = [0.4, 0.5, 0.6, 0.7, 0.8]

for i, (h, color, alpha) in enumerate(zip(h_values, colors, alphas)):
    x_sec = np.array([x0-0.5, x0+h+0.5])
    pendiente = (f(x0+h) - f(x0)) / h
    y_sec = f(x0) + pendiente * (x_sec - x0)
    ax2.plot(x_sec, y_sec, '--', color=color, linewidth=2, alpha=alpha,
             label=f'h={h:.1f}, m≈{pendiente:.2f}')

# Recta tangente (límite cuando h→0)
pendiente_tangente = f_prima(x0)
x_tang = np.linspace(x0-1, x0+2, 100)
y_tang = f(x0) + pendiente_tangente * (x_tang - x0)
ax2.plot(x_tang, y_tang, 'g-', linewidth=4, label=f'TANGENTE: m={pendiente_tangente}', zorder=4)

ax2.set_title('PASO 2: Haciendo h → 0 (límite)', fontsize=18, fontweight='bold', pad=20)
ax2.text(2.5, 17, r"$\lim_{h \to 0} \frac{f(x_0+h) - f(x_0)}{h} = f'(x_0)$",
         fontsize=16, bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8),
         ha='center', fontweight='bold')

ax2.text(2.5, 1, '¡La derivada es la pendiente de la tangente!',
         fontsize=13, bbox=dict(boxstyle='round,pad=0.7', facecolor='gold', alpha=0.9),
         ha='center', fontweight='bold', style='italic')

ax2.set_xlabel('x', fontsize=14, fontweight='bold')
ax2.set_ylabel('f(x)', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10, loc='upper left')
ax2.grid(True, alpha=0.4)
ax2.set_xlim(0.5, 5)
ax2.set_ylim(-1, 20)

plt.tight_layout()
plt.show()

# ============= FIGURA 3: INTERPRETACIÓN GEOMÉTRICA =============
fig3 = plt.figure(figsize=(12, 8))
ax3 = fig3.add_subplot(111)

puntos_demo = [0.5, 1, 1.5, 2, 2.5, 3, 3.5]
x = np.linspace(0, 4, 200)
y = f(x)

ax3.plot(x, y, 'b-', linewidth=3, label='f(x) = x²')

for px in puntos_demo:
    # Punto en la curva
    ax3.plot(px, f(px), 'ro', markersize=10, zorder=5)

    # Tangente en ese punto
    pendiente = f_prima(px)
    x_tang = np.linspace(px-0.5, px+0.5, 50)
    y_tang = f(px) + pendiente * (x_tang - px)
    ax3.plot(x_tang, y_tang, 'g-', linewidth=2, alpha=0.6)

    # Mostrar el valor de la derivada
    if px in [1, 2, 3]:
        ax3.text(px, f(px)+1.2, f"f'({px})={f_prima(px):.1f}",
                fontsize=11, ha='center', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7))

ax3.set_title('PASO 3: Derivada en Diferentes Puntos', fontsize=18, fontweight='bold', pad=20)
ax3.text(2, 14, 'Cada punto tiene su propia tangente\n(y por tanto, su propia derivada)',
         fontsize=13, bbox=dict(boxstyle='round,pad=0.8', facecolor='lavender', alpha=0.8),
         ha='center', fontweight='bold')

ax3.set_xlabel('x', fontsize=14, fontweight='bold')
ax3.set_ylabel('f(x)', fontsize=14, fontweight='bold')
ax3.legend(fontsize=12)
ax3.grid(True, alpha=0.4)
ax3.set_xlim(0, 4)
ax3.set_ylim(-1, 16)

plt.tight_layout()
plt.show()

# ============= FIGURA 4: FUNCIÓN VS DERIVADA =============
fig4 = plt.figure(figsize=(12, 8))
ax4 = fig4.add_subplot(111)

x = np.linspace(-1, 4, 200)
y_func = f(x)
y_deriv = f_prima(x)

ax4.plot(x, y_func, 'b-', linewidth=3, label="f(x) = x² (función original)")
ax4.plot(x, y_deriv, 'r-', linewidth=3, label="f'(x) = 2x (derivada)")

# Puntos especiales con anotaciones
puntos_especiales = [0, 1, 2, 3]
for px in puntos_especiales:
    ax4.plot(px, f(px), 'bo', markersize=12)
    ax4.plot(px, f_prima(px), 'ro', markersize=12)

    # Flechas y anotaciones explicativas
    if px == 0:
        ax4.annotate('Pendiente = 0\n(mínimo)', xy=(px, f(px)), xytext=(0.5, 3),
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
    elif px == 2:
        ax4.annotate('Crece rápido\nPendiente = 4', xy=(px, f(px)), xytext=(2.5, 6),
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', lw=2, color='red'))

# Regiones de crecimiento
ax4.axvspan(0, 4, alpha=0.1, color='green', label='f(x) creciente → f\'(x) > 0')
ax4.axvspan(-1, 0, alpha=0.1, color='red', label='f(x) decreciente → f\'(x) < 0')

ax4.axhline(y=0, color='k', linestyle='-', linewidth=1)
ax4.axvline(x=0, color='k', linestyle='-', linewidth=1)

ax4.set_title('PASO 4: Comparación f(x) vs f\'(x)', fontsize=18, fontweight='bold', pad=20)
ax4.text(1.5, 13, 'La derivada nos dice:\n• Qué tan rápido cambia f(x)\n• Si f(x) crece (+) o decrece (-)',
         fontsize=12, bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', alpha=0.9),
         ha='center', fontweight='bold')

ax4.set_xlabel('x', fontsize=14, fontweight='bold')
ax4.set_ylabel('y', fontsize=14, fontweight='bold')
ax4.legend(fontsize=11, loc='upper left')
ax4.grid(True, alpha=0.4)
ax4.set_xlim(-1, 4)
ax4.set_ylim(-2, 16)

plt.tight_layout()
plt.show()

# ============= RESUMEN ESCRITO =============
print("\n" + "="*80)
print("📚 RESUMEN: ¿QUÉ ES LA DERIVADA?")
print("="*80)
print("""
La DERIVADA de una función en un punto es la PENDIENTE de la recta TANGENTE
a la curva en ese punto.

🔢 DEFINICIÓN MATEMÁTICA:
   f'(x) = lim[h→0] (f(x+h) - f(x)) / h

📐 INTERPRETACIÓN GEOMÉTRICA:
   • Es la pendiente de la recta tangente
   • Nos dice qué tan "inclinada" está la curva en ese punto

📊 INTERPRETACIÓN FÍSICA:
   • Representa la velocidad de cambio
   • Si f(x) es posición, f'(x) es velocidad
   • Si f(x) es velocidad, f'(x) es aceleración

✅ EJEMPLO: f(x) = x²
   • La derivada es f'(x) = 2x
   • En x=0: f'(0) = 0 (tangente horizontal, mínimo)
   • En x=2: f'(2) = 4 (tangente con pendiente 4, crece rápido)
   • En x=3: f'(3) = 6 (tangente con pendiente 6, crece más rápido)

💡 REGLA PRÁCTICA:
   • Si f'(x) > 0 → la función CRECE
   • Si f'(x) < 0 → la función DECRECE
   • Si f'(x) = 0 → la función tiene un EXTREMO (máximo o mínimo)
""")
print("="*80)
