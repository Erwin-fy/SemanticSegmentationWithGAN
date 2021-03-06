import torch
import torch.nn as nn
import torch.nn.functional as f
from collections import OrderedDict


class Generator(nn.Module):
    def __init__(self, n_classes, keep_plob = 0.5):
        super(Generator, self).__init__()
        self.n_classes = n_classes
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),

            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1),

            nn.Conv2d(512, 512, kernel_size=3, padding=2, dilation=2),
            nn.ReLU(False),
            nn.Conv2d(512, 512, kernel_size=3, padding=2, dilation=2),
            nn.ReLU(False),
            nn.Conv2d(512, 512, kernel_size=3, padding=2, dilation=2),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        )

        self.fc1 = nn.Sequential(
            nn.Conv2d(512, 1024, kernel_size=3, padding=6, dilation=6),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False),

            nn.Conv2d(1024, 1024, kernel_size=1),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False)
        )

        self.classifiers1 = nn.Conv2d(1024, self.n_classes, kernel_size=1)

        self.fc2 = nn.Sequential(
            nn.Conv2d(512, 1024, kernel_size=3, padding=12, dilation=12),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False),

            nn.Conv2d(1024, 1024, kernel_size=1),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False)
        )
        self.classifiers2 = nn.Conv2d(1024, self.n_classes, kernel_size=1)

        self.fc3 = nn.Sequential(
            nn.Conv2d(512, 1024, kernel_size=3, padding=18, dilation=18),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False),

            nn.Conv2d(1024, 1024, kernel_size=1),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False)
        )
        self.classifiers3 = nn.Conv2d(1024, self.n_classes, kernel_size=1)

        self.fc4 = nn.Sequential(
            nn.Conv2d(512, 1024, kernel_size=3, padding=24, dilation=24),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False),

            nn.Conv2d(1024, 1024, kernel_size=1),
            nn.ReLU(False),
            nn.Dropout(keep_plob, False)
        )
        self.classifiers4 = nn.Conv2d(1024, self.n_classes, kernel_size=1)

    def forward(self, inputs):
        features = self.features(inputs)
        fc1 = self.fc1(features)
        fc2 = self.fc2(features)
        fc3 = self.fc3(features)
        fc4 = self.fc4(features)
        cl1 = self.classifiers1(fc1)
        cl2 = self.classifiers2(fc2)
        cl3 = self.classifiers2(fc3)
        cl4 = self.classifiers2(fc4)
        outputs = cl1 + cl2 + cl3 + cl4

        return outputs


class Discriminator(nn.Module):
    def __init__(self, n_classes, product = False, concat=False):
        super(Discriminator, self).__init__()
        self.n_classes = n_classes
        self.channels = n_classes
        if product:
            self.channels *= 3
        if concat:
            self.channels += 3
        self.features = nn.Sequential(
            nn.Conv2d(self.channels, 96, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(96, 128, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=0),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            # nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=0),


            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(512, 2, kernel_size=3, padding=1),
        )
    
    def forward(self, inputs):
        outputs = self.features(inputs)
        outputs = f.avg_pool2d(outputs, kernel_size=outputs.size()[2]).contiguous()

        # return outputs.view(-1,1).squeeze(1)
        return outputs.view(-1, 2)


class StrongDiscriminator(nn.Module):
    def __init__(self, n_classes, product=False, concat=False):
        super(Discriminator, self).__init__()
        self.n_classes = n_classes
        self.channels = n_classes
        if product:
            self.channels *= 3
        if concat:
            self.channels += 3
        self.features = nn.Sequential(
            nn.Conv2d(self.channels, 96, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(96, 128, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=0),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            # nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=3, stride=1, padding=0),

            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.MaxPool2d(kernel_size=2, stride=2, padding=0),

            nn.Conv2d(512, 1024, kernel_size=3, padding=1),
            nn.ReLU(False),
            nn.Conv2d(1024, 2, kernel_size=3, padding=1),

            # nn.Conv2d(256, 512, kernel_size=3, padding=1),
            # nn.ReLU(False),
            # nn.Conv2d(512, 2, kernel_size=3, padding=1),
        )

    def forward(self, inputs):
        outputs = self.features(inputs)
        outputs = f.avg_pool2d(outputs, kernel_size=outputs.size()[2]).contiguous()

        # return outputs.view(-1,1).squeeze(1)
        return outputs.view(-1, 2)




