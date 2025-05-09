import sys
import os
import cv2
import numpy as np

def process_image(image_path=None):
    if image_path is None or image_path.startswith('--'):
        if image_path == '--show-code':
            show_code()
            return
        print("Usage: richerfilter <image_path> or richerfilter --show-code")
        return

    image = cv2.imread(image_path)
    if image is None:
        print(f"Could not read image {image_path}")
        return

    # Identity filter
    kernel1 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    identity = cv2.filter2D(src=image, ddepth=-1, kernel=kernel1)
    cv2.imshow("Identity Filter", identity)
    cv2.imwrite('identity.jpg', identity)

    # Kernel blur
    kernel2 = np.ones((5, 5), np.float32) / 25
    img_kernel_blur = cv2.filter2D(src=image, ddepth=-1, kernel=kernel2)
    cv2.imshow("Kernel Blur", img_kernel_blur)
    cv2.imwrite('blur_kernel.jpg', img_kernel_blur)

    # cv2 blur
    img_blur = cv2.blur(src=image, ksize=(5, 5))
    cv2.imshow("Blur", img_blur)
    cv2.imwrite('blur.jpg', img_blur)

    # Gaussian blur
    gaussian_blur = cv2.GaussianBlur(src=image, ksize=(5, 5), sigmaX=0, sigmaY=0)
    cv2.imshow("Gaussian Blur", gaussian_blur)
    cv2.imwrite('gaussian_blur.jpg', gaussian_blur)

    # Median blur
    median = cv2.medianBlur(src=image, ksize=5)
    cv2.imshow("Median Blur", median)
    cv2.imwrite('median_blur.jpg', median)

    # Sharpen
    kernel3 = np.array([[0, -1, 0], [-1, 5, -5], [0, -1, 0]])
    sharp_img = cv2.filter2D(src=image, ddepth=-1, kernel=kernel3)
    cv2.imshow("Sharpened Image", sharp_img)
    cv2.imwrite('sharp_image.jpg', sharp_img)

    # Bilateral filter
    bilateral_filter = cv2.bilateralFilter(src=image, d=9, sigmaColor=75, sigmaSpace=75)
    cv2.imshow("Bilateral Filter", bilateral_filter)
    cv2.imwrite('bilateral_filtering.jpg', bilateral_filter)

    # Wait for a key press and close all image windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("✅ All filters applied, images displayed, and saved successfully!")

def show_code():
    file_path = os.path.realpath(__file__)
    with open(file_path, 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: richerfilter <image_path> or richerfilter --show-code")
    else:
        process_image(sys.argv[1])
