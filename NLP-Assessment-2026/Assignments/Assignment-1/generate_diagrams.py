import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 9.5), dpi=300)
ax.set_xlim(-1.5, 17.5)
ax.set_ylim(-1.5, 10.5)
ax.axis('off')

# Title
ax.text(8.0, 10.0, 'Finite State Automaton (FSA) for Absolute Date Expressions', 
        fontsize=17, fontweight='bold', ha='center', color='#0F172A')
ax.text(8.0, 9.4, 'Natural Language Processing (DSA03) | SIMATS School of Engineering', 
        fontsize=11.5, style='italic', ha='center', color='#475569')

# Define states: key -> (x, y, label, is_accept, sublabel)
states = {
    'q0': (0.6, 5.0, 'q0', False, 'Start'),
    'q1': (3.6, 8.2, 'q1', False, 'Seen DOW'),
    'q2': (7.6, 8.2, 'q2', True, 'Holiday (Accept)'),
    'q3': (4.5, 5.0, 'q3', False, 'Seen Month'),
    'q4': (8.0, 6.4, 'q4', False, 'Seen Month \"the\"'),
    'q5': (2.4, 1.8, 'q5', False, 'Seen \"the\"'),
    'q6': (5.5, 1.8, 'q6', False, 'Seen Day'),
    'q7': (8.6, 1.8, 'q7', False, 'Seen Day \"of\"'),
    'q8': (11.5, 5.0, 'q8', True, 'Month+Day (Accept)'),
    'q9': (14.5, 5.0, 'q9', True, '+Year (Accept)'),
    'q10': (16.8, 5.0, 'q10', True, '+Era (Accept)')
}

# Draw states
for s_id, (x, y, name, is_acc, subtext) in states.items():
    r = 0.55
    bg_color = '#DCFCE7' if is_acc else '#F8FAFC'
    border_color = '#15803D' if is_acc else '#1E3A8A'
    circle = patches.Circle((x, y), r, edgecolor=border_color, facecolor=bg_color, lw=2.2, zorder=3)
    ax.add_patch(circle)
    if is_acc:
        inner = patches.Circle((x, y), r*0.82, edgecolor=border_color, facecolor='#BBF7D0', lw=1.6, zorder=3)
        ax.add_patch(inner)
    ax.text(x, y, name, ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A', zorder=4)
    # State description label
    ax.text(x, y - (r + 0.3), subtext, ha='center', va='top', fontsize=8.5, fontweight='semibold', color='#334155')

# Start arrow
ax.annotate('', xy=(states['q0'][0]-0.55, states['q0'][1]), xytext=(states['q0'][0]-1.3, states['q0'][1]),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='#1E3A8A'), zorder=5)
ax.text(states['q0'][0]-1.35, states['q0'][1], 'Start', ha='right', va='center', fontsize=11, fontweight='bold', color='#1E3A8A')

# Helper to draw edge with text
def draw_edge(ax, p1, p2, text, rad=0.0, ha='center', va='bottom', tpos=0.5, color='#2563EB', t_offset=(0,0)):
    arrow = patches.FancyArrowPatch(
        (p1[0], p1[1]), (p2[0], p2[1]),
        connectionstyle=f'arc3,rad={rad}',
        arrowstyle='-|>,head_length=6,head_width=3.5',
        lw=1.8, color=color, zorder=2,
        shrinkA=17, shrinkB=17
    )
    ax.add_patch(arrow)
    mx = (1-tpos)*p1[0] + tpos*p2[0]
    my = (1-tpos)*p1[1] + tpos*p2[1]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dist = (dx**2 + dy**2)**0.5
    if dist > 0:
        nx = -dy / dist * rad * 1.5
        ny = dx / dist * rad * 1.5
    else:
        nx, ny = 0, 0
    ax.text(mx + nx + t_offset[0], my + ny + t_offset[1], text, ha=ha, va=va, fontsize=8.2, fontweight='bold',
            color='#1E293B', bbox=dict(boxstyle='round,pad=0.2', facecolor='#FEF9C3', edgecolor='#FACC15', alpha=0.92, lw=0.8), zorder=5)

# Edges
# q0 to q1 (DOW)
draw_edge(ax, states['q0'], states['q1'], 'DayOfWeek [,] ', rad=0.15, ha='right', va='bottom')
# q1 to q2 (Holiday)
draw_edge(ax, states['q1'], states['q2'], 'Holiday', rad=0.0, ha='center', va='bottom')
# q1 to q3 (Month)
draw_edge(ax, states['q1'], states['q3'], 'Month', rad=0.1, ha='right', va='center')
# q1 to q5 (the)
draw_edge(ax, states['q1'], states['q5'], 'Article ("the")', rad=0.35, ha='right', va='center')
# q1 to q6 (DayNum / DayOrd)
draw_edge(ax, states['q1'], states['q6'], 'DayNum | DayOrd', rad=-0.1, ha='center', va='center')

