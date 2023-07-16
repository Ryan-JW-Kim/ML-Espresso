import matplotlib.pyplot as plt

def show_images(img_list, figure):
    c = 2
    r = len(img_list)//c

    count = 1
    for image in img_list:

        figure.add_subplot(r, c, count)
        plt.imshow(image)
        plt.axis("off")
        plt.title(f"Image {count}")

        count += 1

    