import subprocess
import cairo

class ImageManager:
    def __init__(self, matrix_file, color, h_pixel, v_pixel):
        self.matrix_file = matrix_file
        self.h_pixel = int(h_pixel) 
        self.v_pixel = int(v_pixel)
        self.color = color
        self.b_r = 255
        self.b_g = 255
        self.b_b = 255

    def __get_size(self):
        fp = open(self.matrix_file, 'r')
        width = 0
        height = 0
        for line in fp:
            if width == 0:
                headers = line[:-1].split('\t')
                width = len(headers)
            else:
                height = height + 1
        fp.close()
        size = {'width': width, 'height': height}
        return size 

    def export(self, out_file):
        size = self.__get_size()
        width = size['width'] * self.h_pixel
        height = size['height'] * self.v_pixel
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)

        color_value = int(self.color, 16)
        r = (color_value // 0x10000) / 255.0
        g = ((color_value // 0x100) % 0x100) / 255.0
        b = (color_value % 0x100) / 255.0
        print(r)
        print(g)
        print(b)
        context.set_source_rgba(r, g, b, 1.0)
        context.set_line_width(1.0)

        in_fp = open(self.matrix_file, 'r')
        ids = []
        row = 0
        for line in in_fp:
            tokens = line[:-1].split('\t')
            if len(ids) == 0:
                for token in tokens:
                    ids.append(int(token))
            else:
                for i in range(len(ids)):
                    value = int(tokens[i])
                    if value > 0:
                        col = i * self.h_pixel
                        context.move_to(col, row)
                        context.line_to(col + self.h_pixel, row)
                row = row + 1
                context.stroke()
        in_fp.close()
        surface.write_to_png(out_file)
