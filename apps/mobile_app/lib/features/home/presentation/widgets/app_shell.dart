import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import 'package:dio/dio.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class AppShell extends ConsumerStatefulWidget {
  final Widget child;
  const AppShell({super.key, required this.child});

  @override
  ConsumerState<AppShell> createState() => _AppShellState();
}

class _AppShellState extends ConsumerState<AppShell> {
  static final _tabs = [
    _ShellTabData(Icons.home_outlined, Icons.home, RoutePaths.home, 'Home'),
    _ShellTabData(Icons.mic_outlined, Icons.mic, RoutePaths.voice, 'Voice'),
    _ShellTabData(Icons.qr_code_scanner, Icons.qr_code_scanner, RoutePaths.componentDetection, 'Scan'),
    _ShellTabData(Icons.store_outlined, Icons.store, RoutePaths.marketplace, 'Market'),
    _ShellTabData(Icons.person_outlined, Icons.person, RoutePaths.profile, 'Profile'),
  ];

  int _currentIndex(String location) {
    for (var i = 0; i < _tabs.length; i++) {
      if (location.startsWith(_tabs[i].path)) return i;
    }
    return 0;
  }

  Future<void> _scanComponent() async {
    try {
      final picker = ImagePicker();
      final XFile? image = await picker.pickImage(source: ImageSource.camera);
      if (image == null || !mounted) return;

      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => const Center(child: CircuitSpinner(size: 48)),
      );

      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(image.path, filename: image.name),
      });
      final response = await ApiClient.instance.dio.post(
        ApiEndpoints.aiVisionDetect,
        data: formData,
      );

      if (mounted) Navigator.of(context).pop();

      final result = response.data;
      final components = result['components'] as List<dynamic>? ?? [result];

      if (!mounted) return;
      _showResults(components);
    } catch (e) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Scan failed: ${e.toString()}')),
        );
      }
    }
  }

  void _showResults(List<dynamic> components) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(DSDimensions.sheetRadius)),
      ),
      builder: (ctx) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(DSDimensions.s16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: DSDimensions.sheetHandleWidth,
                  height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.shade300,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: DSDimensions.s16),
              Text('Detected Components', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
              const SizedBox(height: DSDimensions.s12),
              ...components.map((c) {
                final cMap = c as Map<String, dynamic>;
                final name = cMap['name'] as String? ?? 'Unknown';
                final confidence = cMap['confidence'] as num?;
                return ListTile(
                  leading: const Icon(Icons.memory, color: DSColors.circuitCyan),
                  title: Text(name),
                  subtitle: confidence != null ? Text('${(confidence * 100).toStringAsFixed(0)}% confidence') : null,
                );
              }),
              const SizedBox(height: DSDimensions.s8),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).uri.toString();
    final selectedIndex = _currentIndex(location);

    return Scaffold(
      body: widget.child,
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedIndex,
        onDestinationSelected: (i) {
          if (_tabs[i].path == RoutePaths.componentDetection) {
            _scanComponent();
          } else {
            context.go(_tabs[i].path);
          }
        },
        destinations: _tabs
            .map((t) => NavigationDestination(
                  icon: Icon(t.icon),
                  selectedIcon: Icon(t.selectedIcon),
                  label: t.label,
                ))
            .toList(),
      ),
    );
  }
}

class _ShellTabData {
  final IconData icon;
  final IconData selectedIcon;
  final String path;
  final String label;
  const _ShellTabData(this.icon, this.selectedIcon, this.path, this.label);
}
