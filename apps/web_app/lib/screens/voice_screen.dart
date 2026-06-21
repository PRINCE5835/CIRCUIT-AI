import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/shared/design_system/colors.dart';
import 'package:breadboard_shared/shared/design_system/gradients.dart';

class VoiceScreen extends ConsumerStatefulWidget {
  const VoiceScreen({super.key});

  @override
  ConsumerState<VoiceScreen> createState() => _VoiceScreenState();
}

class _VoiceScreenState extends ConsumerState<VoiceScreen> {
  final _controller = TextEditingController();
  final _messages = <_ChatMessage>[];
  bool _isLoading = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;
    setState(() {
      _messages.add(_ChatMessage(text, true));
      _isLoading = true;
    });
    _controller.clear();

    await Future.delayed(const Duration(milliseconds: 1500));

    if (mounted) {
      setState(() {
        _messages.add(_ChatMessage(
          'I can help you build that! Here\'s a simple circuit:\n\n'
          '- 1x LED (any color)\n'
          '- 1x 220Ω resistor\n'
          '- 1x Battery (3V)\n\n'
          'Connect: Battery + → Resistor → LED (long leg) → LED (short leg) → Battery -',
          false,
        ));
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;
    return Scaffold(
      appBar: AppBar(title: const Text('Voice AI Assistant')),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Container(
                          padding: const EdgeInsets.all(24),
                          decoration: BoxDecoration(
                            gradient: DSGradients.primaryGradient,
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.mic, size: 48, color: Colors.white),
                        ),
                        const SizedBox(height: 24),
                        Text('Ask me anything about electronics', style: Theme.of(context).textTheme.titleMedium),
                        const SizedBox(height: 8),
                        Text('e.g. "Make an LED blink with Arduino"', style: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500)),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length + (_isLoading ? 1 : 0),
                    itemBuilder: (_, i) {
                      if (_isLoading && i == _messages.length) {
                        return const Padding(
                          padding: EdgeInsets.symmetric(vertical: 8),
                          child: Row(
                            children: [
                              SizedBox(width: 48),
                              CircularProgressIndicator(strokeWidth: 2),
                              SizedBox(width: 12),
                              Text('Thinking...'),
                            ],
                          ),
                        );
                      }
                      final msg = _messages[i];
                      return Align(
                        alignment: msg.isUser ? Alignment.centerRight : Alignment.centerLeft,
                        child: Container(
                          margin: const EdgeInsets.only(bottom: 12),
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                          decoration: BoxDecoration(
                            gradient: msg.isUser
                                ? DSGradients.primaryGradient
                                : (isDark ? LinearGradient(colors: [DSColors.surfaceDarkCard, DSColors.surfaceDarkVariant]) : null),
                            color: msg.isUser ? null : (isDark ? null : DSColors.grey50),
                            borderRadius: BorderRadius.only(
                              topLeft: const Radius.circular(16),
                              topRight: const Radius.circular(16),
                              bottomLeft: Radius.circular(msg.isUser ? 16 : 4),
                              bottomRight: Radius.circular(msg.isUser ? 4 : 16),
                            ),
                          ),
                          constraints: BoxConstraints(maxWidth: isWide ? 600 : MediaQuery.of(context).size.width * 0.8),
                          child: Text(msg.text, style: TextStyle(color: msg.isUser ? Colors.white : (isDark ? DSColors.grey100 : DSColors.grey900))),
                        ),
                      );
                    },
                  ),
          ),
          Container(
            padding: EdgeInsets.fromLTRB(isWide ? 48 : 16, 8, isWide ? 48 : 16, 16),
            decoration: BoxDecoration(
              color: isDark ? DSColors.surfaceDarkElevated : DSColors.white,
              border: Border(top: BorderSide(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06))),
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900),
                    decoration: InputDecoration(
                      hintText: 'Type your message...',
                      hintStyle: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    ),
                    onSubmitted: _sendMessage,
                  ),
                ),
                const SizedBox(width: 8),
                Container(
                  decoration: BoxDecoration(gradient: DSGradients.primaryGradient, shape: BoxShape.circle),
                  child: IconButton(
                    icon: const Icon(Icons.send, color: Colors.white),
                    onPressed: () => _sendMessage(_controller.text),
                  ),
                ),
                const SizedBox(width: 4),
                Container(
                  decoration: BoxDecoration(gradient: DSGradients.secondaryGradient, shape: BoxShape.circle),
                  child: IconButton(
                    icon: const Icon(Icons.mic, color: Colors.white),
                    onPressed: () {},
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _ChatMessage {
  final String text;
  final bool isUser;
  const _ChatMessage(this.text, this.isUser);
}
