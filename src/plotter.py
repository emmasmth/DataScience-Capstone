import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

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

def plot_regression_results(y_test, preds, r2, mae, is_log=False, title="Model Results"):
    # Convert back if log model (net worth)
    if is_log:
        y_actual = np.expm1(y_test)
        preds_actual = np.expm1(preds)
    else:
        y_actual = y_test
        preds_actual = preds

    plt.figure(figsize=(6, 6))
    plt.scatter(y_actual, preds_actual, alpha=0.3)

    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title(f"{title}: Actual vs Predicted")
    plt.text(
        0.05, 0.95,
        f"R² = {r2:.3f}\nMAE = {mae:,.2f}",
        transform=plt.gca().transAxes,
        verticalalignment='top'
    )

    # Perfect prediction line
    min_val = min(y_actual.min(), preds_actual.min())
    max_val = max(y_actual.max(), preds_actual.max())

    plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")

    if is_log:
        plt.xscale('log')
        plt.yscale('log')

    plt.tight_layout()
    plt.show()

    # Residuals
    residuals = y_actual - preds_actual

    plt.figure(figsize=(6, 4))
    plt.scatter(preds_actual, residuals, alpha=0.3)

    plt.axhline(0, linestyle="--")

    plt.xlabel("Predicted")
    plt.ylabel("Residuals")
    plt.title(f"{title}: Residual Plot")

    plt.tight_layout()
    plt.show()