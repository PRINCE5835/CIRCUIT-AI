import 'package:dio/dio.dart';

sealed class AppException implements Exception {
  final String message;
  final String? code;

  AppException(this.message, {this.code});

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  final int? statusCode;

  NetworkException(super.message, {this.statusCode, super.code});

  factory NetworkException.fromDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return NetworkException('Connection timed out', code: 'TIMEOUT');
      case DioExceptionType.connectionError:
        return NetworkException('No internet connection', code: 'NO_INTERNET');
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final message = error.response?.data?['message'] ?? 'Server error';
        return NetworkException(message, statusCode: statusCode, code: 'BAD_RESPONSE');
      case DioExceptionType.cancel:
        return NetworkException('Request cancelled', code: 'CANCELLED');
      default:
        return NetworkException('An unexpected error occurred', code: 'UNKNOWN');
    }
  }
}

class AuthException extends AppException {
  AuthException(super.message, {super.code});
}

class ValidationException extends AppException {
  final Map<String, String>? errors;

  ValidationException(super.message, {this.errors, super.code});
}

class CacheException extends AppException {
  CacheException(super.message, {super.code});
}

class AudioException extends AppException {
  AudioException(super.message, {super.code});
}

class VoiceException extends AppException {
  VoiceException(super.message, {super.code});
}

class VisionException extends AppException {
  VisionException(super.message, {super.code});
}

class CircuitException extends AppException {
  CircuitException(super.message, {super.code});
}
