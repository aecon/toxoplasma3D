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

    input=`ls ${di}/${sample}/midres_${side}.nrrd`
    echo "input: $input"
    truecells=/media/athena-admin/FastSSD/Athena/collabODED/baseline2_NOV21/${sample}_${side}/bak/cells.nrrd
    outdir=/media/athena-admin/FastSSD/Athena/collabODED/baseline2_NOV21/${sample}_${side}/align
    mkdir -p "${outdir}"

    echo $sample $side

    ox=`awk 'BEGIN { print ARGV[1] ~ /_left\.nrrd$/ ? 1 : -1}' "$input"`
    echo $input $ox
    ( 
    cd ../
    python3.6 align.py -i ${input} -o ${outdir} -k 1 1 1 -d 6.52 6.52 6.00 -azmin 0 -azmax 230 -ori $ox 2 3 -N 32 -truecells ${truecells} -affine data/affine.txt -bspline data/bspline.txt -v
    rm -rf ${outdir}/stitched.npy
    )

done
done
