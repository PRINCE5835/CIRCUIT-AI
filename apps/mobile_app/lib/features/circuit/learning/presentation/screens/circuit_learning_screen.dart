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
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Circuit Learning')),
      body: ListView.builder(
        padding: const EdgeInsets.all(DSDimensions.s16),
        itemCount: _topics.length,
        itemBuilder: (context, index) {
          final topic = _topics[index];
          return Padding(
            padding: const EdgeInsets.only(bottom: DSDimensions.s12),
            child: AppCard(
              onTap: () => context.go(RoutePaths.voice),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: topic.color.withValues(alpha: 0.15),
                  child: Icon(topic.icon, color: topic.color),
                ),
                title: Text(topic.title, style: theme.textTheme.titleMedium),
                subtitle: Text(topic.description, style: theme.textTheme.bodySmall),
                trailing: const Icon(Icons.chevron_right),
              ),
            ),
          );
        },
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