# q0 to q2 (Holiday)
draw_edge(ax, states['q0'], states['q2'], 'Holiday', rad=0.2, ha='center', va='bottom', tpos=0.45)
# q0 to q3 (Month)
draw_edge(ax, states['q0'], states['q3'], 'Month', rad=0.0, ha='center', va='bottom')
# q0 to q5 (the)
draw_edge(ax, states['q0'], states['q5'], 'Article ("the")', rad=-0.15, ha='right', va='top')
# q0 to q6 (DayNum / DayOrd)
draw_edge(ax, states['q0'], states['q6'], 'DayNum | DayOrd', rad=-0.25, ha='left', va='top', tpos=0.35)

# q3 to q8 (DayNum / DayOrd)
draw_edge(ax, states['q3'], states['q8'], 'DayNum | DayOrd', rad=0.0, ha='center', va='bottom', tpos=0.3)
# q3 to q4 (the)
draw_edge(ax, states['q3'], states['q4'], 'Article ("the")', rad=0.15, ha='right', va='bottom')
# q4 to q8 (DayOrd)
draw_edge(ax, states['q4'], states['q8'], 'DayOrd', rad=0.15, ha='left', va='bottom')
# q3 to q9 (Year)
draw_edge(ax, states['q3'], states['q9'], 'Year (e.g. "Nov 2025")', rad=-0.35, ha='center', va='top', tpos=0.55)

# q5 to q6 (DayOrd)
draw_edge(ax, states['q5'], states['q6'], 'DayOrd', rad=0.0, ha='center', va='top')
# q6 to q7 (of)
draw_edge(ax, states['q6'], states['q7'], 'Prep ("of")', rad=0.0, ha='center', va='top')
# q7 to q8 (Month)
draw_edge(ax, states['q7'], states['q8'], 'Month', rad=-0.15, ha='left', va='bottom')
# q6 to q8 (Month direct)
draw_edge(ax, states['q6'], states['q8'], 'Month (e.g. "15 March")', rad=0.18, ha='left', va='center', tpos=0.6)

# q2 to q9 (Year)
draw_edge(ax, states['q2'], states['q9'], 'Year (e.g. "Christmas 2025")', rad=0.25, ha='left', va='bottom', tpos=0.4)
# q8 to q9 (Year)
draw_edge(ax, states['q8'], states['q9'], '[,] Year', rad=0.0, ha='center', va='bottom')
# q9 to q10 (Era)
draw_edge(ax, states['q9'], states['q10'], 'Era (BC / AD / BCE / CE)', rad=0.0, ha='center', va='bottom')

# Shorthand Box (Legend)
legend_text = (
    "Shorthand Classes of Words (Lexical Categories):\n"
    "• Month: {January..December, Jan..Dec}\n"
    "• DayNum: {1, 2, ..., 31, 01, ..., 31}\n"
    "• DayOrd: {1st, 2nd, ..., 31st, first, second, ..., thirty-first}\n"
    "• DayOfWeek: {Monday..Sunday, Mon..Sun}\n"
    "• Holiday: {Christmas, Thanksgiving, Easter, Halloween, New Year's Day, ...}\n"
    "• Year: {1000..2099, '99, '25, ...}  |  Era: {BC, AD, BCE, CE}\n"
    "• Article: {the}  |  Prep: {of}"
)
ax.text(0.2, -0.9, legend_text, fontsize=9.2, va='bottom', ha='left', color='#0F172A',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1.2))

# Key Insight Box
insight_text = (
    "Absolute vs. Deictic Date Recognition:\n"
    "• Absolute dates anchor to calendar milestones (e.g., 'March 15', 'Christmas').\n"
    "• Deictic dates depend on time of utterance (e.g., 'yesterday', 'tomorrow').\n"
    "• The FSA rejects deictic terms: unrecognized tokens transition to a dead trap state."
)
ax.text(17.2, -0.9, insight_text, fontsize=9.2, va='bottom', ha='right', color='#0F172A',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#EFF6FF', edgecolor='#60A5FA', lw=1.2))

out_path = r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-1\fsa_date_expressions.png'
plt.tight_layout()
plt.savefig(out_path, bbox_inches='tight')
print('FSA diagram successfully saved to:', out_path)
