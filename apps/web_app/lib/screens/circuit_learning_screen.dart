import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class CircuitLearningScreen extends ConsumerWidget {
  const CircuitLearningScreen({super.key});

  static final _topics = [
    _Topic("Ohm's Law", 'Understand voltage, current, and resistance', Icons.electric_bolt, DSColors.circuitCyan),
    _Topic('LED Circuits', 'Learn to light up LEDs with resistors', Icons.emoji_objects_outlined, DSColors.neonViolet),
    _Topic('555 Timer', 'Master the classic timer IC', Icons.timer_outlined, DSColors.warmAmber),
    _Topic('Transistors', 'Switching and amplification basics', Icons.memory, DSColors.neonViolet),
    _Topic('Arduino 101', 'Getting started with microcontrollers', Icons.developer_board, DSColors.tertiary),
    _Topic('Sensors', 'Working with input devices', Icons.sensors, DSColors.neonCoral),
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Circuit Learning')),
      body: Center(
        child: Container(
          constraints: const BoxConstraints(maxWidth: 700),
          padding: EdgeInsets.all(isWide ? 48 : 16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Learn Electronics', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
              const SizedBox(height: 4),
              Text('Interactive tutorials to get you started',
                  style: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500)),
              const SizedBox(height: 24),
              Expanded(
                child: ListView.separated(
                  itemCount: _topics.length,
                  separatorBuilder: (_, __) => const SizedBox(height: 12),
                  itemBuilder: (context, index) {
                    final topic = _topics[index];
                    return Container(
                      decoration: BoxDecoration(
                        color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
                      ),
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        leading: CircleAvatar(
                          backgroundColor: topic.color.withValues(alpha: 0.15),
                          child: Icon(topic.icon, color: topic.color),
                        ),
                        title: Text(topic.title, style: Theme.of(context).textTheme.titleMedium),
                        subtitle: Text(topic.description, style: Theme.of(context).textTheme.bodySmall),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: () => context.go(RoutePaths.voice),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Topic {
  final String title;
  final String description;
  final IconData icon;
  final Color color;
  const _Topic(this.title, this.description, this.icon, this.color);
}
