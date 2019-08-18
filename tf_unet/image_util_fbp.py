from image_util import ImageDataProvider
import scipy.io as sio
import numpy as np


class MatDataProvider(ImageDataProvider):
    def __init__(self, path, a_min=None, a_max=None,
                 data_suffix=".mat", shuffle_data=True):
        super(ImageDataProvider, self).__init__(a_min, a_max)
        self.data_suffix = data_suffix
        self.file_idx = -1
        self.step = 1
        self.shuffle_data = shuffle_data

        self.data_file = path

        image_path = self.data_file
        self.input = self._load_file(image_path, 'sparse')
        self.output = self._load_file(image_path, 'label')
        self.channels = 1
        self.n_class = 1

        print("Number of channels: %s" % self.channels)
        print("Number of classes: %s" % self.n_class)

    def _load_file(self, path, opt, dtype=np.float32):
        mat_contents = sio.loadmat(path)
        # convert HWCN to NHWC format
        data = np.transpose(mat_contents[opt], (3, 0, 1, 2))
        print(data.shape)
        return data

    def len(self):
        return self.input.shape[0]

    def _cylce_file(self):
        self.file_idx += self.step
        if self.file_idx >= self.len():
            self.file_idx = 0

    def _next_data(self):
        self._cylce_file()
        inp = self.input[self.file_idx:self.file_idx + self.step]
        out = self.output[self.file_idx:self.file_idx + self.step]

        return inp, out

    def _load_data_and_label(self):
        data, label = self._next_data()

        # Disable normalization
        # train_data = self._process_data(data)
        # labels = self._process_data(label)
        train_data = data
        labels = label

        train_data, labels = self._post_process(train_data, labels)

        return train_data, labels,


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np

    import sys
    sys.path.append('.')

    from tf_unet import image_util_fbp
    from tf_unet import unet
    from tf_unet import util

    generator = image_util_fbp.MatDataProvider(
            '../fbpconv_tf/data/train_elips.mat')

    x_test, y_test = generator(1)
    net = unet.Unet(channels=generator.channels,
                    n_class=generator.n_class,
                    cost="euclidean",
                    layers=5, features_root=32)
    trainer = unet.Trainer(net,
                           optimizer="adam",
                           batch_size=1,
                           verification_batch_size=1,
                           opt_kwargs=dict(learning_rate=0.0001))
    path = trainer.train(generator,
                         "./unet_trained",
                         training_iters=generator.len(),
                         epochs=100,
                         display_step=2,
                         restore=True)
