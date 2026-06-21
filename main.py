from PIL import Image , ImageEnhance, ImageDraw, ImageFont
import math
import random
import moviepy as mv
import cv2

def convert_image(path_image ,char_list , width , height , inversion_img):
    img = Image.open(path_image) # ./image.png
    img = img.convert("L") #convert to black and white format
    enh = ImageEnhance.Contrast(img)
    contrast_image = enh.enhance(2.0)
    img2 = contrast_image.resize((width, height))
    img2.save("test.png")
    final_art = []

    if inversion_img == "T":
        char_list = char_list[::-1]

    for i in range(0, height):
        line_art = []
        len_interval = 255//len(char_list)
        for j in range(0, width):
            value = img2.getpixel((j, i))
            index = math.floor((value/len_interval))-1
            line_art.append(char_list[index])
        final_art.append(line_art)
    return final_art

def draw_img(final_art_list , width , height , is_color , path_image , index):
    color_list = []
    color_pixel = [255, 255, 255]
    color_background = [0 , 0, 0]
    if is_color == "T":
        img = Image.open(path_image)  # ./image.png
        enh = ImageEnhance.Contrast(img)
        contrast_image = enh.enhance(2.0)
        img2 = contrast_image.resize((width, height))
        for i in range(0, height):
            color_pixel = []
            for j in range(0, width):
                value = img2.getpixel((j, i))
                color_pixel.append(list(value))
            color_list.append(color_pixel)

    im = Image.new("RGB", (width*20, height*20), (color_background[0], color_background[1], color_background[2]))

    d = ImageDraw.Draw(im)

    index_y = 0
    for i in final_art_list:
        art_char = ""
        for j in i:
            art_char += j + " "
        if is_color == "T":
            index_color = random.randrange(0, width)
            color_pixel = color_list[index_y][index_color]

        font = ImageFont.truetype("Pillow/Tests/fonts/DejaVuSansMono.ttf", 17)

        d.text((0, index_y * 20), art_char, fill=(color_pixel[0], color_pixel[1], color_pixel[2]), font=font)
        index_y += 1

    path = "images_ascii/" + str(index) + ".png"
    im.save(path)

def video_to_images(path):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    count = 0
    while success:
        path = "images/" + str(count) + ".png"
        cv2.imwrite(path, image) #save frame
        success, image = vidcap.read() #reading frame
        count += 1
        print(count)

    return count

def art_to_video(count , fps , width , height):
    image_path_list = []
    for i in range(count):
        path = "images_ascii/" + str(i) + ".png"
        img = Image.open(path)
        img = img.resize((width, height))
        img.save(path)
        image_path_list.append(path)
    final_video = mv.ImageSequenceClip(image_path_list, fps=fps)
    final_video.write_videofile("result.mp4")

#------------------------------------------------------------
char_list = ["@" , "G", "5" , "4" , "2" , "'", "."] #from black to white

video_or_image = input("Enter the image or video (I/V): ")
if video_or_image == "I":
    path_image = input("Enter the path of the image: ")
elif video_or_image == "V":
    path_video = input("Enter the path of the video: ")
    height_video = int(input("Enter the height of the video: "))
    width_video = int(input("Enter the width of the video: "))
height_art = int(input("Enter the height of the image: "))
width_art = int(input("Enter the width of the image: "))
image_inversion = str(input("Enter image inversion (T/F):"))#enter T or F
is_color = str(input("Is color? (T/F): "))

if video_or_image == "I":
    final_art = convert_image(path_image , char_list , width_art, height_art , image_inversion)
    draw_img(final_art , width_art, height_art , is_color , path_image, 0)
    with open("output.txt", "w") as f:
        f.write("")

    for i in final_art:
        for j in i:
            with open("output.txt", "a") as f:
                f.write(str(j) + " ")

        with open("output.txt", "a") as f:
            f.write("\n")

elif video_or_image == "V":
    count_frames = video_to_images(path_video)
    for i in range(count_frames):
        path="images/"+str(i)+".png"
        print(path)
        final_art = convert_image(path , char_list , width_art, height_art , image_inversion)
        draw_img(final_art , width_art, height_art , is_color , path  ,i)

    art_to_video(count_frames , 30 , width_video , height_video)