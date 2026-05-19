import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(8, 5))
ax = fig.add_subplot(111, projection='3d')

fig.patch.set_facecolor('#282a36')
ax.set_facecolor('#282a36')

# Spacing them out a bit more so they are distinct but clearly clustered
apple = [8, 8, 8]
pear = [7, 6, 8]
rice = [1, 2, 1]

ax.scatter(apple[0], apple[1], apple[2], c='#50fa7b', s=200, depthshade=False)
ax.scatter(pear[0], pear[1], pear[2], c='#50fa7b', s=200, depthshade=False)
ax.scatter(rice[0], rice[1], rice[2], c='#ff5555', s=200, depthshade=False)

ax.text(apple[0]+0.4, apple[1], apple[2], 'Apple', color='#f8f8f2', fontsize=14, fontweight='bold')
ax.text(pear[0]+0.4, pear[1], pear[2], 'Pear', color='#f8f8f2', fontsize=14, fontweight='bold')
ax.text(rice[0]+0.4, rice[1], rice[2], 'Rice', color='#f8f8f2', fontsize=14, fontweight='bold')

ax.set_xlim([0, 10])
ax.set_ylim([0, 10])
ax.set_zlim([0, 10])

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('#6272a4')
ax.yaxis.pane.set_edgecolor('#6272a4')
ax.zaxis.pane.set_edgecolor('#6272a4')

ax.xaxis.label.set_color('#8be9fd')
ax.yaxis.label.set_color('#8be9fd')
ax.zaxis.label.set_color('#8be9fd')
ax.tick_params(axis='x', colors='#6272a4')
ax.tick_params(axis='y', colors='#6272a4')
ax.tick_params(axis='z', colors='#6272a4')

ax.grid(color='#44475a', linestyle='dashed', linewidth=0.5)
plt.title('Vector Space Representation', color='#bd93f9', fontsize=16, pad=20)
plt.tight_layout()

plt.savefig('/home/gateman/.openclaw/workspace/revealjs-ppt-presentations/rag-agent-sharing/vector_space.png', 
            dpi=300, bbox_inches='tight', facecolor='#282a36')
