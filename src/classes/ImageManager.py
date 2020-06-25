import subprocess

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
        ppm = out_file + '.ppm'
        self.__export_ppm(ppm)
        command = ['convert', ppm, out_file]
        subprocess.run(command)

    def __export_ppm(self, ppm_file):
        size = self.__get_size()
        color_value = int(self.color, 16)
        r = color_value // 0x10000
        g = (color_value // 0x100) % 0x100
        b = color_value % 0x100
        rgb = str(r) + ' ' + str(g) + ' ' + str(b)
        back = str(self.b_r) + ' ' + str(self.b_g) + ' ' + str(self.b_b)

        in_fp = open(self.matrix_file, 'r')
        out_fp = open(ppm_file, 'w')

        out_fp.write('P3\n')
        out_fp.write(str(size['width'] * self.h_pixel) + ' ' + str(size['height'] * self.v_pixel) + '\n')
        out_fp.write('255\n')

        ids = []
        for line in in_fp:
            tokens = line[:-1].split('\t')
            if len(ids) == 0:
                for token in tokens:
                    ids.append(int(token))
            else:
                for i in range(len(ids)):
                    value = int(tokens[i])
                    if value > 0:
                        print(rgb * self.h_pixel, file=out_fp)
                    else:
                        print(back * self.h_pixel, file=out_fp)
        in_fp.close()
        out_fp.close()

