import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class CostEstimationScreen extends ConsumerStatefulWidget {
  const CostEstimationScreen({super.key});

  @override
  ConsumerState<CostEstimationScreen> createState() => _CostEstimationScreenState();
}

class _CostEstimationScreenState extends ConsumerState<CostEstimationScreen> {
  final _componentsController = TextEditingController();
  bool _isEstimating = false;

  @override
  void dispose() {
    _componentsController.dispose();
    super.dispose();
  }

  void _onEstimate() {
    final text = _componentsController.text.trim();
    if (text.isEmpty) return;
    setState(() => _isEstimating = true);
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) setState(() => _isEstimating = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Cost Estimation')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DSDimensions.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: DSDimensions.s24),
            Icon(Icons.monetization_on_outlined, size: 64, color: DSColors.tertiary),
            const SizedBox(height: DSDimensions.s16),
            Text(
              'Estimate Component Costs',
              style: theme.textTheme.headlineSmall,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s8),
            Text(
              'List your components and get price estimates',
              style: theme.textTheme.bodyMedium?.copyWith(
                color: theme.colorScheme.onSurface.withValues(alpha: 0.6),
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s24),
            AppTextField(
              label: 'Components List',
              controller: _componentsController,
              maxLines: 5,
              hint: 'e.g.,\n- 5mm Red LED x10\n- 330Ω Resistor x20\n- Arduino Uno x1',
            ),
            const SizedBox(height: DSDimensions.s16),
            AppButton(
              label: _isEstimating ? 'Estimating...' : 'Estimate Cost',
              isFullWidth: true,
              isDisabled: _isEstimating,
              isLoading: _isEstimating,
              onPressed: _onEstimate,
            ),
          ],
        ),
      ),
    );
  }
}
