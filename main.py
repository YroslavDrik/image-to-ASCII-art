from PIL import Image , ImageEnhance, ImageDraw, ImageFont
import math
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

    if inversion_img == "1":
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

def draw_img(final_art_list , width , height , is_color , path_image , index , color_background , video_or_img):
    color_list = []
    color_pixel = [255, 255, 255]
    if is_color == "1":
        img = Image.open(path_image)  # ./image.png
        img = img.resize((width, height))
        for i in range(0, height):
            color_pixel = []
            for j in range(0, width):
                value = img.getpixel((j, i))
                color_pixel.append(list(value))
            color_list.append(color_pixel)

    im = Image.new("RGB", (width*20, height*20), (color_background[0], color_background[1], color_background[2]))

    d = ImageDraw.Draw(im)

    for i in range(len(final_art_list)):
        for j in range(len(final_art_list[i])):
            art_char = final_art_list[i][j] + " "
            if is_color == "1":
                color_pixel = color_list[i][j]
            print(i , j , art_char , color_pixel)
            font = ImageFont.truetype("Pillow/Tests/fonts/DejaVuSansMono.ttf", 17)

            d.text((i*20, j * 20), art_char, fill=(color_pixel[0], color_pixel[1], color_pixel[2]), font=font)

    if video_or_img == "1":
        path = "output.png"
        im.rotate(270).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(path)


    else:
        path = "images_ascii/" + str(index) + ".png"
        im.rotate(270).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(path)

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

video_or_image = input("Enter the image or video (Image - 1, Video - 2): ")
if video_or_image == "1":
    path_image = input("Enter the path of the image: ")
elif video_or_image == "2":
    path_video = input("Enter the path of the video: ")
    height_video = int(input("Enter the height of the video: "))
    width_video = int(input("Enter the width of the video: "))
height_art = int(input("Enter the height of the art: "))
width_art = int(input("Enter the width of the art: "))
image_inversion = str(input("Enter image inversion (True - 1, False - 2): "))
is_color = str(input("Is color? (True - 1, False - 2): "))

if is_color == "1":
    color_background = list(map(int , input("Enter the background color of the image(RGB): ").split())) #12 123 234
else:
    color_background = [0 , 0 ,0]

if video_or_image == "1":
    final_art = convert_image(path_image , char_list , width_art, height_art , image_inversion)
    draw_img(final_art , width_art, height_art , is_color , path_image, 0 , color_background , video_or_image)
    with open("output.txt", "w") as f:
        f.write("")

    for i in final_art:
        for j in i:
            with open("output.txt", "a") as f:
                f.write(str(j) + " ")

        with open("output.txt", "a") as f:
            f.write("\n")

elif video_or_image == "2":
    count_frames = video_to_images(path_video)
    for i in range(count_frames):
        path="images/"+str(i)+".png"
        print(path)
        final_art = convert_image(path , char_list , width_art, height_art , image_inversion)
        draw_img(final_art , width_art, height_art , is_color , path  ,i , color_background , video_or_image)

    art_to_video(count_frames , 30 , width_video , height_video)