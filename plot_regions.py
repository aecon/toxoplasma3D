import os
import argparse
import numpy as np
import matplotlib.pyplot as plt


FONT_AXIS_TITLE = 14.5
FONT_LEGEND = 14.5


def plot_regions_per_group(data, regions, group, x_pos, vp, ID):
    Nsamples = len(group)
    dx = 0.1
    x0 = Nsamples*0.1 / 2.

    g = []
    fig, ax = plt.subplots(figsize=(9,5))
    my_cmap = plt.cm.get_cmap('plasma')
    for i,s in enumerate(group):
        idx1 = np.where(data[:,0]==s)[0]
        o = data[idx1,:][0] * vp
        g.append( o )
        print(o)
        ax.bar(x_pos-x0+dx*i, o[1::], width=0.1, edgecolor='k', linewidth=0.5, align='edge', label=s, color=my_cmap(i/len(group)))
    ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=FONT_AXIS_TITLE)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(regions, fontsize=FONT_AXIS_TITLE)
    ax.tick_params(axis='y', which='major', labelsize=FONT_AXIS_TITLE)
    plt.xticks(rotation=0)
    plt.ylim([0,1])
    plt.legend(prop={'size': FONT_LEGEND})
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    plt.savefig("%s/pic_per_region_volume_group%s.eps" % (args.o, ID), transparent=False)
    data_group = np.asarray(g)
    means = np.mean(g, axis=0)[1::]
    stads = np.std( g, axis=0)[1::]
    return data_group, means, stads


