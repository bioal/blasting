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
        self.margin_left = 80
        self.margin_top = 30
        self.margin_bottom = 5
        self.margin_right = 5 
        self.y_interval = 1000
        self.measure_length = 10 

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
        width = size['width'] * self.h_pixel + self.margin_left + self.margin_right
        height = size['height'] * self.v_pixel + self.margin_top + self.margin_bottom
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
                        context.move_to(col + self.margin_left, row + self.margin_top)
                        context.line_to(col + self.h_pixel + self.margin_left, row + self.margin_top)
                row = row + 1
                context.stroke()
        self.__draw_axes(context, width, height)
        in_fp.close()
        surface.write_to_png(out_file)

    def __draw_axes(self, context, width, height):
        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        rect_x = self.margin_left - 1
        rect_y = self.margin_top - 1
        rect_width = width - self.margin_left - self.margin_right + 2
        rect_height = height - self.margin_top - self.margin_bottom + 2
        context.rectangle(rect_x, rect_y, rect_width, rect_height)
        context.stroke()

        context.set_font_size(24.0)
        context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        count = 0
        position = self.margin_top
        while position < height - self.margin_bottom:
            if count > 0:
                x = self.margin_left - self.measure_length
                context.move_to(x, position)
                context.line_to(self.margin_left, position)
                s = str(count)
                result = context.text_extents(s)
                context.move_to(x - result.width, position + result.height / 2)
                context.show_text(s)
            count += self.y_interval 
            position = position + self.y_interval * self.v_pixel 
        context.stroke() 
