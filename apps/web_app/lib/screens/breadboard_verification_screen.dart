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
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Breadboard Verification')),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 500),
          padding: EdgeInsets.all(isWide ? 48 : 24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.camera_alt_outlined, size: 80, color: DSColors.neonViolet),
              const SizedBox(height: 24),
              Text(
                'Verify Your Breadboard',
                style: Theme.of(context).textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                'Take a photo of your breadboard layout and AI will verify the connections',
                style: TextStyle(
                  color: isDark ? DSColors.grey400 : DSColors.grey500,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              FilledButton.icon(
                onPressed: _isScanning ? null : _onScan,
                icon: _isScanning
                    ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : const Icon(Icons.camera_alt),
                label: Text(_isScanning ? 'Scanning...' : 'Start Camera Scan'),
                style: FilledButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
