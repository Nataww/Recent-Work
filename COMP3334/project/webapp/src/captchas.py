from captcha.image import ImageCaptcha
import random
import io

# Generate a random CAPTCHA string
def generate_captcha():
    captcha_length = 4
    captcha_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    captcha = ''.join(random.choice(captcha_chars) for _ in range(captcha_length))
    return captcha

# Generate an image-based CAPTCHA
def generate_captcha_image(captcha):
    image_captcha = ImageCaptcha()
    image = image_captcha.generate_image(captcha)
    # image_data = io.BytesIO()
    image_path = f"static/captchas.png"
    image.save(image_path, 'PNG')
    return image_path