import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

def barplot(idx, vals, title, xlab, ylab):
    # generate plot
    # use regex to grab numbers to sort the waves correctly
    fig, ax = plt.subplots(figsize=(15, 6))
    bars = ax.bar(idx, vals, color='skyblue')
    ax.bar_label(bars, fmt='{:,.0f}', padding=5, color='black', fontsize=9)
    ax.set_title(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def boxplot(data, title, xlab, ylab):
    plt.figure(figsize=(8, 8))
    plt.boxplot(data, vert=False, showmeans=True)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.xticks(rotation=45)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:,.0f}'))
    plt.show()

