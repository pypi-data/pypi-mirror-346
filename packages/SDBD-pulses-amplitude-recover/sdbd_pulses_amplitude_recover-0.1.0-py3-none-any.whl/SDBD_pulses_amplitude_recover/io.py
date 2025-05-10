import numpy as np

def parse_cut_peaks_file(filename):
    """
    Returns a list of tuples: (filename, peak_index, plateau_length)
    """
    peaks = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.lower().startswith('filename'):
                fname, idx, pl = line.split(",")
                peaks.append((fname.strip(), int(idx), int(pl)))
    return peaks

def load_npz_data(file_path):
    """
    Loads .npz files assumed to contain a `data` array. Returns dict with keys 'time','voltage','current'
    """
    npz = np.load(file_path)
    data = npz['data']
    return dict(time=data[0], voltage=data[1], current=data[2])
