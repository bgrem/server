import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from content.MODNet.src.models.modnet import MODNet
from constants.image import ImageConstants

class ImageService:
    def get_matte(image:Image):
        # define hyper-parameters
        ref_size = 512

        # define image to tensor transform
        im_transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]
        )

        # create MODNet and load the pre-trained ckpt
        modnet = MODNet(backbone_pretrained=False)
        modnet = nn.DataParallel(modnet)
        ckpt_path = ImageConstants.CKPT_PATH

        if torch.cuda.is_available():
            modnet = modnet.cuda()
            weights = torch.load(ckpt_path)
        else:
            weights = torch.load(ckpt_path, map_location=torch.device('cpu'))

        modnet.load_state_dict(weights)
        modnet.eval()

        # unify image channels to 3
        image = np.asarray(image)
        if len(image.shape) == 2:
            image = image[:, :, None]
        if image.shape[2] == 1:
            image = np.repeat(image, 3, axis=2)
        elif image.shape[2] == 4:
            image = image[:, :, 0:3]

        # convert image to PyTorch tensor
        image = Image.fromarray(image)
        image = im_transform(image)

        # add mini-batch dim
        image = image[None, :, :, :]

        # resize image for input
        im_b, im_c, im_h, im_w = image.shape
        if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
            if im_w >= im_h:
                im_rh = ref_size
                im_rw = int(im_w / im_h * ref_size)
            elif im_w < im_h:
                im_rw = ref_size
                im_rh = int(im_h / im_w * ref_size)
        else:
            im_rh = im_h
            im_rw = im_w
        
        im_rw = im_rw - im_rw % 32
        im_rh = im_rh - im_rh % 32
        image = F.interpolate(image, size=(im_rh, im_rw), mode='area')

        # inference
        _, _, matte = modnet(image.cuda() if torch.cuda.is_available() else image, True)

        # resize matte
        matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
        matte = matte[0][0].data.cpu().numpy()
        return Image.fromarray(((matte * 255).astype('uint8')), mode='L')

    def get_foreground(image:Image, matte:Image):
        # calculate display resolution
        w, h = image.width, image.height
        rw, rh = 800, int(h * 800 / (3 * w))

        # obtain predicted foreground
        image = np.asarray(image)
        if len(image.shape) == 2:
            image = image[:, :, None]
        if image.shape[2] == 1:
            image = np.repeat(image, 3, axis=2)
        elif image.shape[2] == 4:
            image = image[:, :, 0:3]
        matte = np.repeat(np.asarray(matte)[:, :, None], 3, axis=2) / 255
        foreground = image * matte + np.full(image.shape, 255) * (1 - matte)

        return Image.fromarray(np.uint8(foreground))
