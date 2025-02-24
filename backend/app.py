# import requests

# url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1/tesseract-5.3.1.20230401.exe"
# filename = "tesseract-ocr-windows.exe"

# response = requests.get(url, stream=True)
# with open(filename, "wb") as file:
#     for chunk in response.iter_content(chunk_size=1024):
#         if chunk:
#             file.write(chunk)






# import cv2
# import pytesseract
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# from PIL import Image

# # Cấu hình Tesseract OCR
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\duong\Downloads\Tesseract-OCR\Tesseract-OCR\tesseract.exe'

# # My custom class for declare region of interest.
# class ImageConstantROI():
#     class CCCD(object):
#         ROIS = {
#             "id": (460, 330, 530, 80),           # Số CCCD
#             "name": (340, 460, 600, 50),         # Họ và tên
#             "birth_date": (735, 510, 215, 50),   # Ngày sinh
#             "gender": (605, 570, 90, 40),       # Giới tính
#             "nationality": (1030, 550, 190, 50),  # Quốc tịch
#             "place_birth": (350, 660, 800,50),  # Quê quán
#             "address": [(860,700,300,49),(370, 750, 835,50)],      # Nơi thường trú
#         }

# # Custom function to show open cv image on notebook.
# def display_img(cvImg):
#     cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
#     plt.figure(figsize=(10,8))
#     plt.imshow(cvImg)
#     plt.axis('off')
#     plt.show()

# # Loading image using cv2
# baseImg = cv2.imread(r'C:\Users\duong\Downloads\anhKhai.jpg')
# baseH, baseW, baseC = baseImg.shape


# def cropImageRoi(image, roi):
#     if isinstance(roi, list):
#         cropped_images = [
#             image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#             for r in roi
#         ]
#         return cropped_images
#     elif isinstance(roi, tuple):
#         roi_cropped = image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
#         return roi_cropped
#     else:
#         raise ValueError("ROI must be a tuple or a list of tuples.")

# # Processing each ROI in the dictionary
# for key, roi_coords in ImageConstantROI.CCCD.ROIS.items():
#     cropped_imgs = cropImageRoi(baseImg, roi_coords)
#     if isinstance(cropped_imgs, list):
#         text = [pytesseract.image_to_string(cropped_img, lang="vie").strip() for cropped_img in cropped_imgs]
        
#     else:
#         text = pytesseract.image_to_string(cropped_imgs, lang="vie").strip()
        

# # Load second image
# img2 = cv2.imread(r'C:\Users\duong\Downloads\anhHuy.jpg')


# # Keypoints detection
# orb = cv2.ORB_create(1000)
# kp, des = orb.detectAndCompute(baseImg, None)
# imgKp = cv2.drawKeypoints(baseImg,kp, None)


# PER_MATCH = 0.25
# kp1, des1 = orb.detectAndCompute(img2, None)
# bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# matches = list(bf.match(des1, des))
# matches.sort(key=lambda x: x.distance)
# best_matches = matches[:int(len(matches)*PER_MATCH)]
# imgMatch = cv2.drawMatches(img2, kp1, baseImg, kp, best_matches,None, flags=2)


# srcPoints = np.float32([kp1[m.queryIdx].pt for m in best_matches]).reshape(-1,1,2)
# dstPoints = np.float32([kp[m.trainIdx].pt for m in best_matches]).reshape(-1,1,2)
# matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints,cv2.RANSAC, 5.0)
# img_final = cv2.warpPerspective(img2, matrix_relationship, (baseW, baseH))


# # Processing each ROI in the dictionary for transformed image
# for key, roi_coords in ImageConstantROI.CCCD.ROIS.items():
#     cropped_imgs = cropImageRoi(img_final, roi_coords)
#     if isinstance(cropped_imgs, list):
#         text = [pytesseract.image_to_string(cropped_img, lang="vie").strip() for cropped_img in cropped_imgs]
#         print(f"{key}: {' '.join(text)}")
#     else:
#         text = pytesseract.image_to_string(cropped_imgs, lang="vie").strip()
#         print(f"{key}: {text}")



# from flask import Flask, request, jsonify
# import cv2
# import pytesseract
# import numpy as np
# import os
# from PIL import Image
# import io

