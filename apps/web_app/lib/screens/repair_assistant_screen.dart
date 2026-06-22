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
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Repair Assistant')),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 500),
          padding: EdgeInsets.all(isWide ? 48 : 16),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 24),
                Icon(Icons.build_circle_outlined, size: 64, color: DSColors.warmAmber),
                const SizedBox(height: 16),
                Text(
                  'Describe the Issue',
                  style: Theme.of(context).textTheme.headlineSmall,
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Text(
                  "Tell us what's wrong with your circuit",
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
                    labelText: 'Issue Description',
                    hintText: 'e.g., My LED is not lighting up even though I connected everything correctly...',
                    hintStyle: TextStyle(fontSize: 13, color: isDark ? DSColors.grey500 : DSColors.grey400),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                    alignLabelWithHint: true,
                  ),
                ),
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: _isAnalyzing ? null : _onAnalyze,
                  icon: _isAnalyzing
                      ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Icon(Icons.troubleshoot),
                  label: Text(_isAnalyzing ? 'Analyzing...' : 'Analyze Issue'),
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
