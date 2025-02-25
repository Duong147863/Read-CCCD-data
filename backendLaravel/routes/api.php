<?php

use App\Http\Controllers\CCCDController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
//     return $request->user();
// });

Route::post('/upload_cccd', [CCCDController::class, 'uploadCCCD']);