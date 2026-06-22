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
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Cost Estimation')),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 500),
          padding: EdgeInsets.all(isWide ? 48 : 16),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 24),
                Icon(Icons.monetization_on_outlined, size: 64, color: DSColors.tertiary),
                const SizedBox(height: 16),
                Text(
                  'Estimate Component Costs',
                  style: Theme.of(context).textTheme.headlineSmall,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  'List your components and get price estimates',
                  style: TextStyle(
                    color: isDark ? DSColors.grey400 : DSColors.grey500,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 24),
                TextField(
                  controller: _componentsController,
                  maxLines: 6,
                  style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900),
                  decoration: InputDecoration(
                    labelText: 'Components List',
                    hintText: 'e.g.,\n- 5mm Red LED x10\n- 330Ω Resistor x20\n- Arduino Uno x1',
                    hintStyle: TextStyle(fontSize: 13, color: isDark ? DSColors.grey500 : DSColors.grey400),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    alignLabelWithHint: true,
                  ),
                ),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: _isEstimating ? null : _onEstimate,
                  icon: _isEstimating
                      ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.calculate_outlined),
                  label: Text(_isEstimating ? 'Estimating...' : 'Estimate Cost'),
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
