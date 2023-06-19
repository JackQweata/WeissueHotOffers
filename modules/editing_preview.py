import requests
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def creating_frame(product, tags):
    response = requests.get(product.image)
    product_image = Image.open(BytesIO(response.content))

    img_folder = "img/frame"
    frame_image_path = os.path.join(img_folder, f"{tags}_frame.png")
    clean_frame_image_path = os.path.join(img_folder, f"clean_{tags}_frame.png")

    frame_image = Image.open(frame_image_path)
    if not product.description_type:
        frame_image = Image.open(clean_frame_image_path)

    product_image = product_image.resize(frame_image.size)
    result_image = Image.new("RGBA", frame_image.size)
    result_image = Image.alpha_composite(product_image.convert('RGBA'), frame_image.convert('RGBA'))

    draw = ImageDraw.Draw(result_image)
    draw_text(draw, product, tags)

    image_bytes = BytesIO()
    result_image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return image_bytes


def draw_text(draw, product, teg):
    title_text_x = 218
    title_text_y = 576

    channel_text_x = 151
    channel_text_y = 9

    record_text_x = 320
    record_text_y = 623

    channel_text = f"{product.channel} CHANNEL"
    title_text = ''
    record_text = ''

    path_font = os.path.join("img", "Inter-V.ttf")
    font_title = ImageFont.truetype(path_font, 22)
    font_channel = ImageFont.truetype(path_font, 13)
    font_record = ImageFont.truetype(path_font, 16)

    if product.description_type == 'salle':
        title_text = f"Скидка {product.description_text} %"
        title_text_x = 275
        title_text_y = 624

    elif product.description_type == 'size':
        title_text = 'Осталось размеров:' if teg == 'WB' else ''
        record_text = product.size_name[0]

    draw.text((channel_text_x, channel_text_y), channel_text, font=font_channel, fill=(255, 255, 255, 168))
    draw.text((title_text_x, title_text_y), title_text, font=font_title, fill=(255, 255, 255))
    draw.text((record_text_x, record_text_y), record_text, font=font_record, fill=(255, 255, 255))
