# utf-8

import cv2

image1 = cv2.imread('python_snippets/external_data/probe.jpg')
image_cloud = cv2.imread('python_snippets/external_data/weather_img/cloud.jpg')
image_rain = cv2.imread('python_snippets/external_data/weather_img/rain.jpg')
image_snow = cv2.imread('python_snippets/external_data/weather_img/snow.jpg')
image_sun = cv2.imread('python_snippets/external_data/weather_img/sun.jpg')

# вставка градиента цвета
back_card = cv2.imread('python_snippets/external_data/probe.jpg')
i = 0
k = 0
for _ in range(25):
    back_card[:, 0 + i: 50 + i] = (50 + k, 255 - k / 5, 239)
    i += 20
    k += 5


# cv2.namedWindow('test', cv2.WINDOW_NORMAL)
image_bg = back_card
# вставка объекта погоды
image_bg = image1[100:100, 200:200, 1]
# cv2.imshow('test', back_card)
cv2.imshow('testt', image_bg)
cv2.waitKey(0)
cv2.destroyAllWindows()