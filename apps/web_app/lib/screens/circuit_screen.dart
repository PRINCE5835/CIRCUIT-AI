import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/shared/design_system/colors.dart';

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
    await Future.delayed(const Duration(seconds: 2));
    if (mounted) {
      setState(() {
        _result = 'Circuit: LED Blinker\n\n'
            'Components:\n• 1x LED\n• 1x 220Ω Resistor\n• 1x 555 Timer IC\n'
            '• 2x 10kΩ Resistors\n• 2x 100µF Capacitors\n• 1x Breadboard\n• 1x 5V Power Supply\n\n'
            'Steps:\n1. Place 555 timer in center of breadboard\n'
            '2. Connect pin 8 to VCC, pin 1 to GND\n'
            '3. Connect 10kΩ between pin 7 and VCC\n'
            '4. Connect 100µF from pin 2 to GND\n'
            '5. Connect 220Ω + LED from pin 3 to GND\n\n'
            'Estimated Cost: ₹45-60';
        _isGenerating = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;
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
                            Text('Circuit Generated', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
                          ],
                        ),
                        const SizedBox(height: 16),
                        Text(_result!, style: TextStyle(fontSize: 14, height: 1.6, color: isDark ? DSColors.grey100 : DSColors.grey900)),
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
