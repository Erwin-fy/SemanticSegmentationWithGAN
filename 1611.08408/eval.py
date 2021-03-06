import os
import argparse
import random
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import torch.optim as optim
from torch.autograd import Variable
import torch.nn.functional as f
from reader import *
from models import Generator, Discriminator
from utils import *

os.environ['CUDA_VISIBLE_DEVICES'] = '3'

parser = argparse.ArgumentParser()
parser.add_argument('--batchsize', type=int, default=1, help='input batch size')
parser.add_argument('--nclasses', type=int, default=2, help='number of classes')
parser.add_argument('--niter', type=int, default=20001, help='number of epochs to train for')
parser.add_argument('--lr', type=float, default=1e-3, help='learning rate, default=0.0002')


opt = parser.parse_args()

cudnn.benchmark = True


def main():
    dataReader = DataReader(data_root='/media/Disk/wangfuyu/data/cxr/801/',
                            txt='/media/Disk/wangfuyu/data/cxr/801/testJM_id.txt',
                            batchsize=opt.batchsize, is_train=False)

    G = Generator(n_classes=opt.nclasses)
    G.load_state_dict(torch.load('/media/Disk/wangfuyu/SemanticSegmentationWithGAN/1611.08408/G_step_softmax_20000.pth'))

    D = Discriminator(n_classes=opt.nclasses, product=False)
    D.load_state_dict(torch.load('/media/Disk/wangfuyu/SemanticSegmentationWithGAN/1611.08408/D_step_softmax_20000.pth'))

    D.cuda()
    G.cuda()

    gts_all, predictions_all = [], []

    segs, labels = [], []

    for step in xrange(0, dataReader.length()):
        images, _, ground_truths, _ = dataReader.next()

        imgs = Variable(torch.from_numpy(images).float()).cuda()
        gts = Variable(torch.from_numpy(ground_truths).long()).cuda()

        pred_map = G(imgs)
        pred_map_interp = interp(pred_map.data.max(1)[1].squeeze_(1).cpu().numpy(), zoom=8)
        predictions_all.append(np.squeeze(pred_map_interp.astype(long), axis=0))
        gts_all.append(gts.data.squeeze_(0).cpu().numpy())

        # print D(f.softmax(pred_map)).data.max(1)[1]

    acc, acc_class, iou, _, dice = evaluate(predictions_all, gts_all, 2)
    print acc, acc_class, iou, dice



if __name__ == '__main__':
    main()

