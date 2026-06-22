import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class SafetyValidationScreen extends ConsumerStatefulWidget {
  const SafetyValidationScreen({super.key});

  @override
  ConsumerState<SafetyValidationScreen> createState() => _SafetyValidationScreenState();
}

class _SafetyValidationScreenState extends ConsumerState<SafetyValidationScreen> {
  final _descriptionController = TextEditingController();
  bool _isValidating = false;

  @override
  void dispose() {
    _descriptionController.dispose();
    super.dispose();
  }

  void _onValidate() {
    final text = _descriptionController.text.trim();
    if (text.isEmpty) return;
    setState(() => _isValidating = true);
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _isValidating = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Safety Validation')),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 500),
          padding: EdgeInsets.all(isWide ? 48 : 16),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 24),
                Icon(Icons.shield_outlined, size: 64, color: DSColors.safe),
                const SizedBox(height: 16),
                Text(
                  'Safety Check',
                  style: Theme.of(context).textTheme.headlineSmall,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'Describe your circuit for a safety analysis',
                  style: TextStyle(
                    color: isDark ? DSColors.grey400 : DSColors.grey500,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 24),
                TextField(
                  controller: _descriptionController,
                  maxLines: 6,
                  style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900),
                  decoration: InputDecoration(
                    labelText: 'Circuit Description',
                    hintText: 'Describe your circuit components and connections...',
                    hintStyle: TextStyle(fontSize: 13, color: isDark ? DSColors.grey500 : DSColors.grey400),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    alignLabelWithHint: true,
                  ),
                ),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: _isValidating ? null : _onValidate,
                  icon: _isValidating
                      ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.verified_outlined),
                  label: Text(_isValidating ? 'Validating...' : 'Run Safety Check'),
                  style: FilledButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
