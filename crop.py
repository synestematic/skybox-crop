'''
pip3 install Pillow
'''
import os
import time

import click

from PIL import Image

MODE = 'L'
MODE = 'RGB'
MODE = 'CYMK'

class SkyboxImage(object):

    def __init__(self, path):
        self.path = path
        self.ext  = path[-3:]
        self.cubemaps = [c for c in self.cube_maps]
        self.img  = None
        self.load()

    def load(self):
        self.img = Image.open(self.path)
        # print(self.img.__dict__)

    def convert(self, mode):
        self.img = self.img.convert(mode)

    def crop(self, box):
        return self.img.crop(box)

    def crop_by_sections(self):
        width, height = self.img.size
        v_section_pixels = height / self.sections['vertical']
        h_section_pixels = width  / self.sections['horizontal']

        if not h_section_pixels.is_integer():
            raise ValueError(h_section_pixels)
        if not v_section_pixels.is_integer():
            raise ValueError(v_section_pixels)

        h_section_pixels = int(h_section_pixels)
        v_section_pixels = int(v_section_pixels)

        for v in range(self.sections['vertical']):
            for h in range(self.sections['horizontal']):
                if (v, h) in self.vh_filters:
                    continue

                new_img = self.crop( (
                    h_section_pixels * h,  # left
                    v_section_pixels * v,  # upper
                    h_section_pixels * h + h_section_pixels, # right
                    v_section_pixels * v + v_section_pixels, # lower
                ) )

                new_img.save(
                    f'/home/user/{self.cubemaps.pop(0)}.{self.ext}'
                )

                time.sleep(0.5)


class StraightImage(SkyboxImage):
    ''' rludbf '''
    sections = {
        'vertical': 1, 'horizontal': 6,
    }

    vh_filters = ()
    cube_maps = (
        '1rt', '2lf', '3up', '4dn', '5bk', '6ft',
    )


class CrossImage(SkyboxImage):
    ''' .u..
        lbrf
        .d.. '''
    sections = {
        'vertical': 3, 'horizontal': 4,
    }
    vh_filters = (
        (0,0), (0,2), (0,3),
        (2,0), (2,2), (2,3),
    )
    cube_maps = (
        '3up', '2lf', '5bk', '1rt', '6ft', '4dn', 
    )


@click.command()
@click.argument('source_image')
@click.option(
    '-i', '--img-type',
    type=click.Choice(['cross', 'straight']),
    default='cross'
)
def main(source_image, img_type):
    ImageClass = StraightImage if img_type == 'straight' else CrossImage
    ImageClass(source_image).crop_by_sections()


if __name__ == '__main__':
    main()
