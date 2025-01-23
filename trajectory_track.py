# Define folder paths and naming conventions for the trajectory extraction process
FOLDER_TRAJECTORIES = 'Rd3ns3_aligned'
OUTP_FOLDER_TRAJECTORIES = 'Rd3ns3_trajs'
THRESHOLD = 100E-9  # 100 nm in meters, used as a criterion for trajectory alignment
VERBOSE = True

suffix = 'pN_aligned'
re_pattern = re.compile(PREFIX + '(\\d+)' + suffix)  # Regular expression to extract force values from filenames

# Ensure the output folder for the trajectory extraction process exists
Path(OUTP_FOLDER_TRAJECTORIES).mkdir(parents=True, exist_ok=True)

# Read and sort the numeric values (force values) from filenames
nums = sorted([int(match.group(1)) for fname in Path(FOLDER_TRAJECTORIES).glob('*') if (match := re_pattern.search(fname.name))])

class Trajectory:
    # A class representing a trajectory, which stores coordinates and tracks in which files it appears
    def __init__(self):
        self.coords = []  # Store coordinates of this trajectory
        self.found_in_files = set()  # Track the force files where this trajectory is found

    def append(self, coord, force):
        # Append a new coordinate along with its corresponding force to the trajectory
        self.coords.append(coord + (force,))
        self.found_in_files.add(force)

class Trajectories:
    # A class to manage multiple trajectories and handle alignment and extraction
    def __init__(self, initial_forces):
        self.trajectories = []  # Store all trajectories
        self.initial_forces = initial_forces  # Force values of the initial three files

    def find_closest_trajectory(self, coord):
        # Find the closest existing trajectory to the given coordinate based on 2D distance
        closest_traj, min_distance = None, THRESHOLD
        for traj in self.trajectories:
            last_coord = traj.coords[-1]
            distance = ((last_coord[0] - coord[0])**2 + (last_coord[1] - coord[1])**2)**0.5
            if distance < min_distance:
                closest_traj, min_distance = traj, distance
        return closest_traj

    def append_coord(self, coord, force):
        # Append a coordinate to the closest trajectory or start a new trajectory
        traj = self.find_closest_trajectory(coord)
        if traj:
            traj.append(coord, force)
        else:
            new_traj = Trajectory()
            new_traj.append(coord, force)
            self.trajectories.append(new_traj)

    def export(self):
        # Export only the trajectories that appear in all of the initial three files
        # Saves each trajectory to a separate CSV file
        for i, traj in enumerate(self.trajectories, 1):
            if traj.found_in_files >= self.initial_forces:
                df = pd.DataFrame(traj.coords, columns=['x', 'y', 'z', 'force'])
                df.to_csv(f"{OUTP_FOLDER_TRAJECTORIES}/{PREFIX}{i}.csv", sep='\t', index=False, header=False)

trajectories = Trajectories(initial_forces)

# Process each file for trajectory extraction
for num in nums:
    fname = f"{FOLDER_TRAJECTORIES}/{PREFIX}{num}{suffix}"
    if VERBOSE:
        print(f'Read coordinates from {fname}')
    coords = read_coords_file(fname)
    for coord in coords:
        trajectories.append_coord(coord, num)  # Append each coordinate to the closest trajectory

# Export trajectory data
trajectories.export()
if VERBOSE:
    print(f'Saved trajectories in folder {OUTP_FOLDER_TRAJECTORIES}')
