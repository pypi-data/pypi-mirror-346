# myedges/image_utils.py
import cv2

def edge_detection(input_path):
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {input_path}")
    
    # Display original image
    cv2.imshow("Original", img)
    cv2.waitKey(0)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)

    sobelx = cv2.Sobel(img_blur, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(img_blur, cv2.CV_64F, 0, 1, ksize=5)
    sobelxy = cv2.Sobel(img_blur, cv2.CV_64F, 1, 1, ksize=5)

    cv2.imshow("Sobel X", sobelx)
    cv2.waitKey(0)
    cv2.imshow("Sobel Y", sobely)
    cv2.waitKey(0)
    cv2.imshow("Sobel X Y using Sobel() function", sobelxy)
    cv2.waitKey(0)

    edges = cv2.Canny(img_blur, 100, 200)
    cv2.imshow("Canny Edge Detection", edges)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
