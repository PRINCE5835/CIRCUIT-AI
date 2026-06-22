// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:async';
import 'dart:convert';
import 'dart:html' as html;
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'package:breadboard_shared/breadboard_shared.dart';
import 'component_info_sheet.dart';

class CameraDialog extends StatefulWidget {
  const CameraDialog({super.key});

  @override
  State<CameraDialog> createState() => _CameraDialogState();
}

class _CameraDialogState extends State<CameraDialog> {
  html.MediaStream? _stream;
  html.VideoElement? _video;
  html.CanvasElement? _canvas;
  Timer? _timer;
  Uint8List? _currentFrame;
  bool _error = false;

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    try {
      final stream = await html.window.navigator.mediaDevices!.getUserMedia({
        'video': {'facingMode': 'environment'},
        'audio': false,
      });
      final video = html.VideoElement()
        ..srcObject = stream
        ..autoplay = true
        ..muted = true;
      await video.onCanPlay.first;
      video.play();

      final canvas = html.CanvasElement();
      setState(() {
        _stream = stream;
        _video = video;
        _canvas = canvas;
      });

      _timer = Timer.periodic(const Duration(milliseconds: 200), (_) => _grabFrame());
    } catch (e) {
      setState(() => _error = true);
    }
  }

  void _grabFrame() {
    final v = _video;
    final c = _canvas;
    if (v == null || c == null) return;
    final w = v.videoWidth;
    final h = v.videoHeight;
    if (w == 0 || h == 0) return;
    c.width = (w >= h) ? 640 : ((w / h) * 640).round();
    c.height = (h >= w) ? 480 : ((h / w) * 480).round();
    c.context2D.drawImageScaled(v, 0, 0, c.width as int, c.height as int);
    final uri = c.toDataUrl('image/jpeg', 0.3);
    final parts = uri.split(',');
    if (parts.length > 1) {
      final bytes = base64Decode(parts[1]);
      if (mounted) setState(() => _currentFrame = bytes);
    }
  }

  Future<void> _capture() async {
    _timer?.cancel();
    if (_video == null || _stream == null || _canvas == null) return;

    try {
      final vw = _video!.videoWidth;
      final vh = _video!.videoHeight;
      final c = html.CanvasElement()..width = vw..height = vh;
      c.context2D.drawImageScaled(_video!, 0, 0, vw, vh);

      _stream!.getTracks().forEach((t) => t.stop());

      final blob = await c.toBlob('image/jpeg', 0.85);
      final reader = html.FileReader();
      final completer = Completer<Uint8List?>();
      reader.onLoadEnd.listen((_) => completer.complete(reader.result as Uint8List?));
      reader.onError.listen((_) => completer.complete(null));
      reader.readAsArrayBuffer(blob);
      final bytes = await completer.future;
      if (bytes == null || !mounted) return;

      Navigator.of(context).pop();
      _showScanning();
      final base64Image = base64Encode(bytes);
      final response = await ApiClient.instance.dio.post(
        ApiEndpoints.aiVisionDetect,
        data: {'image': base64Image},
        options: Options(receiveTimeout: const Duration(seconds: 120), sendTimeout: const Duration(seconds: 60)),
      );
      if (!mounted) return;
      Navigator.of(context).pop();
      final resultData = response.data;
      final status = resultData['status'] as String? ?? 'success';

      if (status == 'no_circuit') {
        final msg = resultData['message'] as String? ?? 'No electronic circuit detected.';
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
        return;
      }
      if (status == 'unclear') {
        final msg = resultData['message'] as String? ?? 'Image is not clear.';
        if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(msg)));
        return;
      }

      final components = resultData['components'] as List<dynamic>?;
      if (components == null || components.isEmpty) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('No components detected. Try a clearer photo.')),
          );
        }
        return;
      }
      if (!mounted) return;
      _showResults(components);
    } catch (e) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Scan failed: $e')),
        );
      }
    }
  }

  void _showScanning() {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (_) => const Center(child: CircuitSpinner(size: 48)),
    );
  }

  void _showResults(List<dynamic> components) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('${components.length} Component${components.length == 1 ? '' : 's'} Detected'),
        content: SizedBox(
          width: double.maxFinite,
          child: ListView(
            shrinkWrap: true,
            children: components.map((c) {
              final cMap = c as Map<String, dynamic>;
              final name = cMap['name'] as String? ?? 'Unknown';
              final type = cMap['type'] as String?;
              final confidence = cMap['confidence'] as num?;
              final quantity = cMap['quantity'];
              final pkg = cMap['package'] as String?;
              final markings = cMap['markings'] as String?;
              final confStr = confidence != null ? '${(confidence * 100).toStringAsFixed(0)}%' : '';
              return Card(
                margin: const EdgeInsets.symmetric(vertical: 4),
                child: Padding(
                  padding: const EdgeInsets.all(10),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.memory, color: DSColors.circuitCyan, size: 18),
                          const SizedBox(width: 6),
                          Expanded(child: Text(name, style: const TextStyle(fontWeight: FontWeight.w600))),
                          if (confStr.isNotEmpty)
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                              decoration: BoxDecoration(
                                color: DSColors.circuitCyan.withValues(alpha: 0.15),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(confStr, style: TextStyle(fontSize: 11, color: DSColors.circuitCyan)),
                            ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Wrap(
                        spacing: 8,
                        runSpacing: 4,
                        children: [
                          if (type != null) _detailChip('Type', type),
                          if (quantity != null) _detailChip('Qty', '$quantity'),
                          if (pkg != null && pkg.isNotEmpty) _detailChip('Package', pkg),
                          if (markings != null && markings.isNotEmpty) _detailChip('Markings', markings),
                        ],
                      ),
                      const SizedBox(height: 6),
                      Align(
                        alignment: Alignment.centerRight,
                        child: TextButton.icon(
                          onPressed: () => _openComponentInfo(ctx, name),
                          icon: const Icon(Icons.open_in_new, size: 14),
                          label: const Text('Learn More', style: TextStyle(fontSize: 12)),
                          style: TextButton.styleFrom(
                            foregroundColor: DSColors.circuitCyan,
                            padding: const EdgeInsets.symmetric(horizontal: 8),
                            minimumSize: Size.zero,
                            tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              );
            }).toList(),
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK')),
        ],
      ),
    );
  }

  void _openComponentInfo(BuildContext ctx, String name) {
    Navigator.of(ctx).pop();
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => ComponentInfoSheet(componentName: name, showDetails: true),
    );
  }

  Widget _detailChip(String label, String value) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(
        color: DSColors.primary.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Text('$label: $value', style: TextStyle(fontSize: 11, color: DSColors.primary)),
    );
  }

  void _cancel() {
    _timer?.cancel();
    _stream?.getTracks().forEach((t) => t.stop());
    Navigator.of(context).pop();
  }

  @override
  void dispose() {
    _timer?.cancel();
    _stream?.getTracks().forEach((t) => t.stop());
    super.dispose();
  }

  Widget _buildControls() {
    return Positioned(
      left: 0,
      right: 0,
      bottom: 0,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 16),
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.transparent, Colors.black54],
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            IconButton(
              icon: const Icon(Icons.close, color: Colors.white, size: 28),
              onPressed: _cancel,
            ),
            GestureDetector(
              onTap: _currentFrame != null ? _capture : null,
              child: Container(
                width: 64,
                height: 64,
                decoration: const BoxDecoration(shape: BoxShape.circle, color: Colors.white),
                child: const Icon(Icons.camera_alt, color: Colors.black, size: 28),
              ),
            ),
            const SizedBox(width: 48),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      insetPadding: EdgeInsets.zero,
      child: SizedBox(
        width: 500,
        height: 600,
        child: Stack(
          children: [
            if (_error)
              const Center(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.videocam_off, size: 48),
                    SizedBox(height: 8),
                    Text('Camera not available'),
                  ],
                ),
              )
            else if (_currentFrame != null)
              SizedBox(
                width: double.infinity,
                height: double.infinity,
                child: Image.memory(_currentFrame!, fit: BoxFit.cover),
              )
            else
              const Center(child: CircularProgressIndicator()),
            if (_currentFrame != null || _error) _buildControls(),
          ],
        ),
      ),
    );
  }
}
