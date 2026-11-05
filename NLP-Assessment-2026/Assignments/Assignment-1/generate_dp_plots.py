import matplotlib.pyplot as plt
import numpy as np

def plot_dp_matrix(s1, s2, dp, title, filename, optimal_paths=None):
    m, n = len(s1), len(s2)
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    
    matrix = np.array(dp)
    cax = ax.matshow(matrix, cmap='Blues', alpha=0.7)
    
    # Text labels
    col_labels = ['#'] + list(s2)
    row_labels = ['#'] + list(s1)
    
    ax.set_xticks(range(n + 1))
    ax.set_yticks(range(m + 1))
    ax.set_xticklabels(col_labels, fontsize=12, fontweight='bold')
    ax.set_yticklabels(row_labels, fontsize=12, fontweight='bold')
    
    ax.set_xlabel(f'Target: "{s2}"', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel(f'Source: "{s1}"', fontsize=12, fontweight='bold', labelpad=10)
    ax.xaxis.set_label_position('top')
    
    for i in range(m + 1):
        for j in range(n + 1):
            val = dp[i][j]
            is_path = optimal_paths and (i, j) in optimal_paths
            color = '#991B1B' if is_path else '#0F172A'
            weight = 'bold' if is_path else 'normal'
            ax.text(j, i, str(val), ha='center', va='center', fontsize=11, fontweight=weight, color=color)
            if is_path:
                rect = plt.Rectangle((j-0.45, i-0.45), 0.9, 0.9, fill=False, edgecolor='#EF4444', lw=2)
                ax.add_patch(rect)
                
    # Draw arrows along optimal path if provided
    if optimal_paths and len(optimal_paths) > 1:
        for idx in range(len(optimal_paths)-1):
            p1 = optimal_paths[idx]
            p2 = optimal_paths[idx+1]
            ax.annotate('', xy=(p2[1], p2[0]), xytext=(p1[1], p1[0]),
                        arrowprops=dict(arrowstyle='->', lw=2.2, color='#DC2626'))

    plt.title(title, fontsize=13, fontweight='bold', pad=35, color='#1E293B')
    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

# DP calculations
def calc_dp(s1, s2, sub_cost=1):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + sub_cost)
    return dp

# Path for drive -> brief (sub=1):
# (0,0) -> sub d->b (1,1) -> match r (2,2) -> match i (3,3) -> del v (4,3) -> match e (5,4) -> ins f (5,5)
path_db = [(0,0), (1,1), (2,2), (3,3), (4,3), (5,4), (5,5)]
dp_db = calc_dp('drive', 'brief', 1)
plot_dp_matrix('drive', 'brief', dp_db, 
               'Minimum Edit Distance Matrix: "drive" -> "brief"\n(Unit Cost: Del=1, Ins=1, Sub=1 | Distance = 3)',
               r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-1\dp_drive_brief.png',
               path_db)

# Path for drive -> divers (sub=1):
# (0,0) -> match d (1,1) -> del r (2,1) -> match i (3,2) -> match v (4,3) -> match e (5,4) -> ins r (5,5) -> ins s (5,6)
path_dd = [(0,0), (1,1), (2,1), (3,2), (4,3), (5,4), (5,5), (5,6)]
dp_dd = calc_dp('drive', 'divers', 1)
plot_dp_matrix('drive', 'divers', dp_dd, 
               'Minimum Edit Distance Matrix: "drive" -> "divers"\n(Unit Cost: Del=1, Ins=1, Sub=1 | Distance = 3)',
               r'c:\Users\mithu\OneDrive\Desktop\DSA0311 - NATURAL LANGUAGE PROCESSING\NLP-Assessment-2026\Assignments\Assignment-1\dp_drive_divers.png',
               path_dd)

print('DP matrices plotted successfully')
