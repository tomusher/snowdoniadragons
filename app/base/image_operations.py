from wagtail.wagtailimages.image_operations import Operation
from willow.registry import registry
from willow.plugins.pillow import PillowImage

def pad_image(image, width, height):
    from PIL import Image
    image_width, image_height = image.get_size()
    background = Image.new("RGB", (width, height), "white")
    try:
        mask = image.image.split()[3]
        background.paste(image.image, ((width-image_width)//2,
                                       (height-image_height)//2),
                            mask=mask)
    except IndexError:
        background.paste(image.image, ((width-image_width)//2,
                                       (height-image_height)//2))
    return PillowImage(background)

registry.register_operation(PillowImage, 'pad', pad_image)


class PadOperation(Operation):
    def construct(self, size, *extra):
        width_str, height_str = size.split('x')
        self.width = int(width_str)
        self.height = int(height_str)

    def run(self, willow, image):
        image_width, image_height = willow.get_size()
        width_max = max(image_width, self.width)
        height_max = max(image_height, self.height)

        return willow.pad(width_max, height_max)
