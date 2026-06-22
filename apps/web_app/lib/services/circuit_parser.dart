class ParsedCircuit {
  final String title;
  final List<ParsedComponent> components;
  final List<String> connections;
  final String description;

  ParsedCircuit({
    this.title = '',
    this.components = const [],
    this.connections = const [],
    this.description = '',
  });

  bool get hasData => components.isNotEmpty || connections.isNotEmpty;
}

class ParsedComponent {
  final String reference;
  final String name;
  final String type;
  final String value;

  ParsedComponent({
    this.reference = '',
    this.name = '',
    this.type = '',
    this.value = '',
  });
}

class ComponentNode {
  final ParsedComponent component;
  double x;
  double y;
  final double w;
  final double h;

  ComponentNode({
    required this.component,
    this.x = 0,
    this.y = 0,
    this.w = 120,
    this.h = 60,
  });
}

class ConnectionLine {
  final int fromIndex;
  final int toIndex;
  final String label;

  ConnectionLine({required this.fromIndex, required this.toIndex, this.label = ''});
}

class CircuitLayout {
  final List<ComponentNode> nodes;
  final List<ConnectionLine> lines;

  CircuitLayout({required this.nodes, required this.lines});
}

class CircuitAutoLayout {
  static CircuitLayout layout(ParsedCircuit circuit) {
    if (circuit.components.isEmpty) {
      return CircuitLayout(nodes: [], lines: []);
    }

    final cols = circuit.components.length <= 4 ? circuit.components.length : 4;
    const spacingX = 160.0;
    const spacingY = 110.0;
    const startX = 40.0;
    const startY = 40.0;

    final nodes = <ComponentNode>[];
    for (var i = 0; i < circuit.components.length; i++) {
      final col = i % cols;
      final row = i ~/ cols;
      nodes.add(ComponentNode(
        component: circuit.components[i],
        x: startX + col * spacingX,
        y: startY + row * spacingY,
      ));
    }

    final lines = <ConnectionLine>[];
    if (nodes.length >= 2) {
      for (var i = 0; i < nodes.length - 1; i++) {
        lines.add(ConnectionLine(fromIndex: i, toIndex: i + 1));
      }
    }

    return CircuitLayout(nodes: nodes, lines: lines);
  }
}

class CircuitOutputParser {
  static ParsedCircuit parse(String markdown) {
    final lines = markdown.split('\n');
    final components = <ParsedComponent>[];
    final connections = <String>[];
    String title = '';
    String description = '';

    var section = '';
    for (final line in lines) {
      final trimmed = line.trim();

      if (trimmed.startsWith('# ') || trimmed.startsWith('## ')) {
        final header = trimmed.replaceAll(RegExp(r'^#+\s*'), '');
        final lower = header.toLowerCase();
        if (lower.contains('component') || lower.contains('part') || lower.contains('bill') || lower.contains('bom')) {
          section = 'components';
        } else if (lower.contains('connection') || lower.contains('wiring') || lower.contains('step') || lower.contains('instruction')) {
          section = 'connections';
        } else if (lower.contains('description') || lower.contains('overview') || lower.contains('explanation')) {
          section = 'description';
        } else {
          section = '';
          if (title.isEmpty) title = header;
        }
        continue;
      }

      if (trimmed.startsWith('- ') || trimmed.startsWith('* ') || trimmed.startsWith('1.') || trimmed.startsWith('2.')) {
        final text = trimmed.replaceFirst(RegExp(r'^[-*\d.]+ '), '');
        switch (section) {
          case 'components':
            final comp = _parseComponentLine(text);
            if (comp != null) components.add(comp);
            break;
          case 'connections':
            connections.add(text);
            break;
          default:
            if (text.contains(RegExp(r'Ω|kΩ|MΩ|µF|nF|pF|mH|V\b|mA|IC\s|LED|resistor|capacitor|transistor', caseSensitive: false))) {
              final comp = _parseComponentLine(text);
              if (comp != null) components.add(comp);
            }
        }
        continue;
      }

      if (trimmed.contains('|') && trimmed.startsWith('|')) {
        if (section == 'components') {
          final parts = trimmed.split('|').map((s) => s.trim()).where((s) => s.isNotEmpty).toList();
          final headerKeywords = ['ref', 'name', 'value', 'quantity', 'type', 'description', 'part', 'qty'];
          if (parts.length >= 2 && !parts[0].contains('-') && !headerKeywords.contains(parts[0].toLowerCase())) {
            components.add(ParsedComponent(
              reference: parts.length > 2 ? parts[0] : '',
              name: parts.length > 2 ? parts[1] : parts[0],
              value: parts.length > 3 ? parts[2] : (parts.length > 1 ? parts[parts.length - 1] : ''),
              type: parts.length > 3 ? parts[1] : '',
            ));
          }
        }
        continue;
      }

      if (section == 'description') {
        description += '$trimmed ';
      }
    }

    if (title.isEmpty) title = 'Circuit Diagram';

    return ParsedCircuit(
      title: title,
      components: components,
      connections: connections,
      description: description.trim(),
    );
  }

  static ParsedComponent? _parseComponentLine(String text) {
    final refMatch = RegExp(r'^([A-Za-z]+[0-9]+)\s*[:=]?\s*(.*)').firstMatch(text);
    String ref = '';
    String rest = text;
    if (refMatch != null) {
      ref = refMatch.group(1) ?? '';
      rest = refMatch.group(2) ?? text;
    }

    final typeMap = {
      'resistor': 'Resistor',
      'capacitor': 'Capacitor',
      'transistor': 'Transistor',
      'diode': 'Diode',
      'led': 'LED',
      'ic': 'IC',
      'timer': 'IC',
      'potentiometer': 'Potentiometer',
      'switch': 'Switch',
      'relay': 'Relay',
      'inductor': 'Inductor',
      'transformer': 'Transformer',
      'motor': 'Motor',
      'sensor': 'Sensor',
      'display': 'Display',
      'battery': 'Battery',
      'power': 'Power',
      'arduino': 'Microcontroller',
      'raspberry': 'Microcontroller',
      'op-amp': 'Op-Amp',
      'opamp': 'Op-Amp',
    };

    final lower = rest.toLowerCase();
    String detectedType = '';
    for (final entry in typeMap.entries) {
      if (lower.contains(entry.key)) {
        detectedType = entry.value;
        break;
      }
    }

    return ParsedComponent(
      reference: ref,
      name: rest,
      type: detectedType,
      value: '',
    );
  }
}
