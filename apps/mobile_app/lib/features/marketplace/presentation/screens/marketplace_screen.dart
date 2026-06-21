import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class MarketplaceScreen extends ConsumerStatefulWidget {
  const MarketplaceScreen({super.key});

  @override
  ConsumerState<MarketplaceScreen> createState() => _MarketplaceScreenState();
}

class _MarketplaceScreenState extends ConsumerState<MarketplaceScreen> {
  final _searchController = TextEditingController();

  static const _components = [
    _Component('Arduino Uno R3', 'Development Board', 'ATmega328P', 650, 'https://via.placeholder.com/150?text=Arduino+Uno'),
    _Component('Breadboard 830pt', 'Prototyping Board', '830 tie points', 120, 'https://via.placeholder.com/150?text=Breadboard'),
    _Component('LED Assorted Kit', 'LEDs', '100pcs 5mm LEDs', 85, 'https://via.placeholder.com/150?text=LED+Kit'),
    _Component('Resistor Kit', 'Resistors', '500pcs 1/4W', 99, 'https://via.placeholder.com/150?text=Resistor+Kit'),
    _Component('Jumper Wires', 'Wires', '120pcs M-M/M-F/F-M', 149, 'https://via.placeholder.com/150?text=Jumper+Wires'),
    _Component('555 Timer IC', 'IC', 'NE555P DIP-8', 25, 'https://via.placeholder.com/150?text=555+Timer'),
    _Component('LM393 Sensor', 'Sensor', 'Speed Sensor Module', 45, 'https://via.placeholder.com/150?text=LM393+Sensor'),
    _Component('Battery Holder', 'Power', '4xAA with switch', 35, 'https://via.placeholder.com/150?text=Battery+Holder'),
    _Component('Capacitor Kit', 'Capacitors', '50pcs ceramic + electrolytic', 75, 'https://via.placeholder.com/150?text=Capacitor+Kit'),
    _Component('Potentiometer', 'Variable Resistor', '10kΩ + 100kΩ pack', 40, 'https://via.placeholder.com/150?text=Potentiometer'),
    _Component('NPN Transistor', 'Transistors', 'BC547 pack of 10', 30, 'https://via.placeholder.com/150?text=NPN+Transistor'),
    _Component('LCD Display', 'Display', '16x2 I2C module', 180, 'https://via.placeholder.com/150?text=LCD+Display'),
  ];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Marketplace')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(DSDimensions.s16),
            child: AppSearchBar(
              controller: _searchController,
              hint: 'Search components...',
            ),
          ),
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.symmetric(horizontal: DSDimensions.s16),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 0.8,
                crossAxisSpacing: DSDimensions.s12,
                mainAxisSpacing: DSDimensions.s12,
              ),
              itemCount: _components.length,
              itemBuilder: (context, index) {
                final c = _components[index];
                return ComponentCard(
                  name: c.name,
                  category: c.category,
                  specification: c.spec,
                  price: c.price.toDouble(),
                  imageUrl: c.imageUrl,
                  onTap: () {},
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _Component {
  final String name;
  final String category;
  final String spec;
  final int price;
  final String imageUrl;
  const _Component(this.name, this.category, this.spec, this.price, this.imageUrl);
}
