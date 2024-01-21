import random
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import KDTree
from webcolors import (
    #for some reason its uppercase?
    CSS3_HEX_TO_NAMES,
    #css3_hex_to_names,
    hex_to_rgb,
)

#chatgpt generated
def convert_input_to_rgb(input_string):
    try:
        components = input_string.strip().split(',')
        red, green, blue = map(int, components)
        red = max(0, min(255, red))
        green = max(0, min(255, green))
        blue = max(0, min(255, blue))
        return red, green, blue
    except ValueError:
        print("Invalid input. Please provide three comma-separated integers.")
        return None

#yoink -> https://medium.com/codex/rgb-to-color-names-in-python-the-robust-way-ec4a9d97a01f
def convert_rgb_to_names(rgb_tuple):
    css3_db = CSS3_HEX_TO_NAMES
    #css3_db = css3_hex_to_names
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    kdt_db = KDTree(rgb_values)
    #print(color_hex)
    #print(rgb_tuple)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'

def create_filled_image(rgb_color, width=1920, height=1080):
    image = Image.new("RGB", (width, height), rgb_color)
    return image

def draw_middle_square_outline(image, text, rgb_color,font_size,font_path):
    fill_color="white"
    #381 is sum 127*3, checking if every color in rgb is below 127, idfk this is simple work around. me no frontend engineer
    if(sum(rgb_color)>381):
        fill_color="black"
    width, height = image.size
    #adjust square size, make sure you select a good fontsize then

    square_size_maybe = 3

    square_width = width // square_size_maybe
    square_height = height // square_size_maybe
    top_left = ((width - square_width) // 2, (height - square_height) // 2)
    bottom_right = (top_left[0] + square_width, top_left[1] + square_height)
    draw = ImageDraw.Draw(image)
    draw.rectangle([top_left, bottom_right], outline=fill_color, width=5)

    # now text shit
    if(text==""):
        text =  f"{convert_rgb_to_names(rgb_color)}\n\n"
        text += f"HEX {rgb_to_hex(rgb_color)}\n\n"
        text += f"RGB {rgb_color}\n\n"
    new_font = ImageFont.truetype(font_path, font_size)

    closeness_to_square=25

    draw.text((top_left[0]+top_left[0]/closeness_to_square, top_left[1]+top_left[1]/closeness_to_square), text, font=new_font, fill=fill_color)
    return image


# chatgpt generated
def rgb_to_hex(rgb):
    rgb = [max(0, min(255, value)) for value in rgb]
    # Convert RGB to hex format
    hex_color = "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
    return hex_color

def main():
    name=""
    font_size=35
    font_path="Minecraft.ttf"
    rgb_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    print("#Enter nothing to select default btw")

    # pro obfuscation tip
    i_love_allah=input("customize font, fontsize?[y/N] ")
    if(i_love_allah.lower()=="y"):
        i_love_allah=input("Enter font size(default 35):")
        if(i_love_allah!=""):
            font_size=int(i_love_allah.strip())
        i_love_allah=input("Enter font path(default Minecraft.ttf)")
        if(i_love_allah!=""):
            font_path=i_love_allah.strip()

    rand=input("Generate Random color?[Y/n] ")
    if(rand.lower()=="n"):
        name=input("whats the name of the color?")
        #most real human code
        input_string = input("Enter RGB values (comma-separated example: 255,255,255 ): ")
        rgb_color = convert_input_to_rgb(input_string)

    filled_image = create_filled_image(rgb_color)
    result_image = draw_middle_square_outline(filled_image,name,rgb_color,font_size,font_path)
    result_image.save("output.png")

if __name__ == "__main__":
    main()
