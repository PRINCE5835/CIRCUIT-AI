import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/services/circuit_parser.dart';

void main() {
  group('ParsedCircuit', () {
    test('hasData returns false when empty', () {
      final circuit = ParsedCircuit();
      expect(circuit.hasData, false);
    });

    test('hasData returns true with components', () {
      final circuit = ParsedCircuit(components: [
        ParsedComponent(reference: 'R1', name: 'Resistor'),
      ]);
      expect(circuit.hasData, true);
    });

    test('hasData returns true with connections', () {
      final circuit = ParsedCircuit(connections: ['Connect R1 to VCC']);
      expect(circuit.hasData, true);
    });

    test('default values', () {
      final circuit = ParsedCircuit();
      expect(circuit.title, '');
      expect(circuit.components, []);
      expect(circuit.connections, []);
      expect(circuit.description, '');
    });
  });

  group('ParsedComponent', () {
    test('default values', () {
      final comp = ParsedComponent();
      expect(comp.reference, '');
      expect(comp.name, '');
      expect(comp.type, '');
      expect(comp.value, '');
    });
  });

  group('ComponentNode', () {
    test('default dimensions', () {
      final node = ComponentNode(
        component: ParsedComponent(reference: 'R1', name: 'Resistor'),
      );
      expect(node.x, 0);
      expect(node.y, 0);
      expect(node.w, 120);
      expect(node.h, 60);
    });
  });

  group('ConnectionLine', () {
    test('default label', () {
      final line = ConnectionLine(fromIndex: 0, toIndex: 1);
      expect(line.fromIndex, 0);
      expect(line.toIndex, 1);
      expect(line.label, '');
    });
  });
}
