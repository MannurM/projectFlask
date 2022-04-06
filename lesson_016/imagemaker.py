# utf-8

import cv2

image1 = cv2.imread('python_snippets/external_data/probe.jpg')
image_cloud = cv2.imread('python_snippets/external_data/weather_img/cloud.jpg')
image_rain = cv2.imread('python_snippets/external_data/weather_img/rain.jpg')
image_snow = cv2.imread('python_snippets/external_data/weather_img/snow.jpg')
image_sun = cv2.imread('python_snippets/external_data/weather_img/sun.jpg')

# выбор цвета фона и картинки в зависимости от ключа
key_color = 'cloud'
# TODO параметр color нужно отрегулировать
if key_color == 'cloud':
    color = 230
    dst = image_cloud
    color_bg = 1
elif key_color == 'rain':
    color = 150
    dst = image_cloud
    # color_bg = 0
elif key_color == 'snow':
    color = 100
    dst = image_cloud
    # color_bg = 1
else:
    color = 239
    dst = image_sun
    # color_bg = 2

# вставка градиента цвета
back_card = cv2.imread('python_snippets/external_data/probe.jpg')
i = 0
k = 0
for _ in range(25):
    back_card[:, 0 + i: 50 + i] = (50 + k, 255 - k / 5, color)
    i += 20
    k += 5
image_bg = back_card
# cv2.namedWindow('test', cv2.WINDOW_NORMAL)  # изменение размера на полное окно

# вставка объекта погоды

x = 10  # 1 координата вставки
y = 400  # 2 координата вставки
rows, cols = 100, 100  # размер изображения вставки
image_bg[x:x + rows, y:y + cols] = dst


# cv2.imshow('test', back_card)
cv2.imshow('testt', image_bg)
cv2.waitKey(0)
cv2.destroyAllWindows()
