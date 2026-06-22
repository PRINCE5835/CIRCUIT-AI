import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import 'package:breadboard_shared/breadboard_shared.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../widgets/circuit_visualizer.dart';

class CircuitScreen extends ConsumerStatefulWidget {
  const CircuitScreen({super.key});

  @override
  ConsumerState<CircuitScreen> createState() => _CircuitScreenState();
}

class _CircuitScreenState extends ConsumerState<CircuitScreen> {
  final _controller = TextEditingController();
  String? _result;
  bool _isGenerating = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _generate() async {
    final prompt = _controller.text.trim();
    if (prompt.isEmpty) return;
    setState(() { _isGenerating = true; _result = null; });

    try {
      final response = await ApiClient.instance.dio.post(
        ApiEndpoints.aiCircuitGenerate,
        data: {'description': prompt},
        options: Options(
          receiveTimeout: const Duration(seconds: 120),
          sendTimeout: const Duration(seconds: 60),
        ),
      );
      final data = response.data;
      final reply = data['response'] as String? ?? 'No response generated';

      if (mounted) {
        setState(() {
          _result = reply;
          _isGenerating = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _result = 'Error: ${e.toString().replaceFirst('Exception: ', '')}';
          _isGenerating = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    final mdStyle = MarkdownStyleSheet(
      h1: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      h2: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      h3: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      p: TextStyle(fontSize: 14, height: 1.6, color: isDark ? DSColors.grey100 : DSColors.grey900),
      code: TextStyle(
        fontSize: 13, backgroundColor: isDark ? DSColors.surfaceDarkVariant : DSColors.grey100,
        color: isDark ? DSColors.circuitCyan : DSColors.neonViolet,
      ),
      codeblockDecoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkVariant : DSColors.grey100,
        borderRadius: BorderRadius.circular(8),
      ),
      codeblockPadding: const EdgeInsets.all(12),
      blockquoteDecoration: BoxDecoration(
        border: Border(left: BorderSide(color: DSColors.circuitCyan, width: 3)),
        color: isDark ? DSColors.circuitCyan.withValues(alpha: 0.08) : DSColors.circuitCyan.withValues(alpha: 0.05),
      ),
      blockquotePadding: const EdgeInsets.fromLTRB(12, 4, 8, 4),
      tableHead: TextStyle(fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      tableBody: TextStyle(color: isDark ? DSColors.grey100 : DSColors.grey900),
      tableBorder: TableBorder.all(color: isDark ? DSColors.grey600 : DSColors.grey300),
      tableColumnWidth: const FlexColumnWidth(),
      horizontalRuleDecoration: BoxDecoration(border: Border(top: BorderSide(color: isDark ? DSColors.grey600 : DSColors.grey300))),
      strong: TextStyle(fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      a: TextStyle(color: DSColors.circuitCyan, decoration: TextDecoration.underline),
    );

    return Scaffold(
      appBar: AppBar(title: const Text('Circuit Generator')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(isWide ? 48 : 16),
        child: Center(
          child: Container(
            constraints: const BoxConstraints(maxWidth: 700),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Describe your circuit', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 8),
                Text('Tell me what you want to build and I\'ll generate the schematic', style: TextStyle(color: isDark ? DSColors.grey300 : DSColors.grey600)),
                const SizedBox(height: 24),
                TextField(
                  controller: _controller,
                  maxLines: 3,
                  style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900),
                  decoration: InputDecoration(
                    hintText: 'e.g. "Make an LED blink with a 555 timer"',
                    hintStyle: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _isGenerating ? null : _generate,
                    icon: _isGenerating
                        ? const SizedBox(width: 18, height: 18, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                        : const Icon(Icons.auto_awesome),
                    label: Text(_isGenerating ? 'Generating...' : 'Generate Circuit'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: DSColors.primary,
                      foregroundColor: DSColors.onPrimary,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                ),
                if (_result != null) ...[
                  const SizedBox(height: 24),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      gradient: isDark
                          ? LinearGradient(colors: [DSColors.surfaceDarkCard, DSColors.surfaceDarkVariant])
                          : LinearGradient(colors: [DSColors.grey50, DSColors.white]),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: DSColors.circuitCyan.withValues(alpha: 0.3)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(Icons.check_circle, color: DSColors.circuitCyan, size: 24),
                            const SizedBox(width: 8),
                            Text('Generated Circuit', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
                          ],
                        ),
                        const SizedBox(height: 16),
                        MarkdownBody(
                          data: _result!,
                          styleSheet: mdStyle,
                          selectable: true,
                        ),
                        const SizedBox(height: 8),
                        CircuitVisualizer(markdown: _result!),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
