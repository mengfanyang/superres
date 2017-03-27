
from PIL import Image
import torch
from os.path import join, basename, dirname
from torch.autograd import Variable
from torchvision.transforms import ToTensor, ToPILImage
from torchvision.utils import save_image
import numpy
import argparse
import sys


def toImage(net_output):
    img = net_output.data.squeeze().permute(1, 2, 0).numpy()  # [1,c,h,w]->[h,w,c]
    img = (img*255.0).clip(0, 255)
    img = numpy.uint8(img)
    img = Image.fromarray(img, mode='RGB')
    return img


def test(argv=sys.argv[1:]):
    input = "../dataset/BSDS300/images/val/54082.jpg"
    #input = "../dataset/BSDS300/images/val/159008.jpg"
    output = "sr_{}".format(basename(input))  # save in cwd
    output2 = "sr__{}".format(basename(input))
    model = "snapshot/gnet-epoch-1-pretrain.pth"
    #model = "snapshot/gnet-epoch-200.pth"
    cuda = True
    img = Image.open(input)
    width, height = img.size

    gennet = torch.load(model)
    img = ToTensor()(img)  # [c,w,h]->[1,c,h,w]
    input = Variable(img).view(1, 3, height, width)

    if cuda:
        gennet = gennet.cuda()
        input = input.cuda()

    pred = gennet(input).cpu()
    save_image(pred.data, output)
    #ToPILImage()(pred.data).save(output)
    
    toImage(pred).save(output2)


if __name__ == '__main__':
    assert sys.version_info >= (3, 4)
    test()

