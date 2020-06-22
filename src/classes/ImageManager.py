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
                for header in headers:
                    id = int(header)
                    if id > width:
                        width = id
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

        in_fp = open(self.matrix_file, 'r')
        out_fp = open(ppm_file, 'w')

        out_fp.write('P3\n')
        out_fp.write(str(size['width'] * self.h_pixel) + ' ' + str(size['height'] * self.v_pixel) + '\n')
        out_fp.write('255\n')

        count = 0;
        ids = []
        for line in in_fp:
            tokens = line[:-1].split('\t')
            if len(ids) == 0:
                for token in tokens:
                    ids.append(int(token))
            else:
                current_id = 0
                lines = []
                for i in range(len(ids)):
                    id = ids[i]
                    value = int(tokens[i])
                    for gap in range(id - current_id - 1):
                        for h in range(self.h_pixel):
                            lines.append(str(self.b_r) + ' ' + str(self.b_g) + ' ' + str(self.b_b) + '\n')
                    current_id = id
                    if value > 0:
                        for h in range(self.h_pixel):
                            lines.append(str(r) + ' ' + str(g) + ' ' + str(b) + '\n')
                    else:
                        for h in range(self.v_pixel):
                            lines.append(str(self.b_r) + ' ' + str(self.b_g) + ' ' + str(self.b_b) + '\n')
                    for v in range(self.v_pixel):
                        out_fp.writelines(lines)
            count = count + 1
            if count % 100 == 0:
                print(str(count) + ' Lines...')
        in_fp.close()
        out_fp.close()

