from skimage.io import imread


def main():
    img = imread('hoelli.png')
    print(img.shape)

    with open('hoelli.csv', 'w') as f:
        for y in range(img.shape[0]):
            line = ''
            for x in range(img.shape[1]):
                rgb = f'{img[y, x, 0]:02x}'
                rgb += f'{img[y, x, 1]:02x}'
                rgb += f'{img[y, x, 2]:02x}'
                line += rgb

                if x < img.shape[1] - 1:
                    line += ', '

            print(line, file=f)


if __name__ == '__main__':
    main()
