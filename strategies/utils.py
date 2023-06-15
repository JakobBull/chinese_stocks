import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_sharpe(returns, stds):
    return np.array(list(returns))/(np.array(list(stds))*(len(list(returns))/12))

def plot_weights(returns, allocations):
    # Create the combined dataframe for heatmap
    df_heatmap = pd.concat(
        [pd.DataFrame(returns, index=["returns"]), allocations.reindex(["stock_1", "stock_2", "stock_3", "stock_4"])]
    )

    # Set the desired column order
    column_order = ["time_1", "time_2", "time_3"]

    # Reorder the columns in the dataframe
    df_heatmap = df_heatmap[column_order]

    # Create the diverging color palettes
    cmap_weights = sns.color_palette("coolwarm", as_cmap=True)
    cmap_returns = sns.color_palette("gray_r", as_cmap=True)

    # Create a grid of subplots
    fig, axes = plt.subplots(nrows=2, figsize=(8, 10), gridspec_kw={'height_ratios': [1, len(column_order)]})

    extreme_val = abs(np.array(list((returns.values())))).max()

    # Plot the heatmap for weights
    sns.heatmap(
        df_heatmap.iloc[:1, :],
        cmap=cmap_weights,
        annot=True,
        fmt=".1f",
        cbar=True,
        ax=axes[0],
        xticklabels=False,
        vmin=-extreme_val,
        vmax=extreme_val
    )
    axes[0].set_title("Portfolio Returns Heatmap")

    # Plot the heatmap for returns
    sns.heatmap(
        df_heatmap.iloc[1:, :],
        cmap=cmap_returns,
        annot=True,
        fmt=".1f",
        cbar=True,
        ax=axes[1],
        vmin=0
    )
    axes[1].set_title("Portfolio Weights Heatmap")

    # Adjust the layout
    plt.tight_layout()
    return fig


def plot_component_returns(returns, component_returns):
    # Create the combined dataframe for heatmap
    df_heatmap = pd.concat(
        [pd.DataFrame(returns, index=["returns"]), component_returns.reindex(["stock_1", "stock_2", "stock_3", "stock_4"])]
    )

    # Set the desired column order
    column_order = ["time_1", "time_2", "time_3"]

    # Reorder the columns in the dataframe
    df_heatmap = df_heatmap[column_order]

    # Create the diverging color palettes
    cmap_weights = sns.color_palette("coolwarm", as_cmap=True)
    cmap_returns = sns.color_palette("coolwarm", as_cmap=True)

    # Create a grid of subplots
    fig, axes = plt.subplots(nrows=2, figsize=(8, 10), gridspec_kw={'height_ratios': [1, len(column_order)]})

    extreme_val = abs(np.array(list((returns.values())))).max()
    component_returns_extreme = abs(component_returns).max().max()
    global_extreme = np.array([extreme_val, component_returns_extreme]).max()

    # Plot the heatmap for weights
    sns.heatmap(
        df_heatmap.iloc[:1, :],
        cmap=cmap_weights,
        annot=True,
        fmt=".1f",
        cbar=True,
        ax=axes[0],
        xticklabels=False,
        vmin=-global_extreme,
        vmax=global_extreme
    )
    axes[0].set_title("Portfolio Returns Heatmap")

    # Plot the heatmap for returns
    sns.heatmap(
        df_heatmap.iloc[1:, :],
        cmap=cmap_returns,
        annot=True,
        fmt=".1f",
        cbar=True,
        ax=axes[1],
        vmin=-global_extreme,
        vmax=global_extreme
    )
    axes[1].set_title("Component Returns Heatmap")

    # Adjust the layout
    plt.tight_layout()
    return fig

weights = {"Stock_1": 0.4, "Stock_2": 0.1, "Stock_3": 0.5}
returns = pd.DataFrame(
{"Stock_1": [1, 2, 3, 4], "Stock_2": [0, 1, 0, 1], "Stock_3": [6, 5, 4, 1]},
index=["time_1", "time_2", "time_3", "time_4"],
)
