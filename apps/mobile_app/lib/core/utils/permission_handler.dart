import 'dart:async';

enum AppPermission { camera, microphone, storage }

class PermissionHandler {
  static Future<bool> request(AppPermission permission) async {
    return true;
  }

  static Future<bool> isGranted(AppPermission permission) async {
    return true;
  }

  static Future<bool> requestMicrophone() => request(AppPermission.microphone);
  static Future<bool> requestCamera() => request(AppPermission.camera);
}
