import os
import numpy as np
from .approximator import PulseApproximator
from .io import parse_cut_peaks_file, load_npz_data
from .plotting import plot_restore

def process_all_peaks(
    peaks_file,
    data_dir,
    plots_dir,
    approximator=None,
    window_length=15,
    stats_filename="stats.txt"
):
    """
    Full workflow: loads peaks file, loads data files, fits pulses, and saves plots/statistics.
    Returns a summary dict.
    """
    if approximator is None:
        approximator = PulseApproximator(window_length=window_length)
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    peaks = parse_cut_peaks_file(peaks_file)
    non_restored_count = 0
    restored_count = 0
    plateu_lengths = []
    for file_path, peak_idx, plateu_l in peaks:
        file_path_clean = file_path.replace('../', '').replace('data_01_11_2017/', '')
        data_fp = os.path.join(data_dir, file_path_clean) if not os.path.isabs(file_path_clean) else file_path_clean
        if not os.path.exists(data_fp):
            print(f"File not found: {data_fp}")
            continue
        try:
            data = load_npz_data(data_fp)
            t = data['time']
            i = data['current']
        except Exception as e:
            print(f"Failed to load {data_fp}: {e}")
            non_restored_count += 1
            continue

        event_start = peak_idx - 30
        event_end = peak_idx + 150
        if event_end - event_start < 5:
            print(f"Event too short for {data_fp}")
            non_restored_count += 1
            continue

        time = t[event_start:event_end]
        current = i[event_start:event_end]
        if len(time) < 3:
            print(f"Pulse window too short in {data_fp}")
            non_restored_count += 1
            continue

        fitted = approximator.approximate(time, current.copy())
        amp_current = np.max(current)
        amp_fitted = np.max(fitted)
        if abs(amp_fitted - amp_current) > 0.01 and amp_fitted < amp_current:
            non_restored_count += 1
            plateu_lengths.append(plateu_l)
            plot_restore(time, current, fitted, data_fp, restored=False, out_dir=plots_dir)
        else:
            restored_count += 1
            plot_restore(time, current, fitted, data_fp, restored=True, out_dir=plots_dir)

    stats_path = os.path.join(plots_dir, stats_filename)
    with open(stats_path, "w") as f:
        f.write(f"Non-restored peaks: {non_restored_count}\n")
        f.write(f"Restored peaks: {restored_count}\n")
        if plateu_lengths:
            f.write(f"Average Plateu Length in Non-restored: {np.mean(plateu_lengths)}\n")
        else:
            f.write("Average Plateu Length in Non-restored: n/a\n")
    print(f"Done. Non-restored: {non_restored_count}, Restored: {restored_count}")
    return {
        "non_restored": non_restored_count,
        "restored": restored_count,
        "average_plateu_length": float(np.mean(plateu_lengths)) if plateu_lengths else None
    }
