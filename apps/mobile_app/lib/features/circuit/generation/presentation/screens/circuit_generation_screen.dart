import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import '../../../../../core/services/api_service.dart';

class CircuitGenerationScreen extends ConsumerStatefulWidget {
  const CircuitGenerationScreen({super.key});

  @override
  ConsumerState<CircuitGenerationScreen> createState() => _CircuitGenerationScreenState();
}

class _CircuitGenerationScreenState extends ConsumerState<CircuitGenerationScreen> {
  final _promptController = TextEditingController();
  bool _isGenerating = false;
  Map<String, dynamic>? _result;

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  Future<void> _onGenerate() async {
    final prompt = _promptController.text.trim();
    if (prompt.isEmpty) return;
    setState(() {
      _isGenerating = true;
      _result = null;
    });
    try {
      final result = await ApiService.aiGenerateCircuit(prompt);
      if (mounted) setState(() => _result = result);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    }
    if (mounted) setState(() => _isGenerating = false);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Circuit Generation')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DSDimensions.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: DSDimensions.s24),
            Icon(Icons.circle_outlined, size: 64, color: DSColors.circuitCyan),
            const SizedBox(height: DSDimensions.s16),
            Text(
              'Describe your circuit',
              style: theme.textTheme.headlineSmall,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s8),
            Text(
              'Tell me what you want to build in natural language',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s24),
            AppTextField(
              label: 'Circuit Description',
              controller: _promptController,
              maxLines: 5,
              hint: 'e.g., Create a blinking LED circuit with a 555 timer...',
            ),
            const SizedBox(height: DSDimensions.s16),
            AppButton(
              label: _isGenerating ? 'Generating...' : 'Generate Circuit',
              isFullWidth: true,
              isLoading: _isGenerating,
              onPressed: _isGenerating ? null : _onGenerate,
            ),
            if (_result != null) ...[
              const SizedBox(height: DSDimensions.s24),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(DSDimensions.s16),
                  child: Text(
                    _result!['response'] as String? ?? _result.toString(),
                    style: theme.textTheme.bodyMedium,
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
