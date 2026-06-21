import 'package:dio/dio.dart';
import '../config/app_config.dart';

class ApiClient {
  ApiClient._();

  static late final ApiClient instance;
  late final Dio dio;
  late final Dio aiDio;

  static void init() {
    instance = ApiClient._();
    instance._initDio();
  }

  void _initDio() {
    dio = Dio(BaseOptions(
      baseUrl: AppConfig.apiBaseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 30),
      sendTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    aiDio = Dio(BaseOptions(
      baseUrl: AppConfig.aiEngineUrl,
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 60),
      sendTimeout: const Duration(seconds: 60),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    ));

    dio.interceptors.add(_loggingInterceptor);
    aiDio.interceptors.add(_loggingInterceptor);
  }

  Interceptor get _loggingInterceptor => InterceptorsWrapper(
    onRequest: (options, handler) {
      if (AppConfig.isDebug) {
        print('[API] ${options.method} ${options.path}');
      }
      handler.next(options);
    },
    onResponse: (response, handler) {
      if (AppConfig.isDebug) {
        print('[API] ${response.statusCode} ${response.requestOptions.path}');
      }
      handler.next(response);
    },
    onError: (error, handler) {
      if (AppConfig.isDebug) {
        print('[API] ERROR ${error.response?.statusCode} ${error.requestOptions.path}');
      }
      handler.next(error);
    },
  );

  void setAuthToken(String token) {
    dio.options.headers['Authorization'] = 'Bearer $token';
    aiDio.options.headers['Authorization'] = 'Bearer $token';
  }

  void clearAuthToken() {
    dio.options.headers.remove('Authorization');
    aiDio.options.headers.remove('Authorization');
  }
}
