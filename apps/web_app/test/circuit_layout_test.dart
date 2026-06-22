import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/services/circuit_parser.dart';

void main() {
  group('CircuitAutoLayout', () {
    test('returns empty layout for empty circuit', () {
      final circuit = ParsedCircuit();
      final layout = CircuitAutoLayout.layout(circuit);
      expect(layout.nodes, isEmpty);
      expect(layout.lines, isEmpty);
    });

    test('positions single component', () {
      final circuit = ParsedCircuit(components: [
        ParsedComponent(reference: 'R1', name: '10kΩ resistor', type: 'Resistor'),
      ]);
      final layout = CircuitAutoLayout.layout(circuit);
      expect(layout.nodes.length, 1);
      expect(layout.nodes[0].x, 40.0);
      expect(layout.nodes[0].y, 40.0);
    });

    test('positions multiple components in a grid', () {
      final circuit = ParsedCircuit(components: [
        ParsedComponent(reference: 'R1', name: 'R1'),
        ParsedComponent(reference: 'R2', name: 'R2'),
        ParsedComponent(reference: 'R3', name: 'R3'),
      ]);
      final layout = CircuitAutoLayout.layout(circuit);
      expect(layout.nodes.length, 3);
      // Row 0: 0,1,2 at y=40
      expect(layout.nodes[0].y, 40.0);
      expect(layout.nodes[1].y, 40.0);
      expect(layout.nodes[2].y, 40.0);
    });

    test('creates lines between consecutive nodes', () {
      final circuit = ParsedCircuit(components: [
        ParsedComponent(reference: 'R1', name: 'R1'),
        ParsedComponent(reference: 'R2', name: 'R2'),
        ParsedComponent(reference: 'R3', name: 'R3'),
      ]);
      final layout = CircuitAutoLayout.layout(circuit);
      expect(layout.lines.length, 2);
      expect(layout.lines[0].fromIndex, 0);
      expect(layout.lines[0].toIndex, 1);
      expect(layout.lines[1].fromIndex, 1);
      expect(layout.lines[1].toIndex, 2);
    });

    test('wraps to next row after 4 columns', () {
      final circuit = ParsedCircuit(components: [
        ParsedComponent(reference: 'C1', name: 'C1'),
        ParsedComponent(reference: 'C2', name: 'C2'),
        ParsedComponent(reference: 'C3', name: 'C3'),
        ParsedComponent(reference: 'C4', name: 'C4'),
        ParsedComponent(reference: 'C5', name: 'C5'),
      ]);
      final layout = CircuitAutoLayout.layout(circuit);
      expect(layout.nodes.length, 5);
      // Fifth item wraps to next row
      expect(layout.nodes[4].x, 40.0); // col 0 of row 1
      expect(layout.nodes[4].y, 150.0); // startY(40) + 1*110
    });

    test('handles 6 components with correct wrapping', () {
      final circuit = ParsedCircuit(components: List.generate(6, (i) =>
        ParsedComponent(reference: 'C$i', name: 'C$i'),
      ));
      final layout = CircuitAutoLayout.layout(circuit);
      expect(layout.nodes.length, 6);
      // Node 4: col=0 row=1
      expect(layout.nodes[4].x, 40.0);
      expect(layout.nodes[4].y, 150.0);
      // Node 5: col=1 row=1
      expect(layout.nodes[5].x, 200.0);
      expect(layout.nodes[5].y, 150.0);
    });
  });
}
