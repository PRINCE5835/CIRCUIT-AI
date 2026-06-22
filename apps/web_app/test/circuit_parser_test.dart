import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/services/circuit_parser.dart';

void main() {
  group('CircuitOutputParser', () {
    test('parses markdown with component list', () {
      final result = CircuitOutputParser.parse('''
# LED Blinker Circuit

## Components
- R1: 330Ω resistor
- LED1: 5mm red LED
- Q1: 2N2222 transistor
- C1: 100µF capacitor

## Connections
- Connect R1 to VCC
- Connect LED1 anode to R1
''');
      expect(result.title, 'LED Blinker Circuit');
      expect(result.components.length, 4);
      expect(result.components[0].reference, 'R1');
      expect(result.components[0].name, '330Ω resistor');
      expect(result.components[1].type, 'LED');
      expect(result.components[2].type, 'Transistor');
      expect(result.components[3].value, '');
      expect(result.connections.length, 2);
    });

    test('parses markdown with table format', () {
      final result = CircuitOutputParser.parse('''
# BOM
| Ref | Name | Value | Quantity |
|-----|------|-------|----------|
| R1 | Resistor | 10kΩ | 2 |
| C1 | Capacitor | 100µF | 1 |
| U1 | IC | 555 Timer | 1 |
''');
      expect(result.components.length, 3);
      expect(result.components[0].reference, 'R1');
      expect(result.components[0].name, 'Resistor');
      expect(result.components[1].name, 'Capacitor');
      expect(result.components[2].type, 'IC');
    });

    test('returns empty when no components', () {
      final result = CircuitOutputParser.parse('Just some text');
      expect(result.hasData, false);
      expect(result.components, isEmpty);
      expect(result.connections, isEmpty);
    });

    test('title falls back to default when no header found', () {
      final result = CircuitOutputParser.parse('''
- R1: 10kΩ resistor
- LED: red LED
''');
      expect(result.title, 'Circuit Diagram');
      expect(result.components.length, 2);
    });

    test('detects component types from text', () {
      final result = CircuitOutputParser.parse('''
## Components
- R1: 10kΩ resistor
- C1: 100µF capacitor
- LED1: red LED
- IC1: 555 timer IC
- BAT1: 9V battery
- SW1: toggle switch
''');
      expect(result.components.length, 6);
      expect(result.components[0].type, 'Resistor');
      expect(result.components[1].type, 'Capacitor');
      expect(result.components[2].type, 'LED');
      expect(result.components[3].type, 'IC');
      expect(result.components[4].type, 'Battery');
      expect(result.components[5].type, 'Switch');
    });

    test('parses description section', () {
      final result = CircuitOutputParser.parse('''
# Overview
This is a simple LED blinker circuit
that uses a 555 timer in astable mode.
''');
      expect(result.description, contains('LED blinker'));
      expect(result.description, contains('astable mode'));
    });

    test('handles no-reference component lines', () {
      final result = CircuitOutputParser.parse('''
## Components
- 330Ω resistor
- 5mm red LED
- 100µF capacitor
''');
      expect(result.components.length, 3);
      expect(result.components[0].reference, '');
    });
  });
}
