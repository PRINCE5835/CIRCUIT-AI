import 'package:flutter_riverpod/flutter_riverpod.dart';

// Feature-level providers will be registered here as they are built.
// Each feature gets its own provider scope.

final featureProviders = <String, ProviderOrFamily>{};

typedef ProviderOrFamily = Object;
