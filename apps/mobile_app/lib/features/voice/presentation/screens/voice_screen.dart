import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import '../../../../core/services/api_service.dart';
import '../services/voice_service.dart';

class VoiceScreen extends ConsumerStatefulWidget {
  const VoiceScreen({super.key});

  @override
  ConsumerState<VoiceScreen> createState() => _VoiceScreenState();
}

class _VoiceScreenState extends ConsumerState<VoiceScreen> {
  bool _isListening = false;
  bool _isLoading = false;
  final _messages = <_Message>[];
  final _textController = TextEditingController();
  final _voiceService = VoiceService();

  @override
  void dispose() {
    _textController.dispose();
    _voiceService.dispose();
    super.dispose();
  }

  Future<void> _toggleListening() async {
    if (_isListening) {
      setState(() => _isListening = false);
      final text = await _voiceService.stopAndTranscribe();
      if (text != null && text.isNotEmpty) {
        _addUserMessage(text);
        await _sendMessage(text);
      }
    } else {
      final error = await _voiceService.startRecording();
      if (error != null) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Mic error: $error')),
          );
        }
        return;
      }
      setState(() => _isListening = true);
    }
  }

  void _addUserMessage(String text) {
    setState(() => _messages.add(_Message(text, true)));
  }

  Future<void> _onTextSubmitted() async {
    final text = _textController.text.trim();
    if (text.isEmpty) return;
    _textController.clear();
    _addUserMessage(text);
    await _sendMessage(text);
  }

  Future<void> _sendMessage([String? text]) async {
    final messageText = text ?? _textController.text.trim();
    if (messageText.isEmpty || _isLoading) return;

    if (text == null) {
      _addUserMessage(messageText);
      _textController.clear();
    }

    setState(() => _isLoading = true);

    try {
      final chatMessages = _messages
          .where((m) => m.text != 'Thinking...')
          .map((m) => {'role': m.isUser ? 'user' : 'assistant', 'content': m.text})
          .toList();

      final result = await ApiService.aiChat(chatMessages);
      final response = result['response'] as String? ??
          (result['message']?['content'] as String?) ??
          'No response';

      if (mounted) {
        setState(() {
          _messages.add(_Message(response, false));
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add(_Message('Error: ${e.toString().replaceFirst('Exception: ', '')}', false));
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: Text(AppLocalizations.of(context).voice)),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        VoicePulse(color: _isListening ? DSColors.circuitCyan : DSColors.grey400),
                        const SizedBox(height: DSDimensions.s24),
                        Text(
                          _isListening ? 'Speak now...' : 'Tap the mic or type a command',
                          style: theme.textTheme.titleMedium?.copyWith(
                            color: theme.colorScheme.onSurface.withValues(alpha: 0.5),
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(DSDimensions.s16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      final msg = _messages[index];
                      return Align(
                        alignment: msg.isUser ? Alignment.centerRight : Alignment.centerLeft,
                        child: Container(
                          margin: const EdgeInsets.only(bottom: DSDimensions.s8),
                          padding: const EdgeInsets.symmetric(
                            horizontal: DSDimensions.s16,
                            vertical: DSDimensions.s12,
                          ),
                          decoration: BoxDecoration(
                            color: msg.isUser
                                ? DSColors.primary.withValues(alpha: 0.15)
                                : theme.colorScheme.surfaceContainerHighest,
                            borderRadius: BorderRadius.circular(DSDimensions.r16),
                          ),
                          child: Text(msg.text),
                        ),
                      );
                    },
                  ),
          ),
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.only(bottom: 8),
              child: CircuitSpinner(size: 24),
            ),
          Container(
            padding: const EdgeInsets.all(DSDimensions.s16),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              border: Border(
                top: BorderSide(color: theme.dividerTheme.color ?? Colors.grey.shade200),
              ),
            ),
            child: SafeArea(
              child: Row(
                children: [
                  IconButton(
                    icon: Icon(
                      _isListening ? Icons.mic : Icons.mic_none,
                      color: _isListening ? DSColors.danger : null,
                    ),
                    onPressed: _toggleListening,
                  ),
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      decoration: const InputDecoration(
                        hintText: 'Ask anything about circuits...',
                        border: InputBorder.none,
                        isDense: true,
                      ),
                      onSubmitted: (_) => _onTextSubmitted(),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.send_rounded),
                    color: DSColors.primary,
                    onPressed: _onTextSubmitted,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _Message {
  final String text;
  final bool isUser;
  const _Message(this.text, this.isUser);
}