# app = Flask(__name__)

# # Cấu hình thư mục lưu ảnh
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\duong\Downloads\Tesseract-OCR\Tesseract-OCR\tesseract.exe'

# @app.route('/extract_text', methods=['POST'])
# def extract_text():
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image file provided'}), 400

#         file = request.files['image']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         # Kiểm tra dung lượng file
#         file_size = len(file.read())
#         if file_size == 0:
#             return jsonify({'error': 'Empty file received'}), 400
#         print(f"File size: {file_size} bytes")

#         # Lưu file để kiểm tra
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.seek(0)  # Reset con trỏ file
#         file.save(file_path)
#         print(f"File saved at: {file_path}")

#         # Đọc ảnh bằng OpenCV
#         file.seek(0)
#         img_bytes = file.read()
#         image_array = np.frombuffer(img_bytes, np.uint8)
#         img_cv = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

#         if img_cv is None:
#             return jsonify({'error': 'Could not decode image'}), 400

#         # Chuyển thành PIL để kiểm tra
#         img = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))

#         # OCR xử lý ảnh
#         text = pytesseract.image_to_string(img, lang="vie").strip()

#         return jsonify({'text': text})

#     except Exception as e:
#         print("Lỗi xử lý ảnh:", str(e))
#         return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)

# from flask import Flask, request, jsonify
# import cv2
# import pytesseract
# import numpy as np
# import os
# from PIL import Image
# import io

# app = Flask(__name__)

# # Cấu hình thư mục lưu ảnh
# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Đường dẫn Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\duong\Downloads\Tesseract-OCR\Tesseract-OCR\tesseract.exe'

# class ImageConstantROI:
#     class CCCD(object):
#         ROIS = {
#             "id": (460, 330, 530, 80),           # Số CCCD
#             "name": (340, 460, 600, 50),         # Họ và tên
#             "birth_date": (735, 510, 215, 50),   # Ngày sinh
#             "gender": (605, 570, 90, 40),       # Giới tính
#             "nationality": (1030, 550, 190, 50),  # Quốc tịch
#             "place_birth": (350, 660, 800,50),  # Quê quán
#             "address": [(860,700,300,49),(370, 750, 835,50)],      # Nơi thường trú
#         }

# # Hàm cắt ảnh từ các khu vực ROI
# def cropImageRoi(image, roi):
#     if isinstance(roi, list):
#         cropped_images = [
#             image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
#             for r in roi
#         ]
#         return cropped_images
#     elif isinstance(roi, tuple):
#         roi_cropped = image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
#         return roi_cropped
#     else:
#         raise ValueError("ROI must be a tuple or a list of tuples.")

# @app.route('/extract_text', methods=['POST'])
# def extract_text():
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image file provided'}), 400

#         file = request.files['image']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         # Đọc ảnh gửi lên
#         img = cv2.imread(file_path)
#         if img is None:
#             return jsonify({'error': 'Could not decode image'}), 400

#         # Đọc ảnh baseImg (ảnh cơ sở)
#         baseImg = cv2.imread(r'C:\Users\duong\Downloads\anhKhai.jpg')
#         baseH, baseW, baseC = baseImg.shape

#         # Tiền xử lý ảnh gửi lên và baseImg để so sánh
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         gray = cv2.multiply(gray, 1.5)
#         blured1 = cv2.medianBlur(gray, 3)
#         blured2 = cv2.medianBlur(gray, 51)
#         divided = np.ma.divide(blured1, blured2).data
#         normed = np.uint8(255 * divided / divided.max())
#         th, threshed = cv2.threshold(normed, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

#         # Sử dụng ORB để phát hiện keypoints giữa baseImg và ảnh gửi lên
#         orb = cv2.ORB_create(1000)
#         kp1, des1 = orb.detectAndCompute(baseImg, None)
#         kp2, des2 = orb.detectAndCompute(img, None)

#         bf = cv2.BFMatcher(cv2.NORM_HAMMING)
#         matches = list(bf.match(des1, des2))
#         matches.sort(key=lambda x: x.distance)
#         best_matches = matches[:int(len(matches) * 0.25)]  # Lọc ra các match tốt nhất

