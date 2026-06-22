// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use
import 'dart:async';
import 'dart:html' as html;
import 'dart:typed_data';

Future<Uint8List?> capturePhoto({int quality = 50, int maxDimension = 1024}) async {
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

    await Future.delayed(const Duration(milliseconds: 300));

    int w = video.videoWidth;
    int h = video.videoHeight;
    if (w > maxDimension || h > maxDimension) {
      final ratio = maxDimension / (w > h ? w : h);
      w = (w * ratio).round();
      h = (h * ratio).round();
    }

    final canvas = html.CanvasElement()..width = w..height = h;
    canvas.context2D.drawImageScaled(video, 0, 0, w, h);

    stream.getTracks().forEach((t) => t.stop());

    final blob = await canvas.toBlob('image/jpeg', quality / 100);

    final reader = html.FileReader();
    final completer = Completer<Uint8List?>();
    reader.onLoadEnd.listen((_) => completer.complete(reader.result as Uint8List?));
    reader.onError.listen((_) => completer.complete(null));
    reader.readAsArrayBuffer(blob);

    return completer.future;
  } catch (e) {
    return null;
  }
}
