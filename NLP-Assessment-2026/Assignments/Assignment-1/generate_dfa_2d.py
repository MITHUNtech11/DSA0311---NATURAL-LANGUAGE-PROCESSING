import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 5.5)
ax.axis('off')

ax.text(5.0, 5.0, 'Minimal DFA for Language: Each "a" Preceded and Followed by "b"', 
        fontsize=13, fontweight='bold', ha='center', color='#0F172A')
ax.text(5.0, 4.5, r'Alphabet $\Sigma = \{a, b\}$ | Language $L = \{\epsilon\} \cup b(b \mid ab)^*$', 
        fontsize=10.5, style='italic', ha='center', color='#475569')

def draw_state(ax, x, y, name, is_start=False, is_accept=False, radius=0.55):
    circle = patches.Circle((x, y), radius, edgecolor='#15803D' if is_accept else '#1E3A8A',
                            facecolor='#DCFCE7' if is_accept else '#F8FAFC', lw=2, zorder=3)
    ax.add_patch(circle)
    if is_accept:
        inner = patches.Circle((x, y), radius*0.82, edgecolor='#15803D', facecolor='#BBF7D0', lw=1.5, zorder=3)
        ax.add_patch(inner)
    ax.text(x, y, name, ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A', zorder=4)
    if is_start:
        ax.annotate('', xy=(x-radius, y), xytext=(x-radius-0.8, y),
                    arrowprops=dict(arrowstyle='->', lw=2.2, color='#1E3A8A'), zorder=5)
        ax.text(x-radius-0.85, y, 'Start', ha='right', va='center', fontsize=10, fontweight='bold', color='#1E3A8A')

# States
draw_state(ax, 1.0, 2.5, 'S0', is_start=True, is_accept=True)
draw_state(ax, 4.0, 2.5, 'S1', is_accept=True)
draw_state(ax, 7.0, 2.5, 'S2', is_accept=False)
draw_state(ax, 4.0, 0.2, 'Trap', is_accept=False)

# Labels for states
ax.text(1.0, 1.6, 'Start / Empty (e)\n(Accept)', ha='center', va='top', fontsize=8.5, color='#334155', fontweight='bold')
ax.text(4.0, 3.4, 'Ended in "b"\n(Accept)', ha='center', va='bottom', fontsize=8.5, color='#15803D', fontweight='bold')
ax.text(7.0, 3.4, 'Ended in "a"\n(Waiting for "b")', ha='center', va='bottom', fontsize=8.5, color='#B45309', fontweight='bold')
ax.text(4.0, -0.6, 'Dead State (Trap / Reject)', ha='center', va='top', fontsize=8.5, color='#B91C1C', fontweight='bold')

def draw_edge(ax, p1, p2, text, rad=0.0, ha='center', va='bottom', color='#2563EB', tpos=0.5):
    arrow = patches.FancyArrowPatch(
        p1, p2,
        connectionstyle=f'arc3,rad={rad}',
        arrowstyle='-|>,head_length=5,head_width=3',
        lw=1.8, color=color, zorder=2,
        shrinkA=16, shrinkB=16
    )
    ax.add_patch(arrow)
    mx = (1-tpos)*p1[0] + tpos*p2[0]
    my = (1-tpos)*p1[1] + tpos*p2[1]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = (dx**2 + dy**2)**0.5
    nx = -dy / dist * rad * 1.5 if dist > 0 else 0
    ny = dx / dist * rad * 1.5 if dist > 0 else 0
    ax.text(mx + nx, my + ny, text, ha=ha, va=va, fontsize=9, fontweight='bold',
            color='#1E293B', bbox=dict(boxstyle='round,pad=0.15', facecolor='#FEF9C3', edgecolor='#FACC15', alpha=0.9, lw=0.6), zorder=5)

# Self-loop helper
def draw_loop(ax, p, text, direct='up'):
    x, y = p
    if direct == 'up':
        loop = patches.Arc((x, y+0.55), 0.6, 0.6, angle=0, theta1=200, theta2=-20, color='#2563EB', lw=1.8, zorder=2)
        ax.add_patch(loop)
        ax.annotate('', xy=(x+0.25, y+0.45), xytext=(x+0.28, y+0.52),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color='#2563EB'), zorder=5)
        ax.text(x, y+0.95, text, ha='center', va='bottom', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#FEF9C3', edgecolor='#FACC15', alpha=0.9, lw=0.6), zorder=5)
    elif direct == 'down':
        loop = patches.Arc((x, y-0.55), 0.6, 0.6, angle=0, theta1=20, theta2=160, color='#DC2626', lw=1.8, zorder=2)
        ax.add_patch(loop)
        ax.annotate('', xy=(x-0.25, y-0.45), xytext=(x-0.28, y-0.52),
                    arrowprops=dict(arrowstyle='->', lw=1.8, color='#DC2626'), zorder=5)
        ax.text(x, y-0.95, text, ha='center', va='top', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='#FEE2E2', edgecolor='#F87171', alpha=0.9, lw=0.6), zorder=5)

# Edges
# S0 to S1 on b
draw_edge(ax, (1.0, 2.5), (4.0, 2.5), 'b', rad=0.0, ha='center', va='bottom')
# S0 to Trap on a
draw_edge(ax, (1.0, 2.5), (4.0, 0.2), 'a', rad=0.0, ha='center', va='top', color='#DC2626')
# S1 loop on b
draw_loop(ax, (4.0, 2.5), 'b', direct='up')
# S1 to S2 on a
draw_edge(ax, (4.0, 2.5), (7.0, 2.5), 'a', rad=0.25, ha='center', va='bottom')
# S2 to S1 on b
draw_edge(ax, (7.0, 2.5), (4.0, 2.5), 'b', rad=0.25, ha='center', va='bottom')
# S2 to Trap on a
draw_edge(ax, (7.0, 2.5), (4.0, 0.2), 'a', rad=-0.0, ha='center', va='top', color='#DC2626')
# Trap loop on a,b
draw_loop(ax, (4.0, 0.2), 'a, b', direct='down')

plt.tight_layout()
out_path = r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-1\dfa_question_2d.png'
plt.savefig(out_path, bbox_inches='tight')
print('DFA saved to:', out_path)