#         # Chuyển các điểm matching thành 2D array
#         srcPoints = np.float32([kp2[m.queryIdx].pt for m in best_matches]).reshape(-1, 1, 2)
#         dstPoints = np.float32([kp1[m.trainIdx].pt for m in best_matches]).reshape(-1, 1, 2)

#         # Tính ma trận đồng nhất (homography)
#         matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
#         img_transformed = cv2.warpPerspective(img, matrix_relationship, (baseW, baseH))

#         # Tiền xử lý ảnh đã biến đổi (transformed image)
#         gray_transformed = cv2.cvtColor(img_transformed, cv2.COLOR_BGR2GRAY)
#         gray_transformed = cv2.multiply(gray_transformed, 1.5)
#         blured1 = cv2.medianBlur(gray_transformed, 3)
#         blured2 = cv2.medianBlur(gray_transformed, 51)
#         divided = np.ma.divide(blured1, blured2).data
#         normed = np.uint8(255 * divided / divided.max())
#         th, threshed = cv2.threshold(normed, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

#         # Trích xuất văn bản từ các ROI
#         extracted_texts = {}
#         for key, roi_coords in ImageConstantROI.CCCD.ROIS.items():
#             cropped_imgs = cropImageRoi(threshed, roi_coords)
#             if isinstance(cropped_imgs, list):
#                 text = [pytesseract.image_to_string(cropped_img, lang="vie").strip() for cropped_img in cropped_imgs]
#                 extracted_texts[key] = ' '.join(text)
#             else:
#                 text = pytesseract.image_to_string(cropped_imgs, lang="vie").strip()
#                 extracted_texts[key] = text

#         # Trả về kết quả dưới dạng JSON
#         return jsonify({'extracted_texts': extracted_texts})

#     except Exception as e:
#         print("Lỗi xử lý ảnh:", str(e))
#         return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
#-----------------------------------------------------------------------------------------------------------------
from flask import Flask, request, jsonify
import cv2
import pytesseract
import numpy as np
import os
from PIL import Image
#import io

app = Flask(__name__)

# Cấu hình thư mục lưu ảnh
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\duong\Downloads\Tesseract-OCR\Tesseract-OCR\tesseract.exe'

class ImageConstantROI:
    class CCCD(object):
        ROIS = {
            "id": (460, 330, 530, 80),           # Số CCCD
            "name": (340, 460, 600, 50),         # Họ và tên
            "birth_date": (735, 510, 215, 50),   # Ngày sinh
            "gender": (605, 570, 90, 40),       # Giới tính
            "nationality": (1030, 550, 190, 50),  # Quốc tịch
            "place_birth": (350, 660, 800,50),  # Quê quán
            "address": [(860,700,300,49),(370, 750, 835,50)],      # Nơi thường trú
        }

# Hàm cắt ảnh từ các khu vực ROI
def cropImageRoi(image, roi):
    if isinstance(roi, list):
        cropped_images = [
            image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            for r in roi
        ]
        return cropped_images
    elif isinstance(roi, tuple):
        roi_cropped = image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
        return roi_cropped
    else:
        raise ValueError("ROI must be a tuple or a list of tuples.")

