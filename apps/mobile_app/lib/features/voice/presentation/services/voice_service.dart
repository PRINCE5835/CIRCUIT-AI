import 'dart:convert';
import 'dart:io';
import 'package:record/record.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class VoiceService {
  final AudioRecorder _recorder = AudioRecorder();
  bool _isRecording = false;
  String? _recordingPath;

  bool get isRecording => _isRecording;

  Future<String?> startRecording() async {
    try {
      _recordingPath = '${Directory.systemTemp.path}/breadboard_voice_${DateTime.now().millisecondsSinceEpoch}.wav';
      await _recorder.start(
        const RecordConfig(
          encoder: AudioEncoder.wav,
          sampleRate: 16000,
          numChannels: 1,
        ),
        path: _recordingPath!,
      );
      _isRecording = true;
      return null;
    } catch (e) {
      _isRecording = false;
      return e.toString();
    }
  }

  Future<String?> stopAndTranscribe() async {
    if (!_isRecording) return null;
    try {
      _isRecording = false;
      final path = await _recorder.stop();
      if (path == null) return null;

      final file = File(path);
      if (!await file.exists()) return null;

      final bytes = await file.readAsBytes();
      final base64Audio = base64Encode(bytes);

      try {
        final response = await ApiClient.instance.dio.post(
          ApiEndpoints.aiSpeechStt,
          data: {'audio': base64Audio, 'language': 'en'},
        );
        final data = response.data;
        await file.delete();
        return data['text'] as String? ?? '';
      } catch (e) {
        await file.delete();
        return '';
      }
    } catch (e) {
      _isRecording = false;
      return null;
    }
  }

  void dispose() {
    _recorder.dispose();
  }
}
