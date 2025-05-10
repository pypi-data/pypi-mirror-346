import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

class PulseApproximator:
    def __init__(self, window_length=20):
        self.window_length = window_length

    @staticmethod
    def _find_event_start(current_data, peak_index, threshold_factor=0.1):
        derivative = np.diff(current_data[:peak_index])
        threshold = threshold_factor * np.max(derivative)
        start_candidates = np.where(derivative > threshold)[0]
        if len(start_candidates) > 0:
            start_index = start_candidates[0]
        else:
            start_index = max(0, int(peak_index * 0.9))
        return max(0, start_index)

    @staticmethod
    def _combined_function(t, A, k, lambda_, t_peak):
        sigmoid = np.exp(-k * (t - t_peak))
        exponential = np.where(t > t_peak, np.exp(-lambda_ * (t - t_peak)), 1)
        return A * sigmoid * exponential

    @staticmethod
    def _total(t, A1, A2, k1, k2, l1, l2, t_peak):
        return (
            PulseApproximator._combined_function(t, A1, k1, l1, t_peak) +
            PulseApproximator._combined_function(t, A2, k2, l2, t_peak)
        )

    def _preprocess(self, t, current_data):
        peak_index = np.argmax(current_data)
        peak_value = current_data[peak_index]
        start_index = self._find_event_start(current_data, peak_index)
        zoomed_curr = current_data[start_index:].copy()
        zoomed_time = t[start_index:]
        adjusted_peak_index = peak_index - start_index

        # Plateau + EXTENDED ON BOTH SIDES
        plateau_eps = max(1e-6, 1e-3 * abs(peak_value))
        plateau_mask = np.isclose(zoomed_curr, peak_value, atol=plateau_eps)
        plateau_inds = np.where(plateau_mask)[0]
        if len(plateau_inds) > 0:
            diff = np.diff(plateau_inds)
            splits = np.where(diff > 1)[0]
            starts = np.insert(plateau_inds[splits + 1], 0, plateau_inds[0])
            ends = np.append(plateau_inds[splits], plateau_inds[-1])
            segments = [list(range(start, end+1)) for start, end in zip(starts, ends)]
            plateau_segment = None
            for seg in segments:
                if adjusted_peak_index in seg:
                    plateau_segment = seg
                    break
            if plateau_segment is None:
                plateau_segment = [adjusted_peak_index]
        else:
            plateau_segment = [adjusted_peak_index]
        # Extend one left and one right
        if len(plateau_segment) > 1:
            n = len(plateau_segment)
            excess = 0.01 * peak_value
            for i, idx in enumerate(plateau_segment):
                relpos = i / (n-1) if n > 1 else 0
                triangle = 1.0 - 2 * abs(relpos - 0.5)
                zoomed_curr[idx] = peak_value + triangle * excess

        tail = zoomed_curr[adjusted_peak_index+1:]
        if len(tail) > 5:
            x = np.arange(len(tail))
            y = np.log(np.clip(tail, a_min=1e-10, a_max=None))
            coeffs = np.polyfit(x, y, 1)
            trend = np.exp(np.polyval(coeffs, x))
            detrended = tail - trend
            window_length = min(self.window_length, len(detrended))
            if window_length % 2 == 0:
                window_length -= 1
            if window_length > 2:
                smoothed = savgol_filter(detrended, window_length, 2)
                zoomed_curr[adjusted_peak_index+1:] = smoothed + trend
        t_peak = zoomed_time[adjusted_peak_index]
        return zoomed_time, zoomed_curr, peak_value, t_peak, start_index

    def approximate(self, time, current):
        """
        Fit the current pulse and return fitted current curve with the same size as original.
        Args:
            time: np.array, time axis
            current: np.array, current signal
        Returns:
            fitted_curve: np.array with same length as input 'time'
        """
        zoomed_time, zoomed_curr, peak_value, t_peak, start_index = self._preprocess(time, current)
        try:
            popt, _ = curve_fit(
                lambda t, A1, A2, k1, k2, l1, l2: self._total(t, A1, A2, k1, k2, l1, l2, t_peak),
                zoomed_time,
                zoomed_curr,
                p0=[
                    np.sqrt(peak_value),
                    np.sqrt(peak_value)/2,
                    5, 5, 1, 1
                ],
                maxfev=50000
            )
            fitted_zoomed = self._total(zoomed_time, *popt, t_peak)
        except Exception:
            fitted_zoomed = zoomed_curr.copy()

        if start_index > 0:
            fitted_full = np.concatenate([current[:start_index], fitted_zoomed])
        else:
            fitted_full = fitted_zoomed

        if len(fitted_full) < len(current):
            fitted_full = np.concatenate([fitted_full, current[len(fitted_full):]])
        # Ensure exact length
        fitted_full = fitted_full[:len(current)]
        return fitted_full
