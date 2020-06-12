import sys
import os

from sklearn import clone, datasets
from sklearn.datasets import make_circles, make_moons, make_blobs
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
import pandas as pd
import numpy as np

from fexin import Gexin


def main():
    results_dir = "./results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    n_samples = 500
    noisy_circles = make_circles(n_samples=n_samples, factor=.5,
                                 noise=.05)
    noisy_moons = make_moons(n_samples=n_samples, noise=.05)
    blobs = make_blobs(n_samples=n_samples, random_state=8)
    no_structure = np.random.rand(n_samples, 2), None
    random_state = 170
    X, y = make_blobs(n_samples=n_samples, random_state=random_state)
    transformation = [[0.6, -0.6], [-0.4, 0.8]]
    X_aniso = np.dot(X, transformation)
    aniso = (X_aniso, y)
    varied = make_blobs(n_samples=n_samples,
                        cluster_std=[1.0, 2.5, 0.5],
                        random_state=random_state)

    datasets = {
        "noisy_circles": noisy_circles,
        "noisy_moons": noisy_moons,
        "blobs": blobs,
        # "no_structure": no_structure,
        "aniso": aniso,
        "varied": varied,
    }

    bar_position = 0
    progress_bar = tqdm(datasets.items(), position=bar_position)
    for dataset, data in progress_bar:
        progress_bar.set_description("Analysis of dataset: %s" % dataset)
        X, y = data
        X = StandardScaler().fit_transform(X)

        N = 20
        model = Gexin(verbose=False)
        model.fit(X, N=N, num_epochs=400, lr=0.01)
        model.compute_sample_graph()
        model.compute_graph()
        # model.plot_adjacency_matrix()
        model.plot_graph(y, os.path.join(results_dir, f"{dataset}.png"))
        model.plot_sample_graph(y, os.path.join(results_dir, f"{dataset}_samples.png"))
        # pd.DataFrame(model.adjacency_matrix_).to_csv(os.path.join(results_dir, f"{dataset}.csv"))
        # pd.DataFrame(model.centroids_).to_csv(os.path.join(results_dir, f"{dataset}_centroids.csv"))
        # pd.DataFrame(model.adjacency_samples_).to_csv(os.path.join(results_dir, f"{dataset}_samples.csv"))


if __name__ == "__main__":
    sys.exit(main())