import 'dart:async';
import 'dart:convert';
import 'dart:math';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image/image.dart' as img; 
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isCameraInitialized = false;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    _cameras = await availableCameras();
    _controller = CameraController(_cameras!.first, ResolutionPreset.high);
    // _controller = CameraController(_cameras!.first, ResolutionPreset.max);
    // await _controller!.setFocusMode(FocusMode.auto);
    await _controller!.initialize();
    setState(() {
      _isCameraInitialized = true;
    });
  }

// Future<void> _sendToServer(File imageFile) async {
//   try {
//     var client = http.Client();
//     var request = http.MultipartRequest(
//       'POST',
//       Uri.parse("http://10.3.251.68:5000/extract_text"),
//     );

//     request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));

//     var response = await client.send(request).timeout(Duration(seconds: 60));

//     if (!mounted) return; // Kiểm tra nếu widget đã bị unmounted, không tiếp tục

//     if (response.statusCode == 200) {
//       String responseBody = await response.stream.bytesToString();
//       Map<String, dynamic> extractedData = json.decode(responseBody);
//       print("Dữ liệu trích xuất: $extractedData");

//       ScaffoldMessenger.of(context).showSnackBar(
//         SnackBar(content: Text("Ảnh đã gửi thành công!"))
//       );
//     } else {
//       print("Lỗi khi gửi ảnh lên server! Mã lỗi: ${response.statusCode}");

//       ScaffoldMessenger.of(context).showSnackBar(
//         SnackBar(content: Text("Lỗi gửi ảnh!"))
//       );
//     }
//   } on TimeoutException catch (_) {
//     print("Lỗi: Quá thời gian chờ");

//     if (!mounted) return; // Kiểm tra nếu widget đã bị unmounted
//     ScaffoldMessenger.of(context).showSnackBar(
//       SnackBar(content: Text("Lỗi: Quá thời gian chờ"))
//     );
//   } catch (e) {
//     print("Lỗi khi gửi ảnh: $e");

//     if (!mounted) return; // Kiểm tra nếu widget đã bị unmounted
//     ScaffoldMessenger.of(context).showSnackBar(
//       SnackBar(content: Text("Lỗi gửi ảnh!"))
//     );
//   }
// }
Future<void> _sendToServer(File imageFile) async {
  try {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse("http://192.168.1.33:8000/api/upload_cccd") // Laravel API mới
    );

    request.files.add(await http.MultipartFile.fromPath('image', imageFile.path));

    var response = await request.send();

    if (response.statusCode == 200) {
      String responseBody = await response.stream.bytesToString();
      Map<String, dynamic> responseData = json.decode(responseBody);
      
      if (responseData.containsKey('image_url')) {
        String imageUrl = responseData['image_url'];
        print("Ảnh đã lưu trên Laravel: $imageUrl");
      } else {
        print("Lỗi: Không nhận được đường dẫn ảnh từ Laravel!");
      }
    } else {
      print("Lỗi gửi ảnh lên Laravel: ${response.statusCode}");
    }
  } catch (e) {
    print("Lỗi khi gửi ảnh lên Laravel: $e");
  }
}

Future<void> _takePicture() async {
  try {
    final image = await _controller!.takePicture();
    print("Ảnh gốc: ${image.path}");

    File? croppedImage = await _cropImage(image.path);

    if (croppedImage != null) {
      print("Ảnh đã cắt: ${croppedImage.path}");

      String imagePath = croppedImage.path;

      // Pop màn hình trước, rồi gửi ảnh lên server sau đó
      Navigator.pop(context, imagePath);

      Future.microtask(() => _sendToServer(File(imagePath)));
    } else {
      print("Lỗi: Ảnh cắt bị null!");
    }
  } catch (e) {
    print("Lỗi khi chụp hoặc xử lý ảnh: $e");
  }
}