@app.route('/extract_text', methods=['POST'])
def extract_text():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Đọc ảnh gửi lên
        img = cv2.imread(r'C:\Users\duong\MobileApp\uploads\cropped_image.jpg')
        if img is None:
            return jsonify({'error': 'Could not decode image'}), 400
        baseImg = cv2.imread(r'C:\\Users\\duong\\Downloads\\anhKhai.jpg')
        #Declare image size, width height and chanel
        baseH, baseW = baseImg.shape[:2]
        #Init orb, keypoints detection on base Image
        orb = cv2.ORB_create(1000)

        kp, des = orb.detectAndCompute(baseImg, None)
        imgKp = cv2.drawKeypoints(baseImg,kp, None)

        PER_MATCH = 0.25

        #Detect keypoint on img
        kp1, des1 = orb.detectAndCompute(img, None)

        #Init BF Matcher, find the matches points of two images
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = list(bf.match(des1, des))

        #Select top 30% best matcher
        matches.sort(key=lambda x: x.distance)
        best_matches = matches[:int(len(matches)*PER_MATCH)]

        #Show match img
        imgMatch = cv2.drawMatches(img, kp1, baseImg, kp, best_matches,None, flags=2)

        #Init source points and destination points for findHomography function.
        srcPoints = np.float32([kp1[m.queryIdx].pt for m in best_matches]).reshape(-1,1,2)
        dstPoints = np.float32([kp[m.trainIdx].pt for m in best_matches]).reshape(-1,1,2)


        #Find Homography of two images
        matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints,cv2.RANSAC, 5.0)

        #Transform the image to have the same structure as the base image
        img_final1 = cv2.warpPerspective(img, matrix_relationship, (baseW, baseH))

            #Resize image
            #img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

            #convert to grayscale
        gray = cv2.cvtColor(img_final1, cv2.COLOR_BGR2GRAY)
        gray = cv2.multiply(gray, 1.5)

            #blur remove noise
        blured1 = cv2.medianBlur(gray,3)
        blured2 = cv2.medianBlur(gray,51)
        divided = np.ma.divide(blured1, blured2).data
        normed = np.uint8(255*divided/divided.max())


            #Threshold image
        th, threshed = cv2.threshold(normed, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)



        # Function to crop a single ROI or a list of ROIs
        def cropImageRoi(image, roi):
            if isinstance(roi, list):  # If ROI is a list of tuples
                cropped_images = [
                    image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                    for r in roi
                ]
                return cropped_images  # Return list of cropped images
            elif isinstance(roi, tuple):  # If ROI is a single tuple
                roi_cropped = image[int(roi[1]):int(roi[1] + roi[3]), int(roi[0]):int(roi[0] + roi[2])]
                return roi_cropped  # Return a single cropped image
            else:
                raise ValueError("ROI must be a tuple or a list of tuples.")

        # # Đọc ảnh baseImg (ảnh cơ sở)
        # baseImg = cv2.imread(r'C:\\Users\\duong\\Downloads\\anhKhai.jpg')
        # baseH, baseW = baseImg.shape[:2]  # Chỉ lấy chiều cao & chiều rộng


        # # # Tiền xử lý ảnh gửi lên và baseImg để so sánh
        # # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # # gray = cv2.multiply(gray, 1.5)
        # # blured1 = cv2.medianBlur(gray, 3)
        # # blured2 = cv2.medianBlur(gray, 51)
        # # divided = np.ma.divide(blured1, blured2).data
        # # normed = np.uint8(255 * divided / divided.max())
        # # th, threshed = cv2.threshold(normed, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        # # Sử dụng ORB để phát hiện keypoints giữa baseImg và ảnh gửi lên
        # orb = cv2.ORB_create(1000)
        # kp1, des1 = orb.detectAndCompute(baseImg, None)
        # kp2, des2 = orb.detectAndCompute(img, None)

        # bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # matches = list(bf.match(des1, des2))
        # matches.sort(key=lambda x: x.distance)
        # best_matches = matches[:int(len(matches) * 0.25)]  # Lọc ra các match tốt nhất

        # # Chuyển các điểm matching thành 2D array
        # srcPoints = np.float32([kp2[m.queryIdx].pt for m in best_matches]).reshape(-1, 1, 2)
        # dstPoints = np.float32([kp1[m.trainIdx].pt for m in best_matches]).reshape(-1, 1, 2)

        # # Tính ma trận đồng nhất (homography)
        # matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
        # img_transformed = cv2.warpPerspective(img, matrix_relationship, (baseW, baseH))

        # # Tiền xử lý ảnh đã biến đổi (transformed image)
        # gray_transformed = cv2.cvtColor(img_transformed, cv2.COLOR_BGR2GRAY)
        # gray_transformed = cv2.multiply(gray_transformed, 1.5)
        # blured1 = cv2.medianBlur(gray_transformed, 3)
        # blured2 = cv2.medianBlur(gray_transformed, 51)
        # divided = np.ma.divide(blured1, blured2).data
        # normed = np.uint8(255 * divided / divided.max())
        # th, threshed = cv2.threshold(normed, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        # Trích xuất văn bản từ các ROI
        extracted_texts = {}
        for key, roi_coords in ImageConstantROI.CCCD.ROIS.items():
            print(f"Đang xử lý ROI: {key} với tọa độ {roi_coords}")
            cropped_imgs = cropImageRoi(threshed, roi_coords)
            if isinstance(cropped_imgs, list):
                text = [pytesseract.image_to_string(cropped_img, lang="vie").strip() for cropped_img in cropped_imgs]
                extracted_texts[key] = ' '.join(text)
                print(f"Văn bản đã trích xuất từ ROI {key}: {' '.join(text)}")
            else:
                text = pytesseract.image_to_string(cropped_imgs, lang="vie").strip()
                extracted_texts[key] = text
                print(f"Văn bản đã trích xuất từ ROI {key}: {text}")

        # Trả về kết quả dưới dạng JSON
        return jsonify({'extracted_texts': extracted_texts})

    except Exception as e:
        print("Lỗi xử lý ảnh:", str(e))
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
#---------------------------------------------------------------------------------------------------------

