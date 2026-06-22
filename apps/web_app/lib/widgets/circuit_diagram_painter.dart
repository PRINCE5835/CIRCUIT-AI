import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../services/circuit_parser.dart';

class CircuitDiagramPainter extends CustomPainter {
  final CircuitLayout layout;
  final ColorScheme colors;

  CircuitDiagramPainter({required this.layout, required this.colors});

  @override
  void paint(Canvas canvas, Size size) {
    final bgPaint = Paint()..color = colors.surface;
    canvas.drawRect(Offset.zero & size, bgPaint);

    for (final line in layout.lines) {
      if (line.fromIndex >= layout.nodes.length || line.toIndex >= layout.nodes.length) continue;
      final from = layout.nodes[line.fromIndex];
      final to = layout.nodes[line.toIndex];
      _drawWire(canvas, from, to, colors.primary.withValues(alpha: 0.6));
    }

    for (final node in layout.nodes) {
      _drawComponent(canvas, node, colors);
    }
  }

  void _drawWire(Canvas canvas, ComponentNode from, ComponentNode to, Color color) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;

    final p1 = Offset(from.x + from.w / 2, from.y + from.h / 2);
    final p2 = Offset(to.x + to.w / 2, to.y + to.h / 2);
    canvas.drawLine(p1, p2, paint);

