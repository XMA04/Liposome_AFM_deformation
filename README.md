# Liposome_AFM_deformation
To track liposome deformation under varying forces in AFM
## Overview

This repository contains two scripts for processing and analyzing coordinate data from AFM experiments:  
1. **Coordinate Alignment**: Aligns coordinate files based on a reference liposome.  
2. **Trajectory Tracking**: Tracks trajectories by linking coordinates across multiple aligned files.

The scripts are designed to facilitate the analysis of liposome deformation under varying forces.
---

## File Structure

- `coordinate_alignment.py`: Script for aligning coordinates based on a reference liposome.  
- `trajectory_track.py`: Script for identifying and exporting liposome trajectories.  
- `Rd3ns2/`: Input folder containing raw coordinate data for alignment.  
- `Rd3ns2_aligned/`: Output folder for aligned coordinate data.  
- `Rd3ns3_aligned/`: Input folder containing aligned coordinate data for trajectory tracking.  
- `Rd3ns3_trajs/`: Output folder for trajectory files.

---

## Coordinate Alignment

### Description
This script processes raw coordinate files, aligning all coordinates based on the displacement of a reference liposome.

### Key Parameters
- **FOLDER**: Path to the input folder containing raw coordinate files (default: `Rd3ns2/`).
- **OUTP_FOLDER_ALIGNMENT**: Path to the output folder for aligned data (default: `Rd3ns2_aligned/`).
- **PREFIX**: Prefix for input filenames (default: `Rd3ns2_`).
- **SUFFIX**: Suffix for input filenames (default: `pN`).
- **ref_liposome_coord**: Coordinates of the reference liposome (default: `(-5.82546e-006, 7.82117e-006, 6.5728e-008)`).

### Output
Aligned coordinate files are saved in the `OUTP_FOLDER_ALIGNMENT` directory.

---

## Trajectory Tracking

### Description
This script processes aligned coordinate files to identify and track trajectories of liposomes across multiple files.

### Key Parameters
- **FOLDER_TRAJECTORIES**: Path to the input folder containing aligned coordinate files (default: `Rd3ns3_aligned/`).
- **OUTP_FOLDER_TRAJECTORIES**: Path to the output folder for trajectory data (default: `Rd3ns3_trajs/`).
- **THRESHOLD**: Distance threshold (in meters) for linking coordinates to trajectories (default: `100E-9`).
- **VERBOSE**: Boolean flag for detailed logging (default: `True`).

### Output
Each trajectory is saved as a separate CSV file in the `OUTP_FOLDER_TRAJECTORIES` directory.

---

## How to Run

1. Ensure Python and required libraries (`pandas`, `pathlib`, `re`) are installed.  
2. Place the raw coordinate files in the `Rd3ns2/` folder.  
3. Run the **Coordinate Alignment** script:
   ```bash
   python coordinate_alignment.py
   ```
4. Place the aligned files in the `Rd3ns3_aligned/` folder.  
5. Run the **Trajectory Tracking** script:
   ```bash
   python trajectory_track.py
   ```

---

## Notes
- Ensure input files follow the expected naming convention (`<PREFIX><force><SUFFIX>`).
- Adjust parameters as needed for your dataset and experimental conditions.
- For additional details, consult the comments in each script.

--- 
