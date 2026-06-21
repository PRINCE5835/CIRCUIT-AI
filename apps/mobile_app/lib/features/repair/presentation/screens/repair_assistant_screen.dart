import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class RepairAssistantScreen extends ConsumerStatefulWidget {
  const RepairAssistantScreen({super.key});

  @override
  ConsumerState<RepairAssistantScreen> createState() => _RepairAssistantScreenState();
}

class _RepairAssistantScreenState extends ConsumerState<RepairAssistantScreen> {
  final _descriptionController = TextEditingController();
  bool _isAnalyzing = false;

  @override
  void dispose() {
    _descriptionController.dispose();
    super.dispose();
  }

  void _onAnalyze() {
    final text = _descriptionController.text.trim();
    if (text.isEmpty) return;
    setState(() => _isAnalyzing = true);
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _isAnalyzing = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Repair Assistant')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DSDimensions.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: DSDimensions.s24),
            Icon(Icons.build_circle_outlined, size: 64, color: DSColors.warmAmber),
            const SizedBox(height: DSDimensions.s16),
            Text(
              'Describe the Issue',
              style: theme.textTheme.headlineSmall,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s8),
            Text(
              'Tell us what\'s wrong with your circuit',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s24),
            AppTextField(
              label: 'Issue Description',
              controller: _descriptionController,
              maxLines: 5,
              hint: 'e.g., My LED is not lighting up even though I connected everything correctly...',
            ),
            const SizedBox(height: DSDimensions.s16),
            AppButton(
              label: _isAnalyzing ? 'Analyzing...' : 'Analyze Issue',
              isFullWidth: true,
              isDisabled: _isAnalyzing,
              isLoading: _isAnalyzing,
              onPressed: _onAnalyze,
            ),
          ],
        ),
      ),
    );
  }
}
