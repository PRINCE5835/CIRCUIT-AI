import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class BreadboardVerificationScreen extends ConsumerStatefulWidget {
  const BreadboardVerificationScreen({super.key});

  @override
  ConsumerState<BreadboardVerificationScreen> createState() => _BreadboardVerificationScreenState();
}

class _BreadboardVerificationScreenState extends ConsumerState<BreadboardVerificationScreen> {
  bool _isScanning = false;

  void _onScan() {
    setState(() => _isScanning = true);
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) setState(() => _isScanning = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Breadboard Verification')),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(DSDimensions.s24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.camera_alt_outlined, size: 80, color: DSColors.neonViolet),
              const SizedBox(height: DSDimensions.s24),
              Text(
                'Verify Your Breadboard',
                style: theme.textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: DSDimensions.s8),
              Text(
                'Take a photo of your breadboard layout and AI will verify the connections',
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: DSDimensions.s32),
              AppButton(
                label: _isScanning ? 'Scanning...' : 'Start Camera Scan',
                isFullWidth: true,
                isDisabled: _isScanning,
                isLoading: _isScanning,
                onPressed: _onScan,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
