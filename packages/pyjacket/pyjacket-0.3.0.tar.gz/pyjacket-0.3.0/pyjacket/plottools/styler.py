import matplotlib.pyplot as plt
import matplotlib as mpl
import copy
import os
from matplotlib.axes import Axes

class style:
    def __init__(self, name: str):
        self.name = name
        self.before = None

    def __enter__(self):
        self.before = copy.deepcopy(mpl.rcParams)
        self.use(self.name)

    def __exit__(self, exc_type, exc_value, traceback):
        mpl.rcParams.update(self.before)

    @classmethod
    def use(self, name: str):
        file_path = os.path.join(os.path.dirname(__file__), 'styles', f'{name.lower()}.mplstyle')
        plt.style.use(file_path)


if __name__ == "__main__":
    import numpy as np

    def main():
        ROOT = r'C:\Users\arfma005\Documents\GitHub\pyjacket\pyjacket\plottools\styles'
        plt.style.use(f"{ROOT}\sprakel.mplstyle")
        test_plot()

    def test_plot():
        nrows, ncols = 2, 2
        base_figsize = (4, 3)  # Width x Height per subplot
        figsize = (base_figsize[0] * ncols, base_figsize[1] * nrows)
        ax0: Axes
        ax1: Axes
        ax2: Axes
        ax3: Axes
        fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2, figsize=figsize)

        # Plot
        if True:
            labels = [f'sample {i}' for i in range(1, 8+1)]
            L = np.linspace(0, 25, len(labels))
            x = np.linspace(0, 10, 101)[:, np.newaxis]
            y = (100 - L) / (1 + np.exp(x - 5 + 2*L/100)) + L/2
            # ax0.set_title('Panel 1: Line Plot')
            ax0.plot(x, y, label=labels)
            ax0.set_xlabel('${t}$ [${ms}$]')
            ax0.set_ylabel('${h}$ [${\mu m}$]')
            ax0.legend()

        # Scatter
        if True:
            labels = [f'sample {i}' for i in range(1, 4+1)]
            k = np.geomspace(10, 100, len(labels))[:, np.newaxis]  # (3, 1)
            x = np.geomspace(1, 1000, 11)  # (11,)
            xfit = np.geomspace(1, 1000, 101) # (101,)

            def model(k: np.ndarray, x: np.ndarray):
                return x / (k + x)
            
            yfit = model(k, xfit)  # (3, 101)
            meas = model(k, x)  # (3, 11)
            meas += np.random.normal(loc=0.0, scale=0.03, size=meas.shape)
            meas[meas < 0] = 0  # Disable negative numbers

            # ax1.set_title('Panel 2: Scatter with guidelines')
            for line, label in zip(meas, labels):
                ax1.scatter(x, line, label=label)
            ax1.plot(xfit, yfit.T, linestyle='--')
            ax1.set_xlabel(r'${c}$ [${\mu M}$]')
            ax1.set_ylabel(r'${\theta}$ [-]')
            ax1.set_xscale('log')
            ax1.legend()

        # Image
        if True:
            from skimage import data
            img = data.astronaut()
            img = data.coins()  # (303, 384)

            # ax2.set_title('Panel 3: Imshow')
            ax2.set_axis_off()
            ax2.imshow(img)

        # Hist
        if True:
            labels = [f'sample {i}' for i in range(1, 5+1)]
            centers = np.linspace(40, 70, len(labels))
            freqs = [np.random.normal(c, 3, 301) for c in centers]

            # ax3.set_title('Panel 4: Histogram')
            for arr, label in zip(freqs, labels):
                ax3.hist(arr, density=False, label=label, alpha=0.75)

            ax3.set_xlabel(r'${\tau}$ [${\mu s}$]')
            ax3.set_ylabel('n [${-}$]')
            # ax3.set_xlim([40, None])
            ax3.legend()

            # freqs = np.random.normal(60, 3, 301)
            # ax3.hist(freqs)

        
        plt.show()


    main()