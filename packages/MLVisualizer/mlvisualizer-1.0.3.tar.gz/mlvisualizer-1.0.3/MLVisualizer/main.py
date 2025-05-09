from sklearn import tree
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
from matplotlib.colors import ListedColormap


def DecisionTreeVisualizer(classifier):
    tree.plot_tree(classifier, filled=True)

def ConfusionMatrixVisualizer(cm):
    sns.heatmap(cm, annot=True, cmap="Blues")

def MeshGridVisualizer(classifier=None, x_train=None, y_train=None, x_test=None, y_test=None):
    if x_train is not None and y_train is not None:
        x_set, y_set = x_train, y_train
    else:
        x_set, y_set = x_test, y_test
    cmap = ListedColormap(['purple', 'green'])

    x1, x2 = np.meshgrid(
        np.arange(start=x_set[:, 0].min() - 1, stop=x_set[:, 0].max() + 1, step=0.01),
        np.arange(start=x_set[:, 1].min() - 1, stop=x_set[:, 1].max() + 1, step=0.01)
    )
    plt.contourf(
        x1, x2, classifier.predict(np.array([x1.ravel(), x2.ravel()]).T).reshape(x1.shape),
        alpha=0.75, cmap=cmap
    )
    plt.xlim(x1.min(), x1.max())
    plt.ylim(x2.min(), x2.max())
    for i, j in enumerate(np.unique(y_set)):
        plt.scatter(
            x_set[y_set == j, 0], x_set[y_set == j, 1],
            c=[cmap(i)], label=j
        )

def ScatterPlotVisualizer(x_train=None, y_train=None, x_test=None, y_test=None, x_pred=None):
    if x_train is not None and y_train is not None:
        x_set, y_set = x_train, y_train
    else:
        x_set, y_set = x_test, y_test
    plt.scatter(x_set, y_set, color="green")
    plt.plot(x_train, x_pred, color="red")

def ElbowGraphVisualizer(wcss_list):
    plt.plot(range(1, 11), wcss_list)

def DendrogramVisualizer(data=None):
    shc.dendrogram(shc.linkage(data, method="ward"))

def ClusterVisualizer(data=None, classifier=None, y_pred=None):
    plt.scatter(data[y_pred == 0, 0], data[y_pred == 0, 1], s=100, c='blue', label='Cluster 1')
    plt.scatter(data[y_pred == 1, 0], data[y_pred == 1, 1], s=100, c='green', label='Cluster 2')
    plt.scatter(data[y_pred == 2, 0], data[y_pred == 2, 1], s=100, c='red', label='Cluster 3')
    plt.scatter(data[y_pred == 3, 0], data[y_pred == 3, 1], s=100, c='cyan', label='Cluster 4')
    plt.scatter(data[y_pred == 4, 0], data[y_pred == 4, 1], s=100, c='magenta', label='Cluster 5')
    if classifier and hasattr(classifier, 'cluster_centers_'):
        plt.scatter(classifier.cluster_centers_[:, 0], classifier.cluster_centers_[:, 1], s=300, c='yellow', label='Centroid')


def DBSCANVisualizer(data=None, classifier=None):
    labeling = classifier.labels_

    colours1 = {}
    colours1[0] = 'r'
    colours1[1] = 'g'
    colours1[2] = 'b'
    colours1[3] = 'c'
    colours1[4] = 'y'
    colours1[5] = 'm'
    colours1[-1] = 'k'
    cvec = [colours1[label] for label in labeling]
    colors = ['r', 'g', 'b', 'c', 'y', 'm', 'k']
    r = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[0])
    g = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[1])
    b = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[2])
    c = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[3])
    y = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[4])
    m = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[5])
    k = plt.scatter(data['C1'], data['C2'], marker='o', color=colors[6])
    plt.figure(figsize=(9, 9))
    plt.scatter(data['C1'], data['C2'], c=cvec)
    plt.legend((r, g, b, c, y, m, k),
                ('Label M.0', 'Label M.1', 'Label M.2', 'Label M.3', 'Label M.4', 'Label M.5', 'Label M.-1'),
                scatterpoints=1, loc='upper left', ncol=3, fontsize=10)

def MLP():
    print("""
    class MLP:
    def __init__(self, input_size, h_size, o_size, epochs=10000, lr=0.1):
        self.w1 = np.random.rand(input_size, h_size)
        self.b1 = np.random.rand(1, h_size)
        self.w2 = np.random.rand(h_size, o_size)
        self.b2 = np.random.rand(1, o_size)
        self.epochs = epochs
        self.lr = lr

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_der(self, x):
        return x * (1 - x)

    def predict(self, x):
        h_in = np.dot(x, self.w1) + self.b1
        h_out = self.sigmoid(h_in)
        o_in = np.dot(h_out, self.w2) + self.b2  # Fixed: use h_out, not h_in
        o_out = self.sigmoid(o_in)
        return o_out

    def train(self, x, y):
        for _ in range(self.epochs):
            h_in = np.dot(x, self.w1) + self.b1
            h_out = self.sigmoid(h_in)
            o_in = np.dot(h_out, self.w2) + self.b2
            o_out = self.sigmoid(o_in)

            e_o = y - o_out
            d_o = e_o * self.sigmoid_der(o_out)
            e_h = d_o.dot(self.w2.T)
            d_h = e_h * self.sigmoid_der(h_out)

            self.w1 += x.T.dot(d_h) * self.lr
            self.b1 += np.sum(d_h, axis=0, keepdims=True) * self.lr
            self.w2 += h_out.T.dot(d_o) * self.lr
            self.b2 += np.sum(d_o, axis=0, keepdims=True) * self.lr

def main():
    mlp = MLP(2, 2, 1)
    X = np.array([[0,0],[0,1],[1,0],[1,1]])
    y = np.array([[0],[1],[1],[0]])
    mlp.train(X, y)
    for x in X:
        prediction = mlp.predict(x)
        print(f"Input: {x}, Predicted: {int(round(prediction[0][0]))}") # round to 0 or 1

if __name__ == "__main__":
    main()""")