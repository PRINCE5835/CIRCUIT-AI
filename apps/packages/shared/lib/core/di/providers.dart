import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../network/api_client.dart';

final dioClientProvider = Provider((ref) => ApiClient.instance);

final authStateProvider = StateProvider<bool>((ref) => false);

final isLoadingProvider = StateProvider<bool>((ref) => false);
