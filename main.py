from PIL import Image , ImageEnhance
import math

def convert_image(path_image ,char_list , size_art , inversion_img):
    img = Image.open(path_image) # ./image.png
    img = img.convert("L") #convert to black and white format
    enh = ImageEnhance.Contrast(img)
    contrast_image = enh.enhance(2.0)
    img2 = contrast_image.resize((size_art, size_art))
    img2 = img2.rotate(90)
    final_art = []

    if inversion_img == "T":
        char_list = char_list[::-1]

    for i in range(0, size_art):
        line_art = []
        len_interval = 255//len(char_list)
        for j in range(0, size_art):
            value = img2.getpixel((i, j))
            index = math.floor((value/len_interval))-1
            line_art.append(char_list[index])
        final_art.append(line_art)
    return final_art



path_image = str(input("Enter the path of the image: "))
size_art = int(input("Enter the size of the art: ")) #64x64, 128x128, 256x256
char_list = ["@" , "G", "5" , "4" , "2" , "'", "."] #from black to white
image_inversion = str(input("Enter image inversion T/F:"))#enter T or F
final_art = convert_image(path_image , char_list , size_art , image_inversion)

with open("output.txt", "w") as f:
    f.write("")

for i in final_art :
    for j in i:
        with open("output.txt", "a") as f:
            f.write(str(j) + " ")

    with open("output.txt", "a") as f:
        f.write("\n")


