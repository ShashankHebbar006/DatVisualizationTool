import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class Plots:
    def __init__(self, df):
        self.df = df
        if not os.path.exists("src/plots"):
            os.makedirs("src/plots")

    def scatter_plot(self, x: str, y: str):
        filename = "plots/scatter_plot.png"
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df[x], self.df[y])
        plt.title(f"Scatter Plot of {x} vs {y}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.savefig(filename)
        plt.close()
        return filename

    def line_plot(self, x: str, y: str):
        filename = "plots/line_plot.png"
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df[x], self.df[y])
        plt.title(f"Scatter Plot of {x} vs {y}")
        plt.xlabel(x)
        plt.ylabel(y)
        plt.savefig(filename)
        plt.close()
        return filename
    
    def bar_plot(self, x: str, y: str = None):
        filename = "plots/bar_plot.png"
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[x])
        plt.title(f"Bar Plot of {x} vs Frequency")
        plt.xlabel(x)
        plt.ylabel("Frequency")
        plt.savefig(filename)
        plt.close()
        return filename
    
    def histogram_plot(self, x: str, y: str = None):
        filename = "plots/histogram_plot.png"
        plt.figure(figsize=(10, 6))
        plt.hist(self.df[x])
        plt.title(f"Histogram of {x} vs Frequency")
        plt.xlabel(x)
        plt.ylabel("Frequency")
        plt.savefig(filename)
        plt.close()
        return filename

    def box_plot(self):
        """
        TO DO
        """
        return "Box Plot"
    
    def heatmap_plot(self, x: str = None, y: str = None):
        filename = "plots/heatmap_plot.png"
        corr_matrix = self.df.corr(numeric_only=True)
        plt.figure(figsize=(15, 10))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
        plt.title(f"Heat map")
        plt.savefig(filename)
        plt.close()
        return filename

    def pair_plot(self):
        """
        TO DO
        """
        return "Pair Plot"
    
    def pie_plot(self):
        """
        TO DO
        """
        return "Pie Plot"
