import matplotlib.pyplot as plt


def barplot(idx, vals, title, xlab, ylab):
    # generate plot
    # use regex to grab numbers to sort the waves correctly
    fig, ax = plt.subplots(figsize=(15, 6))
    bars = ax.bar(idx, vals, color='skyblue')
    ax.bar_label(bars, fmt='{:,.0f}', padding=5, color='black', fontsize=9)
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    plt.tight_layout()
    plt.show()


def boxplot(data, title, ylab):
    plt.figure(figsize=(8, 5))
    plt.boxplot(data, vert=False, showmeans=True)
    plt.title(title)
    plt.ylabel(ylab)
    plt.show()

