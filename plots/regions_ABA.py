import os
import nrrd
import argparse
import skimage.io
import numpy as np
from pathlib import Path
from allensdk.core.reference_space_cache import ReferenceSpaceCache


def generate_region_mask(brain_regions, resolution=25, is_half_brain=False):
    print("Downloading atlas...")
    reference_space_key = os.path.join('annotation', 'ccf_2017')

    # Load Reference Space
    odir = "tmp"
    rspc = ReferenceSpaceCache(resolution, reference_space_key, manifest=Path(odir) / 'manifest.json')
    tree = rspc.get_structure_tree(structure_graph_id=1) 

    # Get brain region IDs
    print("Retrieving region IDs...")
    main_brain_region_IDs = []
    for _region in brain_regions:
    	_structure = tree.get_structures_by_name([_region])
    	#print('\n', _structure)
    	main_brain_region_IDs.append(_structure[0]['id'])
    print('Main brain region IDs:', main_brain_region_IDs)

    # Download annotation volume
    annotation, meta = rspc.get_annotation_volume()

    # Construct ReferenceSpace
    rsp = rspc.get_reference_space()

    # Remove unassigned structures
    rsp.remove_unassigned()

    # Generate mask for each brain region
    print("Generating masks...")
    all_masks = []
    for _id in main_brain_region_IDs:
    	_mask = rsp.make_structure_mask([_id])
    	all_masks.append(_mask)

    # Reorient masks to saggital ABA view
    reshaped_masks = []
    for _mask in all_masks:
        Nx, Ny, Nz = np.shape(_mask)   #(528, 320, 456
        if is_half_brain==True:
            Nz = Nz//2
        _tmp = np.zeros((Ny, Nx, Nz))
        for k in range(Nz):
            _tmp[:,:,k] = (_mask[:,:,k]).T
        reshaped_masks.append(_tmp)

    # Exclude masked brain regions
    all_areas = np.zeros(np.shape(reshaped_masks[0]))
    for i, _mask in enumerate(reshaped_masks):
        all_areas[_mask==1] = i+1

    return all_areas



# Brain regions for quantification (using ABA IDs) # see http://atlas.brain-map.org/atlas?atlas=2
brain_regions = ['Hindbrain', 'Hippocampal formation', 'Hypothalamus', 'Isocortex', 'Thalamus'] # exclude 'Cerebellum'


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', type=str, required=True, help="path to output file, nrrd")
    args = parser.parse_args()

    resolution = 25

    selected_regions = generate_region_mask(brain_regions, resolution)

    nrrd.write(args.o, selected_regions)

    # Save total volume per region in pixels
    total_volumes = np.zeros(len(brain_regions))
    for i in range(len(brain_regions)):
        print(i)
        print(np.shape(selected_regions))
        total_volumes[i] = np.sum(selected_regions==i+1)

    with open("ABA_region_volume.dat", 'w') as f:
        for br in brain_regions:
            f.write("%25s " % br)
        f.write("\n")
        for volume in total_volumes:
            f.write("%25d " % volume)
        f.write("\n")


