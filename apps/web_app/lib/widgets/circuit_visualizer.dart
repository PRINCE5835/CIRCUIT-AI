import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../services/circuit_parser.dart';
import 'circuit_diagram_painter.dart';

class CircuitVisualizer extends StatefulWidget {
  final String markdown;
  final bool compact;

  const CircuitVisualizer({
    super.key,
    required this.markdown,
    this.compact = false,
  });

  @override
  State<CircuitVisualizer> createState() => _CircuitVisualizerState();
}

class _CircuitVisualizerState extends State<CircuitVisualizer> {
  late ParsedCircuit _circuit;
  CircuitLayout? _layout;
  bool _expanded = true;
  int _selectedTab = 0;

  @override
  void initState() {
    super.initState();
    _circuit = CircuitOutputParser.parse(widget.markdown);
    if (_circuit.hasData) {
      _layout = CircuitAutoLayout.layout(_circuit);
    }
  }

  @override
  void didUpdateWidget(CircuitVisualizer oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.markdown != widget.markdown) {
      _circuit = CircuitOutputParser.parse(widget.markdown);
      _layout = _circuit.hasData ? CircuitAutoLayout.layout(_circuit) : null;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_circuit.hasData) return const SizedBox.shrink();

    final ts = Theme.of(context).textTheme;
    final colors = Theme.of(context).colorScheme;

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            _buildHeader(colors, ts),
            if (_expanded) ...[
              _buildTabs(colors, ts),
              if (_selectedTab == 0) _buildDiagram(colors),
              if (_selectedTab == 1) _buildPartsList(colors, ts),
              if (_selectedTab == 2) _buildConnectionsList(colors, ts),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(ColorScheme colors, TextTheme ts) {
    return InkWell(
      onTap: () => setState(() => _expanded = !_expanded),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          children: [
            Icon(Icons.auto_awesome, color: colors.primary, size: 20),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                _circuit.title,
                style: ts.titleSmall?.copyWith(fontWeight: FontWeight.w600),
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(
                color: colors.primary.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                '${_circuit.components.length} parts',
                style: ts.labelSmall?.copyWith(color: colors.primary),
              ),
            ),
            const SizedBox(width: 8),
            AnimatedRotation(
              turns: _expanded ? 0.5 : 0,
              duration: const Duration(milliseconds: 200),
              child: Icon(Icons.expand_more, size: 20, color: colors.onSurface.withValues(alpha: 0.5)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTabs(ColorScheme colors, TextTheme ts) {
    final tabs = ['Diagram', 'Parts List', 'Wiring'];
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12),
      child: Row(
        children: List.generate(tabs.length, (i) {
          final selected = _selectedTab == i;
          return Padding(
            padding: const EdgeInsets.only(right: 4),
            child: ChoiceChip(
              label: Text(tabs[i], style: ts.labelSmall),
              selected: selected,
              onSelected: (v) => setState(() => _selectedTab = i),
              visualDensity: VisualDensity.compact,
              materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
            ),
          );
        }),
      ),
    );
  }

  Widget _buildDiagram(ColorScheme colors) {
    if (_layout == null || _layout!.nodes.isEmpty) {
      return const Padding(
        padding: EdgeInsets.all(24),
        child: Center(child: Text('No components to display')),
      );
    }

    final canvasW = _layout!.nodes.fold(0.0, (max, n) => math.max(max, n.x + n.w)) + 60;
    final canvasH = _layout!.nodes.fold(0.0, (max, n) => math.max(max, n.y + n.h)) + 60;

    return InteractiveViewer(
      minScale: 0.5,
      maxScale: 4.0,
      child: SizedBox(
        width: canvasW,
        height: canvasH,
        child: CustomPaint(
          size: Size(canvasW, canvasH),
          painter: CircuitDiagramPainter(layout: _layout!, colors: colors),
        ),
      ),
    );
  }

  Widget _buildPartsList(ColorScheme colors, TextTheme ts) {
    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(left: 4, bottom: 8),
            child: Text('Components', style: ts.labelMedium?.copyWith(fontWeight: FontWeight.w600)),
          ),
          ...List.generate(_circuit.components.length, (i) {
            final comp = _circuit.components[i];
            return Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Row(
                children: [
                  _componentIcon(comp.type),
                  const SizedBox(width: 8),
                  if (comp.reference.isNotEmpty)
                    Text('${comp.reference}: ', style: ts.bodySmall?.copyWith(fontWeight: FontWeight.w600)),
                  Expanded(child: Text(comp.name, style: ts.bodySmall)),
                  if (comp.value.isNotEmpty)
                    Text(comp.value, style: ts.bodySmall?.copyWith(color: colors.primary)),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _buildConnectionsList(ColorScheme colors, TextTheme ts) {
    if (_circuit.connections.isEmpty) {
      return Padding(
        padding: const EdgeInsets.all(16),
        child: Text('No wiring instructions found.', style: ts.bodySmall),
      );
    }

    return Padding(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.only(left: 4, bottom: 8),
            child: Text('Wiring Instructions', style: ts.labelMedium?.copyWith(fontWeight: FontWeight.w600)),
          ),
          ...List.generate(_circuit.connections.length, (i) {
            return Padding(
              padding: const EdgeInsets.only(bottom: 6),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('${i + 1}. ', style: ts.bodySmall?.copyWith(color: colors.primary, fontWeight: FontWeight.w600)),
                  Expanded(child: Text(_circuit.connections[i], style: ts.bodySmall)),
                ],
              ),
            );
          }),
        ],
      ),
    );
  }

  Widget _componentIcon(String type) {
    IconData icon;
    Color color;
    switch (type.toLowerCase()) {
      case 'resistor':
        icon = Icons.timeline;
        color = Colors.brown;
        break;
      case 'capacitor':
        icon = Icons.linear_scale;
        color = Colors.orange;
        break;
      case 'led':
        icon = Icons.circle;
        color = Colors.red;
        break;
      case 'diode':
        icon = Icons.arrow_forward;
        color = Colors.blueGrey;
        break;
      case 'ic':
      case 'microcontroller':
        icon = Icons.memory;
        color = Colors.indigo;
        break;
      case 'transistor':
        icon = Icons.graphic_eq;
        color = Colors.teal;
        break;
      case 'battery':
      case 'power':
        icon = Icons.battery_std;
        color = Colors.green;
        break;
      case 'switch':
        icon = Icons.toggle_on;
        color = Colors.amber;
        break;
      default:
        icon = Icons.devices_other;
        color = Colors.blueGrey;
    }
    return Icon(icon, size: 16, color: color);
  }
}
