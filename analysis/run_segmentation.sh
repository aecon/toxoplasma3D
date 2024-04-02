#!/bin/bash
set -eu


# ~~~~~~~~~~~ DATA ~~~~~~~~~~~ #
#di=/media/athena-admin/FastSSD/Athena/collabODED/data/01_Toxofilin-Cre
#samples=(4834 4836 4844 4849 4851 4858 4864 4868)
#
#di=/media/athena-admin/FastSSD/Athena/collabODED/data/02_Gra16-Cre
#samples=(4837 4840 4847 4848 4850 4871 4873)
#
#di=/media/athena-admin/FastSSD/Athena/collabODED/data/03_saline
#samples=(4838 4843)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

exit


sides=("left" "right")

for sample in ${samples[@]}; do
for side in ${sides[@]}; do

    input=${di}/${sample}/midres_${side}.nrrd
    outdir=/media/athena-admin/FastSSD/Athena/collabODED/baseline2_NOV21/${sample}_${side}
    mkdir -p "${outdir}"

    Imin=`cat manual_intensities.dat | grep ${sample} | awk '{print $2}'`
    Imax=`cat manual_intensities.dat | grep ${sample} | awk '{print $3}'`
    echo $sample $side $Imin $Imax

    python segmentation.py -i "${input}" -o "${outdir}" -Imin $Imin -Imax $Imax -v -p

    # detele intermediate files
    mkdir -p ${outdir}/bak
    cp ${outdir}/segment/denoised.* $outdir/bak/
    cp ${outdir}/segment/lst.* $outdir/bak/
    rm -rf ${outdir}/segment

done
done
