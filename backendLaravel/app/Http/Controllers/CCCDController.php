<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;
class CCCDController extends Controller
{
    public function uploadCCCD(Request $request)
    {
        try {
            if (!$request->hasFile('image')) {
                return response()->json(['error' => 'No image file provided'], 400);
            }
    
            $file = $request->file('image');
            if (!$file->isValid()) {
                return response()->json(['error' => 'Invalid image file'], 400);
            }
    
            // Đặt tên cố định
            $fileName = 'cropped_image.jpg';
            $path = $file->storeAs('cccd_images', $fileName, 'public'); 
            $imageUrl = asset('storage/' . $path); 
    
            // Gửi ảnh đến Flask bằng multipart/form-data
            $response = Http::attach('image', file_get_contents($file), $fileName)
                ->post('http://192.168.1.33:5000/extract_text');
    
            return response()->json([
                'message' => 'Upload thành công',
                'image_url' => $imageUrl,
                'python_response' => $response->json()
            ], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }
    
}
