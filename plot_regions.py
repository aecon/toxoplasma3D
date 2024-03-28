import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help="input file, dat")
parser.add_argument('-o', type=str, required=True, help="output directory for figures")
args = parser.parse_args()

if not os.path.exists(args.o):
    os.makedirs(args.o)

data = np.loadtxt(args.i, skiprows=1)

dx=6.52*1.e-3
dz=6.00*1.e-3
regions = ["Brain stem", "Hippocampus", "Hypothalamus", "Cortex", "Thalamus"]
vp = dx*dx*dz
# 01_Toxofilin-Cre
group1 = [4834, 4836, 4844, 4849, 4851, 4858, 4864, 4868]
# 02_Gra16-Cre
group2 = [4837, 4840, 4847, 4848, 4850, 4871, 4873]
# 03_saline
group3 = [4838, 4843]


Nc = np.shape(data)[1]
x_pos = np.arange(len(regions))

my_cmap = plt.cm.get_cmap('plasma')

g = []
fig, ax = plt.subplots(figsize=(9,5))
for i,s in enumerate(group1):
    idx1 = np.where(data[:,0]==s)[0]
    o = data[idx1,:][0] * vp
    g.append( o )
    print(o)
    ax.bar(x_pos-0.4+0.1*i, o[1::], width=0.1, edgecolor='k', linewidth=0.5, align='edge', label=s, color=my_cmap(i/len(group1)))
ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=13)
plt.xticks(rotation=0)
plt.ylim([0,1])
plt.legend(prop={'size': 12})
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig("%s/pic_per_region_counts_group1-TOXO.png"%args.o, transparent=True)
data_group1 = np.asarray(g)
means1 = np.mean(g, axis=0)[1::]
stads1 = np.std( g, axis=0)[1::]

g = []
fig, ax = plt.subplots(figsize=(9,5))
for i,s in enumerate(group2):
    idx1 = np.where(data[:,0]==s)[0]
    o = data[idx1,:][0] * vp
    g.append( o )
    ax.bar(x_pos-0.35+0.1*i, o[1::], width=0.1, edgecolor='k', linewidth=0.5, align='edge', label=s, color=my_cmap(i/len(group2)))
ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=13)
plt.xticks(rotation=0)
plt.ylim([0,1])
plt.legend(prop={'size': 12})
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig("%s/pic_per_region_counts_group2-Gra16.png"%args.o, transparent=True)
data_group2 = np.asarray(g)
means2 = np.mean(g, axis=0)[1::]
stads2 = np.std( g, axis=0)[1::]

g = []
fig, ax = plt.subplots(figsize=(9,5))
for i,s in enumerate(group3):
    idx1 = np.where(data[:,0]==s)[0]
    o = data[idx1,:][0] * vp
    g.append( o )
    ax.bar(x_pos-0.05+0.1*i, o[1::], width=0.1, edgecolor='k', linewidth=0.5, align='edge', label=s, color=my_cmap(i/len(group3)))
ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=13)
plt.xticks(rotation=0)
plt.ylim([0,1])
plt.legend(prop={'size': 12})
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.tight_layout()
plt.savefig("%s/pic_per_region_counts_group3-SALINE.png"%args.o, transparent=True)
data_group3 = np.asarray(g)
means3 = np.mean(g, axis=0)[1::]
stads3 = np.std( g, axis=0)[1::]

# checks
print("Group data:")
print(data_group1)
print(data_group2)
print(data_group3)

fig, ax = plt.subplots(figsize=(9,5))
#ax.bar(x_pos-0.25, means1, yerr=stads1, align='edge', width=0.2, capsize=7, color='m', label="Toxofilin-Cre")
#ax.bar(x_pos,      means2, yerr=stads2, align='edge', width=0.2, capsize=7, color='c', label="Gra16-Cre")
#ax.bar(x_pos+0.25, means3, yerr=stads3, align='edge', width=0.2, capsize=7, color='#ffea00', label="saline")
ax.bar(x_pos-0.25, means1, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='m', label="Toxofilin-Cre")
ax.bar(x_pos,      means2, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='c', label="Gra16-Cre")
ax.bar(x_pos+0.25, means3, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='#ffea00', label="saline")
ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=13)
plt.legend(prop={'size': 11})
plt.savefig("%s/pic_per_region_counts_group_averages.png"%args.o, transparent=True)


# bar-plot with error bars and all points
fig, ax = plt.subplots(figsize=(9,5))

for i in range(np.shape(data_group1)[0]-1):
    ax.plot(x_pos-0.25+0.1, data_group1[i,1::], 'o', color='m', markeredgecolor='k', markersize=5, alpha=0.7)
ax.bar(x_pos-0.25, means1, yerr=stads1, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='m', label="Toxofilin-Cre")

for i in range(np.shape(data_group2)[0]-1):
    ax.plot(x_pos+0.1, data_group2[i,1::], 'o', color='c', markeredgecolor='k', markersize=5, alpha=0.7)
ax.bar(x_pos,      means2, yerr=stads2, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='c', label="Gra16-Cre")

for i in range(np.shape(data_group3)[0]-1):
    ax.plot(x_pos+0.25+0.1, data_group3[i,1::], 'o', color='#ffea00', markeredgecolor='k', markersize=5, alpha=0.7)
ax.bar(x_pos+0.25, means3, yerr=stads3, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='#ffea00', label="saline")

ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, fontsize=13)
ax.tick_params(axis='y', which='major', labelsize=13)
ax.set_ylim(bottom=0)
plt.legend(prop={'size': 11})
plt.savefig("%s/pic_per_region_counts_group_averages_w_std.png"%args.o, transparent=True)
plt.savefig("%s/pic_per_region_counts_group_averages_w_std.pdf"%args.o, transparent=True)



