import numpy as np

def find_event_start(current_data, peak_index, threshold_factor=0.1):
    derivative = np.diff(current_data[:peak_index])
    if len(derivative) == 0:
        return 0
    threshold = threshold_factor * np.max(derivative)
    start_candidates = np.where(derivative > threshold)[0]
    if len(start_candidates) > 0:
        start_index = start_candidates[0]
    else:
        start_index = max(0, int(peak_index * 0.9))
    return max(0, start_index)

def find_event_end(current_data, peak_index, threshold_factor=0.1, extra_points=20):
    derivative = np.diff(current_data[peak_index:])
    if len(derivative) == 0:
        return len(current_data)-1
    threshold = threshold_factor * np.max(derivative)
    end_candidates = np.where(derivative < -threshold)[0]
    if len(end_candidates) > 0:
        end_index = peak_index + end_candidates[0]
    else:
        end_index = min(len(current_data)-1, int(peak_index + (len(current_data)-peak_index)*0.1))
    end_index = min(len(current_data)-1, end_index + extra_points)
    return end_index