# from flask import Flask, request, jsonify
# import cv2
# import pytesseract
# import numpy as np
# import os
# import uuid
# from PIL import Image
# import io

# app = Flask(__name__)

# UPLOAD_FOLDER = "uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\duong\Downloads\Tesseract-OCR\Tesseract-OCR\tesseract.exe'

# class ImageConstantROI:
#     class CCCD(object):
#         ROIS = {
#             "id": (460, 330, 530, 80),
#             "name": (340, 460, 600, 50),
#             "birth_date": (735, 510, 215, 50),
#             "gender": (605, 570, 90, 40),
#             "nationality": (1030, 550, 190, 50),
#             "place_birth": (350, 660, 800, 50),
#             "address": [(860, 700, 300, 49), (370, 750, 835, 50)],
#         }

# def cropImageRoi(image, roi):
#     if isinstance(roi, list):
#         return [image[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] for r in roi]
#     elif isinstance(roi, tuple):
#         return image[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
#     else:
#         raise ValueError("ROI must be a tuple or a list of tuples.")

# @app.route('/extract_text', methods=['POST'])
# def extract_text():
#     try:
#         if 'image' not in request.files:
#             return jsonify({'error': 'No image file provided'}), 400

#         file = request.files['image']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400

#         file_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.jpg")
#         file.save(file_path)

#         img = cv2.imread(file_path)
#         if img is None:
#             return jsonify({'error': 'Could not decode image'}), 400

#         baseImg = cv2.imread(r'C:\Users\duong\Downloads\anhKhai.jpg')
#         baseH, baseW, baseC = baseImg.shape

#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         gray = cv2.GaussianBlur(gray, (3, 3), 0)
#         gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#         sift = cv2.SIFT_create()
#         kp1, des1 = sift.detectAndCompute(baseImg, None)
#         kp2, des2 = sift.detectAndCompute(img, None)

#         index_params = dict(algorithm=1, trees=5)
#         search_params = dict(checks=50)
#         flann = cv2.FlannBasedMatcher(index_params, search_params)
#         matches = flann.knnMatch(des1, des2, k=2)

#         good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]

#         if len(good_matches) < 4:
#             return jsonify({'error': 'Not enough good matches'}), 400

#         srcPoints = np.float32([kp2[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#         dstPoints = np.float32([kp1[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        
#         matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)
#         img_transformed = cv2.warpPerspective(img, matrix_relationship, (baseW, baseH))

#         gray_transformed = cv2.cvtColor(img_transformed, cv2.COLOR_BGR2GRAY)
#         gray_transformed = cv2.GaussianBlur(gray_transformed, (3, 3), 0)
#         gray_transformed = cv2.adaptiveThreshold(gray_transformed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

#         extracted_texts = {}
#         custom_config = r'--oem 3 --psm 6'
#         for key, roi_coords in ImageConstantROI.CCCD.ROIS.items():
#             cropped_imgs = cropImageRoi(gray_transformed, roi_coords)
#             if isinstance(cropped_imgs, list):
#                 text = [pytesseract.image_to_string(img, lang="vie", config=custom_config).strip() for img in cropped_imgs]
#                 extracted_texts[key] = ' '.join(text)
#             else:
#                 extracted_texts[key] = pytesseract.image_to_string(cropped_imgs, lang="vie", config=custom_config).strip()

#         return jsonify({'extracted_texts': extracted_texts})

#     except Exception as e:
#         return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)