// Cắt ảnh theo khung
Future<File?> _cropImage(String imagePath) async {
  // Load ảnh từ file
  final img.Image image = img.decodeImage(File(imagePath).readAsBytesSync())!;

  // Vị trí và kích thước của khung (bắt đầu từ tỉ lệ màn hình)
  double screenWidth = MediaQuery.of(context).size.width;
  double screenHeight = MediaQuery.of(context).size.height;

  // Kích thước và vị trí của khung màu đỏ
  double overlayWidth = screenWidth * 0.8; // Khung chiếm 80% chiều rộng màn hình
  double overlayHeight = overlayWidth / 1.585; // Giữ đúng tỉ lệ CCCD

  // Khoảng cách từ trên xuống cho khung
  double topOffset = screenHeight * 0.2;

  // Tính toán vị trí và kích thước chính xác của ảnh (theo tỉ lệ màn hình)
  int x = (screenWidth * 0.1).toInt(); // X = 10% chiều rộng màn hình
  int y = (topOffset * image.height / screenHeight).toInt(); // Tính toán y từ tỉ lệ chiều cao của ảnh
  int width = (overlayWidth * image.width / screenWidth).toInt(); // Tính toán width
  int height = (overlayHeight * image.height / screenHeight).toInt(); // Tính toán height

  // Phóng to vùng cắt lên 10% (hoặc theo hệ số bạn muốn)
  double zoomFactor = 1.1; // Phóng to lên 10%
  width = (width * zoomFactor).toInt();
  height = (height * zoomFactor).toInt();

  // Giả sử bạn đã có thông tin về góc nghiêng của ảnh (ví dụ qua cảm biến hoặc từ camera)
  double angle = 5.0; // Ví dụ, giả sử góc nghiêng là 5 độ (bạn có thể thay đổi giá trị này hoặc lấy từ dữ liệu cảm biến)

  // Chuyển góc nghiêng sang radians
  double radians = angle * pi / 180;

  // Tính toán ma trận xoay (rotation matrix) để điều chỉnh khung cắt
  double cosAngle = cos(radians);
  double sinAngle = sin(radians);

  // Áp dụng ma trận xoay vào các điểm cắt (điều chỉnh x, y, width, height)
  int rotatedX = (x * cosAngle - y * sinAngle).toInt();
  int rotatedY = (x * sinAngle + y * cosAngle).toInt();
  int rotatedWidth = (width * cosAngle - height * sinAngle).toInt();
  int rotatedHeight = (width * sinAngle + height * cosAngle).toInt();

  // Phóng to vùng cắt thêm 10% để bù đắp khi nghiêng
  rotatedWidth = (rotatedWidth * zoomFactor).toInt();
  rotatedHeight = (rotatedHeight * zoomFactor).toInt();

  // In ra giá trị kiểm tra để debug
  print('Rotated x: $rotatedX, y: $rotatedY, width: $rotatedWidth, height: $rotatedHeight');
  print('image.width: ${image.width}, image.height: ${image.height}');

  // Cắt ảnh theo vị trí và kích thước đã tính toán sau khi xoay
  img.Image cropped = img.copyCrop(image, rotatedX, rotatedY, rotatedWidth, rotatedHeight);

  // Lưu ảnh đã cắt ra file mới
  final directory = await Directory.systemTemp.createTemp();
  final newImagePath = '${directory.path}/cropped_image.jpg';
  File(newImagePath)..writeAsBytesSync(img.encodeJpg(cropped));

  return File(newImagePath);
}

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Quét CCCD')),
      body: _isCameraInitialized
          ? Stack(
              children: [
                CameraPreview(_controller!),
                _buildCCCDOverlay(), // Hiển thị khung CCCD
                Align(
                  alignment: Alignment.bottomCenter,
                  child: Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: FloatingActionButton(
                      onPressed: _takePicture,
                      child: Icon(Icons.camera),
                    ),
                  ),
                ),
              ],
            )
          : Center(child: CircularProgressIndicator()),
    );
  }

  // Tạo overlay khung CCCD
  Widget _buildCCCDOverlay() {
    double screenWidth = MediaQuery.of(context).size.width;
    double overlayWidth = screenWidth * 0.8; // Khung chiếm 80% chiều rộng màn hình
    double overlayHeight = overlayWidth / 1.585; // Giữ đúng tỉ lệ CCCD

    return Positioned(
      top: MediaQuery.of(context).size.height * 0.2, // Khoảng cách từ trên xuống
      left: (screenWidth - overlayWidth) / 2, // Căn giữa khung
      child: Container(
        width: overlayWidth,
        height: overlayHeight,
        decoration: BoxDecoration(
          border: Border.all(color: Colors.red, width: 3),
          borderRadius: BorderRadius.circular(15), // Bo góc theo chuẩn CCCD
          color: Colors.transparent,
        ),
      ),
    );
  }
}

