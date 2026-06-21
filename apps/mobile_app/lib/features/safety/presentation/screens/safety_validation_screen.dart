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
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Safety Validation')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DSDimensions.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: DSDimensions.s24),
            Icon(Icons.shield_outlined, size: 64, color: DSColors.safe),
            const SizedBox(height: DSDimensions.s16),
            Text(
              'Safety Check',
              style: theme.textTheme.headlineSmall,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s8),
            Text(
              'Describe your circuit for a safety analysis',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s24),
            AppTextField(
              label: 'Circuit Description',
              controller: _descriptionController,
              maxLines: 5,
              hint: 'Describe your circuit components and connections...',
            ),
            const SizedBox(height: DSDimensions.s16),
            AppButton(
              label: _isValidating ? 'Validating...' : 'Run Safety Check',
              isFullWidth: true,
              isDisabled: _isValidating,
              isLoading: _isValidating,
              onPressed: _onValidate,
            ),
          ],
        ),
      ),
    );
  }
}
