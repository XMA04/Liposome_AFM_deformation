import pandas as pd
from pathlib import Path
import re

# Define folder paths and naming conventions for the alignment process
FOLDER = 'Rd3ns2'
OUTP_FOLDER_ALIGNMENT = 'Rd3ns2_aligned'
PREFIX = 'Rd3ns2_'
SUFFIX = 'pN'
ref_liposome_coord = (-5.82546e-006, 7.82117e-006, 6.5728e-008)  # Reference liposome coordinates in meters

# Ensure the output folder for the alignment process exists
Path(OUTP_FOLDER_ALIGNMENT).mkdir(parents=True, exist_ok=True)

def read_coords_file(file_path):
    # Read a coordinate file from the specified path and return a list of coordinates
    # The file is tab-separated with x, y, z columns
    df = pd.read_csv(file_path, sep='\t', comment='#', names=['x', 'y', 'z'])
    return [tuple(row) for row in df.to_numpy()]

def find_closest_liposome(ref_coord, coords, max_distance=0.2e-6):
    # Find the point in a list of coordinates closest to the reference liposome
    # Distance is calculated in 2D (x, y), ignoring the z-coordinate
    min_distance = max_distance
    closest_coord = None
    for coord in coords:
        # Calculate Euclidean distance in 2D
        distance = ((ref_coord[0] - coord[0])**2 + (ref_coord[1] - coord[1])**2)**0.5
        if distance < min_distance:
            min_distance = distance
            closest_coord = coord
    return closest_coord

def align_coordinates(ref_coord, new_ref_coord, coords):
    # Align all coordinates based on the displacement of the reference liposome
    # Calculates the shift in x and y, then applies this correction to all coordinates
    delta_x = new_ref_coord[0] - ref_coord[0]
    delta_y = new_ref_coord[1] - ref_coord[1]
    return [(x - delta_x, y - delta_y, z) for x, y, z in coords]

# Process each file for alignment
files = sorted(Path(FOLDER).glob(f'{PREFIX}*{SUFFIX}'))
for file in files:
    # Extract the force value from the filename using regex
    force = re.search(f'{PREFIX}(\\d+){SUFFIX}', file.name).group(1)
    print(f'Processing {file.name}...')
    
    coords = read_coords_file(file)
    if ref_liposome_coord:
        # Find the closest liposome to the reference in the current file
        new_ref_coord = find_closest_liposome(ref_liposome_coord, coords, max_distance=0.2e-6)
        if new_ref_coord:
            # Align the coordinates based on the new reference liposome
            aligned_coords = align_coordinates(ref_liposome_coord, new_ref_coord, coords)
            # Save the aligned data
            aligned_df = pd.DataFrame(aligned_coords, columns=['x', 'y', 'z'])
            aligned_df.to_csv(f'{OUTP_FOLDER_ALIGNMENT}/{PREFIX}{force}{SUFFIX}_aligned', sep='\t', index=False, header=False)
            print(f'Saved aligned data for {force}pN.')
        else:
            print(f'Reference liposome not found in {force}pN file.')

