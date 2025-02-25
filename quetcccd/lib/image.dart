
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:quetcccd/cccdscant.dart';

void main() {
  runApp(GridListDemo());
}

class GridListDemo extends StatefulWidget {
  @override
  _GridListDemoState createState() => _GridListDemoState();
}

class _GridListDemoState extends State<GridListDemo> {
  File? _image;
  Map<String, dynamic>? _extractedData; // Đổi từ String sang Map

  Future<void> _uploadImage(File image) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('http://192.168.1.33:8000/api/upload_cccd'),
    );

    request.files.add(await http.MultipartFile.fromPath('image', image.path));
    var response = await request.send();

    if (response.statusCode == 200) {
      var jsonResponse = jsonDecode(await response.stream.bytesToString());
      setState(() {
        _extractedData = jsonResponse['extracted_texts']; // Chuyển thành Map
      });
      print("Ảnh đã gửi thành công, dữ liệu nhận về: $_extractedData");
    } else {
      setState(() {
        _extractedData = null;
      });
      print("Lỗi khi gửi ảnh, mã lỗi: ${response.statusCode}");
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("OCR Application")),
        body: Column(
          children: [
            Container(
              height: 300,
              width: 300,
              child: _image != null
                  ? Image.file(_image!, fit: BoxFit.contain)
                  : Text("Please take a photo of front ID card"),
            ),
            ElevatedButton(
              onPressed: () async {
                final imagePath = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => CameraScreen()),
                );

                if (imagePath != null) {
                  File imageFile = File(imagePath);
                  setState(() {
                    _image = imageFile;
                  });

                  await _uploadImage(imageFile);
                }
              },
              child: Text("Take Photo"),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: _extractedData != null
                  ? _buildFormattedText(_extractedData!)
                  : Text("Không có dữ liệu"),
            ),
          ],
        ),
      ),
    );
  }

  /// Hiển thị dữ liệu dưới dạng danh sách có format rõ ràng
  Widget _buildFormattedText(Map<String, dynamic> data) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildTextRow("Mã CCCD", data["id"]),
        _buildTextRow("Tên CCCD", data["name"]),
        _buildTextRow("Giới tính", data["gender"]),
        _buildTextRow("Ngày sinh", data["birth_date"]),
        _buildTextRow("Quốc tịch", data["nationality"]),
        _buildTextRow("Nơi sinh", data["place_birth"]),
        _buildTextRow("Địa chỉ", data["address"]),
      ],
    );
  }

  Widget _buildTextRow(String title, String? value) {
    return Padding(
      padding: EdgeInsets.symmetric(vertical: 4),
      child: Text(
        "$title: ${value ?? 'Không có dữ liệu'}",
        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
      ),
    );
  }
}
