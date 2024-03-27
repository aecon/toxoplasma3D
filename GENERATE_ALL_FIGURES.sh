#!/bin/bash
set -eu

base0="/media/neptun/LocalDisk16TB/Athena/Bracha_et_al_accepted_032024/paper_data/3D_mouse_brain_data"
#base0="3D_mouse_brain_data"
samples0=(4834 4836 4844 4849 4851 4858 4864 4868 4837 4840 4847 4848 4850 4871 4873 4838 4843)

# SAMPLE COHORTS
# 01_Toxofilin-Cre
samples1=(4834 4836 4844 4849 4851 4858 4864 4868)
# 02_Gra16-Cre
samples2=(4837 4840 4847 4848 4850 4871 4873)
# 03_saline
samples3=(4838 4843)

atlas="${base0}/ABA_atlas/ABA_25um_reference.tif"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Coronal slices of cell volume, per sample
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

odir1="plots_coronal_slices_per_brain"
mkdir -p $odir1

# for sample in ${samples0[@]}; do
#     mc="${base0}/${sample}/merged_transformed_cells.nrrd"
#     mv="${base0}/${sample}/merged_voxelized.nrrd"
#     
#     python3 coronal_per_sample.py -i $mc -s $sample -on "real" -a $atlas -od $odir1
#     python3 coronal_per_sample.py -i $mv -s $sample -on "blur" -a $atlas -od $odir1
# done



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Montage: Group coronal views into one picture
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
odir2=plots_montage
mkdir -p $odir2

# # REAL CELL LOCATIONS
# files=""
# counter=0
# for s in ${samples1[@]}; do
#     files="$files ${odir1}/pic_density_coronal_real_${s}.png"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir2}/pic_coronal_samples_montage_G1-TOXO_real.png
# 
# files=""
# counter=0
# for s in ${samples2[@]}; do
#     files="$files ${odir1}/pic_density_coronal_real_${s}.png"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir2}/pic_coronal_samples_montage_G2-Gra16_real.png
# 
# files=""
# counter=0
# for s in ${samples3[@]}; do
#     files="$files ${odir1}/pic_density_coronal_real_${s}.png"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir2}/pic_coronal_samples_montage_G3-SAL_real.png
# 
# 
# # BLURRIED DATA / "VOXELIZED"
# files=""
# counter=0
# for s in ${samples1[@]}; do
#     files="$files ${odir1}/pic_density_coronal_blur_${s}.png"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir2}/pic_coronal_samples_montage_G1-TOXO_blur.png
# 
# files=""
# counter=0
# for s in ${samples2[@]}; do
#     files="$files ${odir1}/pic_density_coronal_blur_${s}.png"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir2}/pic_coronal_samples_montage_G2-Gra16_blur.png
# 
# files=""
# counter=0
# for s in ${samples3[@]}; do
#     files="$files ${odir1}/pic_density_coronal_blur_${s}.png"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir2}/pic_coronal_samples_montage_G3-SAL_blur.png



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Average distribution per group
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
odir3=plots_coronal_slices_average_density
mkdir -p $odir3


# files=""
# counter=0
# for s in ${samples1[@]}; do
#     files="$files $base0/${s}/merged_voxelized.nrrd"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# echo "Files:" $files
# echo "Number of files:" $counter
# python3 plot_avg_density.py -i $files -on "blur" -o ${odir3} -g 1 -of ${odir3} -a $atlas
# 
# files=""
# counter=0
# for s in ${samples2[@]}; do
#     files="$files $base0/${s}/merged_voxelized.nrrd"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# echo "Files:" $files
# echo "Number of files:" $counter
# python3 plot_avg_density.py -i $files -on "blur" -o ${odir3} -g 2 -of ${odir3} -a $atlas
# 
# files=""
# counter=0
# for s in ${samples3[@]}; do
#     files="$files $base0/${s}/merged_voxelized.nrrd"
#     counter=`awk -v c=$counter 'BEGIN {print c+1}'`
# done
# echo "Files:" $files
# echo "Number of files:" $counter
# python3 plot_avg_density.py -i $files -on "blur" -o ${odir3} -g 3 -of ${odir3} -a $atlas
# 
# 
# # MONTAGE
# files=`ls ${odir3}/pic_density_coronal_AVG_g?_*.png`
# counter=3
# echo $files
# montage $files -geometry +0+0 -tile 1x"${counter}" ${odir3}/pic_density_coronal_AVG_montage_blur.png




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Statistics per region
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Generate ABA regions label mask
odir4="ABA_regions"
mkdir -p $odir4
# python regions_ABA.py -o "${odir4}/labeled_regions.nrrd"
# 
# # Compute total cell volume per labeled brain region
# files=`ls ${base0}/*/merged_transformed_cells.nrrd`
# for f in ${files[@]}; do
#     echo "Computing total cell volume per brain region for file:" $f
#     s0=`dirname $f`
#     s=`basename $s0`
#     o=${odir4}/${s}_volume_per_region.dat
#     python region_volumes.py -i ${f} -r "${odir4}/labeled_regions.nrrd" -o ${o} -s ${s}
# done

# Collect all region volumes from all brains
files=`ls ${odir4}/*_volume_per_region.dat`
o="volume_per_region_allSamples.dat"
printf "%10s %25s %25s %25s %25s %25s\n" 'Sample' 'Brain stem' 'Hippocampus' 'Hypothalamus' 'Cortex' 'Thalamus' > $o
for f in ${files[@]}; do
    tail -n 1 $f >> $o
done

# Plot region statistics
o2=plots_statistics_2023Mar27
python3 plot_regions.py -i ${o} -o ${o2}

