import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class MarketplaceScreen extends ConsumerWidget {
  const MarketplaceScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;
    final products = [
      _Product('Arduino Uno R3', 'Development Board', 'ATmega328P', 650, DSColors.circuitCyan,
          'https://via.placeholder.com/150?text=Arduino+Uno'),
      _Product('Breadboard 830pt', 'Prototyping Board', '830 tie points', 120, DSColors.neonViolet,
          'https://via.placeholder.com/150?text=Breadboard'),
      _Product('LED Assorted Kit', 'LEDs', '100pcs 5mm LEDs', 85, DSColors.warmAmber,
          'https://via.placeholder.com/150?text=LED+Kit'),
      _Product('Resistor Kit', 'Resistors', '500pcs 1/4W', 99, DSColors.circuitCyan,
          'https://via.placeholder.com/150?text=Resistor+Kit'),
      _Product('Jumper Wires', 'Wires', '120pcs M-M/M-F/F-M', 149, DSColors.neonGreen,
          'https://via.placeholder.com/150?text=Jumper+Wires'),
      _Product('555 Timer IC', 'IC', 'NE555P DIP-8', 25, DSColors.neonViolet,
          'https://via.placeholder.com/150?text=555+Timer'),
      _Product('LM393 Sensor', 'Sensor', 'Speed Sensor Module', 45, DSColors.warmAmber,
          'https://via.placeholder.com/150?text=LM393+Sensor'),
      _Product('Battery Holder', 'Power', '4xAA with switch', 35, DSColors.neonCoral,
          'https://via.placeholder.com/150?text=Battery+Holder'),
      _Product('Capacitor Kit', 'Capacitors', '50pcs ceramic + electrolytic', 75, DSColors.neonViolet,
          'https://via.placeholder.com/150?text=Capacitor+Kit'),
      _Product('Potentiometer', 'Variable Resistor', '10kΩ + 100kΩ pack', 40, DSColors.warmAmber,
          'https://via.placeholder.com/150?text=Potentiometer'),
      _Product('NPN Transistor', 'Transistors', 'BC547 pack of 10', 30, DSColors.circuitCyan,
          'https://via.placeholder.com/150?text=NPN+Transistor'),
      _Product('LCD Display', 'Display', '16x2 I2C module', 180, DSColors.neonGreen,
          'https://via.placeholder.com/150?text=LCD+Display'),
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('Marketplace')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(isWide ? 48 : 16),
        child: Center(
          child: Container(
            constraints: const BoxConstraints(maxWidth: 1000),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      colors: [DSColors.primary.withValues(alpha: 0.1), DSColors.secondary.withValues(alpha: 0.05)],
                    ),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: DSColors.primary.withValues(alpha: 0.2)),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Low-Cost Components', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
                            const SizedBox(height: 4),
                            Text('Affordable parts for your projects', style: TextStyle(color: isDark ? DSColors.grey300 : DSColors.grey600)),
                          ],
                        ),
                      ),
                      Icon(Icons.card_giftcard, color: DSColors.warmAmber, size: 40),
                    ],
                  ),
                ),
                const SizedBox(height: 24),
                Wrap(
                  spacing: 16,
                  runSpacing: 16,
                  children: products.map((p) => SizedBox(
                    width: isWide ? 220 : (MediaQuery.of(context).size.width - 48),
                    child: ComponentCard(
                      name: p.name,
                      category: p.category,
                      specification: p.spec,
                      categoryColor: p.color,
                      price: p.price.toDouble(),
                      imageUrl: p.imageUrl,
                    ),
                  )).toList(),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _Product {
  final String name;
  final String category;
  final String spec;
  final int price;
  final Color color;
  final String imageUrl;
  const _Product(this.name, this.category, this.spec, this.price, this.color, this.imageUrl);
}