    final dot = Paint()..color = color;
    canvas.drawCircle(p1, 3, dot);
    canvas.drawCircle(p2, 3, dot);
  }

  void _drawComponent(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final type = node.component.type.toLowerCase();
    switch (type) {
      case 'resistor':
        _drawResistor(canvas, node, colors);
        break;
      case 'capacitor':
        _drawCapacitor(canvas, node, colors);
        break;
      case 'led':
        _drawLed(canvas, node, colors);
        break;
      case 'diode':
        _drawDiode(canvas, node, colors);
        break;
      case 'ic':
      case 'microcontroller':
        _drawIc(canvas, node, colors);
        break;
      case 'transistor':
        _drawTransistor(canvas, node, colors);
        break;
      case 'battery':
      case 'power':
        _drawBattery(canvas, node, colors);
        break;
      case 'switch':
        _drawSwitch(canvas, node, colors);
        break;
      default:
        _drawDefault(canvas, node, colors);
    }

    _drawLabel(canvas, node, colors);
  }

  void _drawResistor(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final paint = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.5
      ..style = PaintingStyle.stroke;

    final r = Rect.fromLTWH(node.x + 8, node.y + 8, node.w - 16, node.h - 16);
    final dy = r.height / 2;
    final cx = r.center.dx;
    final cy = r.center.dy;
    const zigzagW = 8.0;
    const zigzagCount = 6;
    final totalZigzagW = zigzagW * zigzagCount;

    canvas.drawLine(Offset(r.left, cy), Offset(cx - totalZigzagW / 2, cy), paint);
    canvas.drawLine(Offset(cx + totalZigzagW / 2, cy), Offset(r.right, cy), paint);

    final zigzag = Paint()
      ..color = Colors.brown
      ..strokeWidth = 2.5
      ..style = PaintingStyle.stroke;

    final path = Path();
    path.moveTo(cx - totalZigzagW / 2, cy);
    for (var i = 0; i < zigzagCount; i++) {
      final x1 = cx - totalZigzagW / 2 + (i + 0.5) * zigzagW;
      final x2 = cx - totalZigzagW / 2 + (i + 1) * zigzagW;
      path.lineTo(x1, cy - dy / 2);
      path.lineTo(x2, cy);
    }
    canvas.drawPath(path, zigzag);

    final fill = Paint()
      ..color = Colors.brown.withValues(alpha: 0.08);
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(6)), fill);
  }

  void _drawCapacitor(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final r = Rect.fromLTWH(node.x + 8, node.y + 8, node.w - 16, node.h - 16);
    final cx = r.center.dx;
    final cy = r.center.dy;
    const plateGap = 6.0;
    final plateH = r.height * 0.5;

    final wire = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(r.left, cy), Offset(cx - plateGap, cy), wire);
    canvas.drawLine(Offset(cx + plateGap, cy), Offset(r.right, cy), wire);

    final plate = Paint()
      ..color = Colors.orange
      ..strokeWidth = 3.0;
    canvas.drawLine(Offset(cx - plateGap, cy - plateH / 2), Offset(cx - plateGap, cy + plateH / 2), plate);
    canvas.drawLine(Offset(cx + plateGap, cy - plateH / 2), Offset(cx + plateGap, cy + plateH / 2), plate);

    final fill = Paint()
      ..color = Colors.orange.withValues(alpha: 0.08);
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(6)), fill);
  }

  void _drawLed(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final r = Rect.fromLTWH(node.x + 8, node.y + 8, node.w - 16, node.h - 16);
    final cx = r.center.dx;
    final cy = r.center.dy;
    final size = math.min(r.width, r.height) * 0.35;

    final wire = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(r.left, cy), Offset(cx - size, cy), wire);
    canvas.drawLine(Offset(cx + size, cy), Offset(r.right, cy), wire);

    final triangle = Path()
      ..moveTo(cx - size, cy - size)
      ..lineTo(cx - size, cy + size)
      ..lineTo(cx + size * 0.7, cy)
      ..close();

    final triPaint = Paint()
      ..color = Colors.red
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;
    canvas.drawPath(triangle, triPaint);

    final arrow = Paint()
      ..color = Colors.red
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(cx + size * 0.3, cy - size * 0.4), Offset(cx + size, cy), arrow);
    canvas.drawLine(Offset(cx + size * 0.3, cy + size * 0.4), Offset(cx + size, cy), arrow);

    final fill = Paint()
      ..color = Colors.red.withValues(alpha: 0.08);
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(6)), fill);

    final glow = Paint()
      ..color = Colors.red.withValues(alpha: 0.15);
    canvas.drawCircle(Offset(cx, cy), size * 1.3, glow);
  }

  void _drawDiode(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final r = Rect.fromLTWH(node.x + 8, node.y + 8, node.w - 16, node.h - 16);
    final cx = r.center.dx;
    final cy = r.center.dy;
    final size = math.min(r.width, r.height) * 0.3;

    final wire = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(r.left, cy), Offset(cx - size, cy), wire);
    canvas.drawLine(Offset(cx + size, cy), Offset(r.right, cy), wire);

    final triangle = Path()
      ..moveTo(cx - size, cy - size)
      ..lineTo(cx - size, cy + size)
      ..lineTo(cx + size * 0.6, cy)
      ..close();

    final triPaint = Paint()
      ..color = Colors.blueGrey
      ..style = PaintingStyle.fill;
    canvas.drawPath(triangle, triPaint);

    final bar = Paint()
      ..color = Colors.blueGrey
      ..strokeWidth = 3.0;
    canvas.drawLine(Offset(cx + size, cy - size), Offset(cx + size, cy + size), bar);
  }

  void _drawIc(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final r = Rect.fromLTWH(node.x + 4, node.y + 4, node.w - 8, node.h - 8);
    final rectPaint = Paint()
      ..color = colors.onSurface.withValues(alpha: 0.1);
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(8)), rectPaint);

    final border = Paint()
      ..color = colors.primary.withValues(alpha: 0.5)
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(8)), border);

    final notchPaint = Paint()
      ..color = colors.primary.withValues(alpha: 0.3);
    canvas.drawCircle(Offset(r.center.dx, r.top + 8), 4, notchPaint);

    final pinPaint = Paint()
      ..color = colors.onSurface.withValues(alpha: 0.5)
      ..strokeWidth = 1.0;
    for (var i = 0; i < 4; i++) {
      final y = r.top + 12 + i * (r.height - 24) / 3;
      canvas.drawLine(Offset(r.left - 4, y), Offset(r.left, y), pinPaint);
      canvas.drawLine(Offset(r.right, y), Offset(r.right + 4, y), pinPaint);
    }
  }

  void _drawTransistor(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final r = Rect.fromLTWH(node.x + 8, node.y + 8, node.w - 16, node.h - 16);
    final cx = r.center.dx;
    final cy = r.center.dy;
    final size = math.min(r.width, r.height) * 0.25;

    final wire = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(r.left, cy), Offset(cx - size, cy), wire);
    canvas.drawLine(Offset(cx + size, cy), Offset(r.right, cy), wire);
    canvas.drawLine(Offset(cx, cy - size * 1.5), Offset(cx, r.top), wire);
    canvas.drawLine(Offset(cx, cy + size * 1.5), Offset(cx, r.bottom), wire);

    final circle = Paint()
      ..color = colors.primary.withValues(alpha: 0.15);
    canvas.drawCircle(Offset(cx, cy), size * 1.5, circle);

    final circleBorder = Paint()
      ..color = colors.primary
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;
    canvas.drawCircle(Offset(cx, cy), size * 1.5, circleBorder);
  }

  void _drawBattery(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final cx = node.x + node.w / 2;
    final cy = node.y + node.h / 2;

    final wire = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(node.x + 8, cy), Offset(cx - 20, cy), wire);
    canvas.drawLine(Offset(cx + 20, cy), Offset(node.x + node.w - 8, cy), wire);

    final body = Paint()
      ..color = Colors.green.withValues(alpha: 0.15);
    canvas.drawRRect(RRect.fromRectAndRadius(
      Rect.fromLTWH(cx - 20, cy - 16, 40, 32), const Radius.circular(4)), body);

    final bodyBorder = Paint()
      ..color = Colors.green
      ..strokeWidth = 2.0
      ..style = PaintingStyle.stroke;
    canvas.drawRRect(RRect.fromRectAndRadius(
      Rect.fromLTWH(cx - 20, cy - 16, 40, 32), const Radius.circular(4)), bodyBorder);

    final plus = Paint()
      ..color = Colors.red
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(cx + 6, cy - 4), Offset(cx + 6, cy + 4), plus);
    canvas.drawLine(Offset(cx + 3, cy), Offset(cx + 9, cy), plus);

    final minus = Paint()
      ..color = Colors.black54
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(cx - 9, cy), Offset(cx - 3, cy), minus);
  }

  void _drawSwitch(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final cy = node.y + node.h / 2;

    final wire = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.0;
    canvas.drawLine(Offset(node.x + 8, cy), Offset(node.x + node.w / 2 - 10, cy), wire);
    canvas.drawLine(Offset(node.x + node.w / 2 + 10, cy), Offset(node.x + node.w - 8, cy), wire);

    final dot1 = Offset(node.x + node.w / 2 - 10, cy);
    final dot2 = Offset(node.x + node.w / 2 + 10, cy);

    final dotPaint = Paint()..color = colors.primary;
    canvas.drawCircle(dot1, 3, dotPaint);
    canvas.drawCircle(dot2, 3, dotPaint);

    final lever = Paint()
      ..color = colors.primary
      ..strokeWidth = 2.5;
    canvas.drawLine(dot1, Offset(node.x + node.w / 2 + 12, cy - 12), lever);
  }

  void _drawDefault(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final r = Rect.fromLTWH(node.x + 4, node.y + 4, node.w - 8, node.h - 8);
    final fill = Paint()
      ..color = colors.primary.withValues(alpha: 0.1);
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(8)), fill);

    final border = Paint()
      ..color = colors.primary.withValues(alpha: 0.4)
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;
    canvas.drawRRect(RRect.fromRectAndRadius(r, const Radius.circular(8)), border);
  }

  void _drawLabel(Canvas canvas, ComponentNode node, ColorScheme colors) {
    final cx = node.x + node.w / 2;
    final labelY = node.y + node.h + 14;

    final ref = node.component.reference;
    final name = node.component.type.isNotEmpty ? node.component.type : node.component.name;

    final refPainter = TextPainter(
      text: TextSpan(
        text: ref.isNotEmpty ? ref : (node.component.name.length > 12 ? '${node.component.name.substring(0, 12)}...' : node.component.name),
        style: TextStyle(
          color: colors.onSurface,
          fontSize: 11,
          fontWeight: FontWeight.w600,
        ),
      ),
      textDirection: TextDirection.ltr,
    )..layout(maxWidth: node.w);

    if (ref.isNotEmpty) {
      refPainter.paint(canvas, Offset(cx - refPainter.width / 2, labelY));
    }

    if (name.isNotEmpty) {
      final namePainter = TextPainter(
        text: TextSpan(
          text: name.length > 14 ? '${name.substring(0, 14)}...' : name,
          style: TextStyle(
            color: colors.onSurface.withValues(alpha: 0.6),
            fontSize: 9,
          ),
        ),
        textDirection: TextDirection.ltr,
      )..layout(maxWidth: node.w);

      final nameY = ref.isNotEmpty ? labelY + 14 : labelY;
      namePainter.paint(canvas, Offset(cx - namePainter.width / 2, nameY));
    }
  }

  @override
  bool shouldRepaint(covariant CircuitDiagramPainter oldDelegate) => true;
}
