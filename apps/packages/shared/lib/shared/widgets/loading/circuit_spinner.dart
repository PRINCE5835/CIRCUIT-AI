import 'dart:math';
import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class CircuitSpinner extends StatefulWidget {
  final double size;
  final Color? color;
  final double strokeWidth;

  const CircuitSpinner({
    super.key,
    this.size = 48,
    this.color,
    this.strokeWidth = 3,
  });

  @override
  State<CircuitSpinner> createState() => _CircuitSpinnerState();
}

class _CircuitSpinnerState extends State<CircuitSpinner> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: 1500.ms)..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: widget.size,
      height: widget.size,
      child: CustomPaint(
        painter: _CircuitSpinnerPainter(
          animation: _controller,
          color: widget.color ?? DSColors.circuitCyan,
          strokeWidth: widget.strokeWidth,
        ),
      ),
    );
  }
}

class _CircuitSpinnerPainter extends CustomPainter {
  final Animation<double> animation;
  final Color color;
  final double strokeWidth;

  _CircuitSpinnerPainter({required this.animation, required this.color, required this.strokeWidth}) : super(repaint: animation);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = (size.width - strokeWidth) / 2;
    final paint = Paint()
      ..color = color
      ..strokeWidth = strokeWidth
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final sweepAngle = (pi * 1.5) + (pi * 2 * animation.value % (pi * 2));
    final startAngle = -pi / 2 + animation.value * pi * 4;

    canvas.drawArc(Rect.fromCircle(center: center, radius: radius), startAngle, sweepAngle % (pi * 2), false, paint);

    // Dot at end
    final dotAngle = startAngle + sweepAngle % (pi * 2);
    final dotX = center.dx + radius * cos(dotAngle);
    final dotY = center.dy + radius * sin(dotAngle);
    canvas.drawCircle(Offset(dotX, dotY), strokeWidth * 1.2, Paint()..color = color);
  }

  @override
  bool shouldRepaint(_CircuitSpinnerPainter old) => old.animation != animation;
}

class VoicePulse extends StatefulWidget {
  final Color? color;
  final double size;

  const VoicePulse({super.key, this.color, this.size = 120});

  @override
  State<VoicePulse> createState() => _VoicePulseState();
}

class _VoicePulseState extends State<VoicePulse> with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: 1000.ms)..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final col = widget.color ?? DSColors.circuitCyan;

    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        final t = _controller.value;
        final scale1 = 0.8 + t * 0.4;
        final opacity1 = 1.0 - t * 0.5;
        final scale2 = 0.6 + t * 0.6;
        final opacity2 = 0.5 - t * 0.5;

        return SizedBox(
          width: widget.size,
          height: widget.size,
          child: Stack(
            alignment: Alignment.center,
            children: [
              _pulseRing(scale2, opacity2, col),
              _pulseRing(scale1, opacity1, col),
              Container(
                width: widget.size * 0.35,
                height: widget.size * 0.35,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: col.withValues(alpha: 0.15),
                  border: Border.all(color: col, width: 2),
                ),
                child: Icon(Icons.mic, color: col, size: widget.size * 0.18),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _pulseRing(double scale, double opacity, Color color) {
    return Transform.scale(
      scale: scale,
      child: Container(
        width: widget.size,
        height: widget.size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(color: color.withValues(alpha: opacity), width: 2),
        ),
      ),
    );
  }
}

class GlowSpinner extends StatelessWidget {
  final double size;
  final Color? color;

  const GlowSpinner({super.key, this.size = 32, this.color});

  @override
  Widget build(BuildContext context) {
    final col = color ?? DSColors.circuitCyan;

    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        boxShadow: [BoxShadow(color: col.withValues(alpha: 0.5), blurRadius: 12, spreadRadius: 2)],
      ),
      child: CircularProgressIndicator(
        strokeWidth: 2.5,
        valueColor: AlwaysStoppedAnimation<Color>(col),
      ),
    ).animate().shimmer(duration: 1000.ms, color: col.withValues(alpha: 0.2));
  }
}
