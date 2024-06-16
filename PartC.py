import matplotlib.pyplot as plt
import numpy as np

# Data from MySQL database
techniques = ["RSA", "DES", "AES"]
# SELECT AVG(rsa.generation_time), AVG(des.generation_time), AVG(aes.generation_time) FROM rsa, des, aes;
avg_generation_time = [0.29325703667000, 0.00029324001000, 0.00021503665333]
success_times = [30, 30, 30]
fail_times = [0, 0, 0]

if __name__ == "__main__":
    # Creating a figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), num="Comparison of encryption techniques")

    # Subplot 1: Bar chart for average generation time
    bars1 = ax1.bar(techniques, avg_generation_time, color=["blue", "yellow", "purple"])
    ax1.set_xlabel("Encryption Techniques")
    ax1.set_ylabel("Average Generation Time (seconds)")
    ax1.set_title("Average Generation Time Comparison")
    ax1.set_yscale("log")
    ax1.set_yticks([1e-4, 1e-3, 1e-2, 1e-1, 1])
    ax1.set_yticklabels([0.0001, 0.001, 0.01, 0.1, 0.5])

    # Adding labels to bars in the first subplot
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            round(yval, 10),
            ha="center",
            va="bottom",
        )

    # Subplot 2: Grouped bar chart for success and fail times
    bar_width = 0.35
    index = np.arange(len(techniques))

    bars2 = ax2.bar(index, success_times, bar_width, label="Success Times", color="green")
    bars3 = ax2.bar(
        index + bar_width, fail_times, bar_width, label="Fail Times", color="red"
    )

    ax2.set_xlabel("Encryption Techniques")
    ax2.set_ylabel("Count")
    ax2.set_title("Success and Fail Times Comparison")
    ax2.set_xticks(index + bar_width / 2)
    ax2.set_xticklabels(techniques)
    ax2.legend()

    # Adding labels to bars in the second subplot
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2, yval, int(yval), ha="center", va="bottom"
        )

    for bar in bars3:
        yval = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2, yval, int(yval), ha="center", va="bottom"
        )

    # Display the combined plot
    plt.tight_layout()
    plt.show()