def plot_region_percentage_per_group(data, regions, group, x_pos, total_volumes, ID):
    Nsamples = len(group)
    dx = 0.1
    x0 = Nsamples*0.1 / 2.

    g = []
    fig, ax = plt.subplots(figsize=(9,5))
    my_cmap = plt.cm.get_cmap('plasma')
    for i,s in enumerate(group):
        idx1 = np.where(data[:,0]==s)[0]
        o = data[idx1,:][0]
        print(np.shape(o))
        g.append( o )
        print(o)
        ax.bar(x_pos-x0+dx*i, o[1::]/total_volumes*100, width=0.1, edgecolor='k', linewidth=0.5, align='edge', label=s, color=my_cmap(i/len(group)))
    ax.set_ylabel(r'Volume percentage with ZsGreen+ cells', fontsize=FONT_AXIS_TITLE)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(regions, fontsize=FONT_AXIS_TITLE)
    ax.tick_params(axis='y', which='major', labelsize=FONT_AXIS_TITLE)
    plt.xticks(rotation=0)
    #plt.ylim([0,1])
    plt.legend(prop={'size': FONT_LEGEND})
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.tight_layout()
    plt.savefig("%s/pic_per_region_percentage_group%s.eps" % (args.o, ID), transparent=False)
    data_group = np.asarray(g)
    means = np.mean(g, axis=0)[1::]
    stads = np.std( g, axis=0)[1::]
    return data_group, means, stads



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, required=True, help="input file, dat")
    parser.add_argument('-o', type=str, required=True, help="output directory for figures")
    args = parser.parse_args()

    if not os.path.exists(args.o):
        os.makedirs(args.o)

    data = np.loadtxt(args.i, skiprows=1)
    total_volumes = np.loadtxt("ABA_region_volume.dat", skiprows=1)

    dx=6.52*1.e-3
    dz=6.00*1.e-3
    vp = dx*dx*dz

    # Region names
    regions = ["Brain stem", "Hippocampus", "Hypothalamus", "Cortex", "Thalamus"]
    # 01_Toxofilin-Cre
    group1 = [4834, 4836, 4844, 4849, 4851, 4858, 4864, 4868]
    # 02_Gra16-Cre
    group2 = [4837, 4840, 4847, 4848, 4850, 4871, 4873]
    # 03_saline
    group3 = [4838, 4843]

    Nc = np.shape(data)[1]
    x_pos = np.arange(len(regions))


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Plot all samples per GROUP
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Plot volumes per sample per region, in mm3
    data_group1, means1, stads1 = plot_regions_per_group(data, regions, group1, x_pos, vp, ID="1-TOXO")
    data_group2, means2, stads2 = plot_regions_per_group(data, regions, group2, x_pos, vp, ID="2-Gra16")
    data_group3, means3, stads3 = plot_regions_per_group(data, regions, group3, x_pos, vp, ID="3-SALINE")
    # Plot Vcells/Vregion * 100
    data_group1, means1, stads1 = plot_region_percentage_per_group(data, regions, group1, x_pos, total_volumes, ID="1-TOXO")
    data_group2, means2, stads2 = plot_region_percentage_per_group(data, regions, group2, x_pos, total_volumes, ID="2-Gra16")
    data_group3, means3, stads3 = plot_region_percentage_per_group(data, regions, group3, x_pos, total_volumes, ID="3-SALINE")



    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Plot group AVERAGES
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # Group volume averages, only means
    # fig, ax = plt.subplots(figsize=(9,5))
    # #ax.bar(x_pos-0.25, means1, yerr=stads1, align='edge', width=0.2, capsize=7, color='m', label="Toxofilin-Cre")
    # #ax.bar(x_pos,      means2, yerr=stads2, align='edge', width=0.2, capsize=7, color='c', label="Gra16-Cre")
    # #ax.bar(x_pos+0.25, means3, yerr=stads3, align='edge', width=0.2, capsize=7, color='#ffea00', label="saline")
    # ax.bar(x_pos-0.25, means1, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='m', label="Toxofilin-Cre")
    # ax.bar(x_pos,      means2, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='c', label="Gra16-Cre")
    # ax.bar(x_pos+0.25, means3, align='edge', width=0.2, edgecolor='k', linewidth=0.5, color='#ffea00', label="saline")
    # ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=13)
    # ax.set_xticks(x_pos)
    # ax.set_xticklabels(regions, fontsize=13)
    # ax.tick_params(axis='y', which='major', labelsize=13)
    # plt.legend(prop={'size': 11})
    # plt.savefig("%s/pic_per_region_volume_group_averages.png"%args.o, transparent=True)



    # Group volume averages: means, stds, all points
    fig, ax = plt.subplots(figsize=(10,5))
    for i in range(np.shape(data_group1)[0]-1):
        ax.plot(x_pos-0.25+0.1, data_group1[i,1::], 'o', color='m', markeredgecolor='k', markersize=5, alpha=0.7)
    ax.bar(x_pos-0.25, means1, yerr=stads1, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='m', label="Toxofilin-Cre")
    for i in range(np.shape(data_group2)[0]-1):
        ax.plot(x_pos+0.1, data_group2[i,1::], 'o', color='c', markeredgecolor='k', markersize=5, alpha=0.7)
    ax.bar(x_pos,      means2, yerr=stads2, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='c', label="Gra16-Cre")
    for i in range(np.shape(data_group3)[0]-1):
        ax.plot(x_pos+0.25+0.1, data_group3[i,1::], 'o', color='#ffea00', markeredgecolor='k', markersize=5, alpha=0.7)
    ax.bar(x_pos+0.25, means3, yerr=stads3, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='#ffea00', label="saline")

    ax.set_ylabel(r'Cell volume ($mm^3$)', fontsize=FONT_AXIS_TITLE)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(regions, fontsize=FONT_AXIS_TITLE)
    ax.tick_params(axis='y', which='major', labelsize=FONT_AXIS_TITLE)
    ax.set_ylim(bottom=0)
    plt.legend(prop={'size': FONT_LEGEND})
    plt.savefig("%s/pic_per_region_volume_group_averages_w_std.eps"%args.o, transparent=False)



    # Group volume PERCENTAGE averages: means, stds, all points
    fig, ax = plt.subplots(figsize=(10,5))
    for i in range(np.shape(data_group1)[0]-1):
        ax.plot(x_pos-0.25+0.1, data_group1[i,1::]/total_volumes*100, 'o', color='m', markeredgecolor='k', markersize=5, alpha=0.7)
    ax.bar(x_pos-0.25, means1/total_volumes*100, yerr=stads1/total_volumes*100, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='m', label="Toxofilin-Cre")
    for i in range(np.shape(data_group2)[0]-1):
        ax.plot(x_pos+0.1, data_group2[i,1::]/total_volumes*100, 'o', color='c', markeredgecolor='k', markersize=5, alpha=0.7)
    ax.bar(x_pos,      means2/total_volumes*100, yerr=stads2/total_volumes*100, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='c', label="Gra16-Cre")
    for i in range(np.shape(data_group3)[0]-1):
        ax.plot(x_pos+0.25+0.1, data_group3[i,1::]/total_volumes*100, 'o', color='#ffea00', markeredgecolor='k', markersize=5, alpha=0.7)
    ax.bar(x_pos+0.25, means3/total_volumes*100, yerr=stads3/total_volumes*100, align='edge', width=0.2, capsize=7, edgecolor='k', linewidth=0.5, color='#ffea00', label="saline")

    ax.set_ylabel(r'Volume percentage with ZsGreen+ cells', fontsize=FONT_AXIS_TITLE)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(regions, fontsize=FONT_AXIS_TITLE)
    ax.tick_params(axis='y', which='major', labelsize=FONT_AXIS_TITLE)
    ax.set_ylim(bottom=0)
    plt.legend(prop={'size': FONT_LEGEND})
    plt.savefig("%s/pic_per_region_percentage_group_averages_w_std.eps"%args.o, transparent=False)


