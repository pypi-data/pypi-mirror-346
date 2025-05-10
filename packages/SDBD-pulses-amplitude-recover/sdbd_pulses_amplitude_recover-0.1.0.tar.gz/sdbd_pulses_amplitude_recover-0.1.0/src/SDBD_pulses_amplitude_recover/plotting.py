import os
import matplotlib.pyplot as plt

def plot_restore(time, current, fitted, filename, restored, out_dir):
    """
    Plots and saves the original and fitted current curves.
    """
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    plt.figure(figsize=(8,6))
    plt.plot(time, current, label="Original current", color='blue')
    plt.plot(time, fitted, label="Fitted pulse", color='red', linestyle='--')
    plt.xlabel("Time")
    plt.ylabel("Current")
    plt.legend()
    plt.title(f"{os.path.basename(filename)} - {'Restored' if restored else 'Not restored'}")
    out_name = os.path.splitext(os.path.basename(filename))[0]
    status = "restored" if restored else "not_restored"
    out_file = os.path.join(out_dir, f"{out_name}_{status}.png")
    plt.savefig(out_file, dpi=150)
    plt.close()
