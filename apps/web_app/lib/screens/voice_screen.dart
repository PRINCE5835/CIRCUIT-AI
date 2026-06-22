import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import 'package:breadboard_shared/breadboard_shared.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../widgets/conversation_list.dart';
import '../services/sse_client.dart';
import '../widgets/circuit_visualizer.dart';

final _conversationProvider = StateNotifierProvider<_ConvNotifier, AsyncValue<List<Map<String, dynamic>>>>((ref) {
  return _ConvNotifier();
});

class _ConvNotifier extends StateNotifier<AsyncValue<List<Map<String, dynamic>>>> {
  String _searchQuery = '';

  _ConvNotifier() : super(const AsyncValue.loading());

  Future<void> load() async {
    state = const AsyncValue.loading();
    try {
      final url = _searchQuery.isNotEmpty
          ? ApiEndpoints.conversationSearch(_searchQuery)
          : ApiEndpoints.conversations;
      final resp = await ApiClient.instance.dio.get(url);
      final items = (resp.data['items'] as List?)?.cast<Map<String, dynamic>>() ?? [];
      ConversationCache.save(items);
      state = AsyncValue.data(items);
    } catch (e) {
      final cached = ConversationCache.search(_searchQuery);
      if (cached.isNotEmpty) {
        state = AsyncValue.data(cached);
      } else {
        state = AsyncValue.error(e, StackTrace.current);
      }
    }
  }

  void search(String query) {
    _searchQuery = query;
    load();
  }

  Future<void> refresh() => load();
}

class VoiceScreen extends ConsumerStatefulWidget {
  final int? initialConversationId;
  const VoiceScreen({super.key, this.initialConversationId});

  @override
  ConsumerState<VoiceScreen> createState() => _VoiceScreenState();
}

class _VoiceScreenState extends ConsumerState<VoiceScreen> {
  final _controller = TextEditingController();
  final _scrollController = ScrollController();
  final _messages = <_ChatMessage>[];
  int? _conversationId;
  bool _isLoading = false;
  String _title = 'New Chat';
  bool _showHistory = false;

  @override
  void initState() {
    super.initState();
    _conversationId = widget.initialConversationId;
    WidgetsBinding.instance.addPostFrameCallback((_) => _init());
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _init() async {
    if (_conversationId != null) {
      await _loadConversation(_conversationId!);
    } else {
      _addWelcome();
    }
    ref.read(_conversationProvider.notifier).load();
  }

  void _addWelcome() {
    setState(() {
      _messages.add(_ChatMessage(
        'Hello! I\'m **BreadBoard AI**, your electronics engineering assistant.\n\n'
        'I can help you with:\n'
        '- 🔌 **Circuit design** — describe what you want to build\n'
        '- 💡 **Component specs** — ask about any electronic part\n'
        '- 🔧 **Troubleshooting** — describe your problem\n'
        '- 📚 **Learning** — explain electronics concepts\n\n'
        '> Try: *"Design an LED flasher circuit using a 555 timer"*',
        false,
      ));
    });
  }

  Future<void> _loadConversation(int id) async {
    try {
      final resp = await ApiClient.instance.dio.get(ApiEndpoints.conversation(id));
      final data = resp.data;
      setState(() {
        _title = data['title'] as String? ?? 'Chat';
        final msgs = (data['messages'] as List?) ?? [];
        _messages.clear();
        for (final m in msgs) {
          final role = m['role'] as String?;
          final content = m['content'] as String? ?? '';
          if (role == 'user') {
            _messages.add(_ChatMessage(content, true));
          } else if (role == 'assistant') {
            _messages.add(_ChatMessage(content, false));
          }
        }
      });
    } catch (e) {
      _addWelcome();
    }
  }

  Future<void> _newChat() async {
    final apiMsg = _messages
        .where((m) => m.text.isNotEmpty)
        .map((m) => {'role': m.isUser ? 'user' : 'assistant', 'content': m.text})
        .toList();

    if (apiMsg.isNotEmpty && _conversationId != null) {
      try {
        await ApiClient.instance.dio.put(
          ApiEndpoints.conversation(_conversationId!),
          data: {'messages': apiMsg},
        );
      } catch (_) {}
    }

    setState(() {
      _conversationId = null;
      _title = 'New Chat';
      _messages.clear();
    });
    _addWelcome();
    _controller.clear();
    ref.read(_conversationProvider.notifier).refresh();
  }

  Future<void> _selectConversation(int id) async {
    setState(() {
      _showHistory = false;
      _conversationId = id;
    });
    await _loadConversation(id);
  }

  void _scroll() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 150),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty || _isLoading) return;

    setState(() {
      _messages.add(_ChatMessage(text, true));
      _isLoading = true;
    });
    _controller.clear();
    _scroll();

    final chatMessages = _messages
        .where((m) => m.text.isNotEmpty)
        .map((m) => {'role': m.isUser ? 'user' : 'assistant', 'content': m.text})
        .toList();

    final payload = <String, dynamic>{'messages': chatMessages, 'model': 'llava'};
    if (_conversationId != null) {
      payload['conversation_id'] = _conversationId;
    }

    final baseUrl = ApiClient.instance.dio.options.baseUrl;
    final streamUrl = '$baseUrl${ApiEndpoints.aiChatStream}';

    setState(() {
      _messages.add(_ChatMessage('', false));
    });
    _scroll();

    SseClient? sseClient;

    sseClient = SseClient(
      url: streamUrl,
      body: payload,
      onToken: (token) {
        final idx = _messages.length - 1;
        if (idx >= 0 && idx < _messages.length) {
          _messages[idx] = _ChatMessage(_messages[idx].text + token, false);
          setState(() {});
          _scroll();
        }
      },
      onMeta: (meta) {},
      onDone: (content, meta, convId) {
        setState(() {
          _isLoading = false;
          if (convId != null) _conversationId = convId;
          if (content.isNotEmpty) {
            final idx = _messages.length - 1;
            if (idx >= 0) _messages[idx] = _ChatMessage(content, false);
          }
          if (_conversationId == null && meta?['conversation_id'] != null) {
            _conversationId = meta!['conversation_id'] as int;
          }
          if (_title == 'New Chat' && text.isNotEmpty) {
            _title = text.length > 60 ? '${text.substring(0, 60)}...' : text;
          }
        });
        ref.read(_conversationProvider.notifier).refresh();
      },
      onError: (err) {
        _streamingFallback(text, chatMessages);
      },
    );

    sseClient.connect();
  }

  Future<void> _streamingFallback(String text, List chatMessages) async {
    try {
      final payload = <String, dynamic>{'messages': chatMessages, 'model': 'llava'};
      if (_conversationId != null) payload['conversation_id'] = _conversationId;

      final response = await ApiClient.instance.dio.post(
        ApiEndpoints.aiChat,
        data: payload,
        options: Options(
          receiveTimeout: const Duration(seconds: 120),
          sendTimeout: const Duration(seconds: 60),
        ),
      );
      final result = response.data;
      final reply = result['response'] as String? ?? 'No response';

      if (mounted) {
        setState(() {
          final idx = _messages.length - 1;
          if (idx >= 0) _messages[idx] = _ChatMessage(reply, false);
          _isLoading = false;
          if (result['conversation_id'] != null) {
            _conversationId = result['conversation_id'] as int;
          }
          if (_title == 'New Chat' && text.isNotEmpty) {
            _title = text.length > 60 ? '${text.substring(0, 60)}...' : text;
          }
        });
        _scroll();
        ref.read(_conversationProvider.notifier).refresh();
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          final idx = _messages.length - 1;
          if (idx >= 0) {
            _messages[idx] = _ChatMessage(
              '> **Error**: I encountered a problem. Please make sure the backend and AI engine are running on ports **8000** and **8001**.',
              false,
            );
          }
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;
    final convs = ref.watch(_conversationProvider);

    final mdStyle = MarkdownStyleSheet(
      h1: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      h2: TextStyle(fontSize: 17, fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      h3: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      p: TextStyle(fontSize: 14, height: 1.5, color: isDark ? DSColors.grey100 : DSColors.grey900),
      code: TextStyle(
        fontSize: 13, backgroundColor: isDark ? DSColors.surfaceDarkVariant : DSColors.grey100,
        color: isDark ? DSColors.circuitCyan : DSColors.neonViolet,
      ),
      codeblockDecoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkVariant : DSColors.grey100,
        borderRadius: BorderRadius.circular(8),
      ),
      codeblockPadding: const EdgeInsets.all(12),
      blockquoteDecoration: BoxDecoration(
        border: Border(left: BorderSide(color: DSColors.primary, width: 3)),
        color: isDark ? DSColors.primary.withValues(alpha: 0.08) : DSColors.primary.withValues(alpha: 0.05),
      ),
      blockquotePadding: const EdgeInsets.fromLTRB(12, 4, 8, 4),
      listBullet: TextStyle(fontSize: 14, color: isDark ? DSColors.grey100 : DSColors.grey900),
      tableHead: TextStyle(fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      tableBody: TextStyle(color: isDark ? DSColors.grey100 : DSColors.grey900),
      tableBorder: TableBorder.all(color: isDark ? DSColors.grey600 : DSColors.grey300),
      tableColumnWidth: const FlexColumnWidth(),
      horizontalRuleDecoration: BoxDecoration(border: Border(top: BorderSide(color: isDark ? DSColors.grey600 : DSColors.grey300))),
      strong: TextStyle(fontWeight: FontWeight.bold, color: isDark ? DSColors.white : DSColors.grey900),
      em: TextStyle(fontStyle: FontStyle.italic, color: isDark ? DSColors.grey100 : DSColors.grey900),
      del: TextStyle(decoration: TextDecoration.lineThrough, color: isDark ? DSColors.grey400 : DSColors.grey500),
      a: TextStyle(color: DSColors.circuitCyan, decoration: TextDecoration.underline),
      checkbox: TextStyle(color: DSColors.circuitCyan),
    );

    return Scaffold(
      appBar: AppBar(
        title: Text(_title, overflow: TextOverflow.ellipsis),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            tooltip: 'Conversation History',
            onPressed: () => setState(() => _showHistory = !_showHistory),
          ),
          IconButton(
            icon: const Icon(Icons.add),
            tooltip: 'New Chat',
            onPressed: _newChat,
          ),
        ],
      ),
      body: Row(
        children: [
          if (_showHistory)
            SizedBox(
              width: isWide ? 300 : 260,
              child: ConversationList(
                conversations: convs,
                selectedId: _conversationId,
                onSelect: _selectConversation,
                onNewChat: _newChat,
                onSearch: (q) => ref.read(_conversationProvider.notifier).search(q),
              ),
            ),
          Expanded(
            child: Column(
              children: [
                Expanded(
                  child: _messages.isEmpty && !_isLoading
                      ? _buildEmptyState(isDark)
                      : ListView.builder(
                          controller: _scrollController,
                          padding: const EdgeInsets.all(16),
                          itemCount: _messages.length + (_isLoading ? 1 : 0),
                          itemBuilder: (_, i) {
                            if (_isLoading && i == _messages.length) {
                              return _buildThinking(isDark);
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
                                constraints: BoxConstraints(
                                  maxWidth: isWide ? 640 : MediaQuery.of(context).size.width * 0.85,
                                  minWidth: 80,
                                ),
                                child: Column(
                                  crossAxisAlignment: msg.isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    msg.isUser
                                        ? Text(msg.text, style: const TextStyle(color: Colors.white, fontSize: 14))
                                        : MarkdownBody(
                                            data: msg.text,
                                            styleSheet: mdStyle,
                                            selectable: true,
                                          ),
                                    if (!msg.isUser)
                                      Padding(
                                        padding: const EdgeInsets.only(top: 4),
                                        child: CircuitVisualizer(markdown: msg.text, compact: true),
                                      ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                ),
                _buildInputBar(isDark, isWide),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildThinking(bool isDark) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          const SizedBox(width: 48),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: isDark ? DSColors.surfaceDarkCard : DSColors.grey50,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                SizedBox(
                  width: 16, height: 16,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: DSColors.primary,
                  ),
                ),
                const SizedBox(width: 10),
                Text('Thinking...', style: TextStyle(fontSize: 13, color: isDark ? DSColors.grey300 : DSColors.grey500)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState(bool isDark) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(24),
            decoration: BoxDecoration(gradient: DSGradients.primaryGradient, shape: BoxShape.circle),
            child: const Icon(Icons.mic, size: 48, color: Colors.white),
          ),
          const SizedBox(height: 24),
          Text('Ask me anything about electronics', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          Text('e.g. "Design an LED flasher circuit"', style: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500)),
        ],
      ),
    );
  }

  Widget _buildInputBar(bool isDark, bool isWide) {
    return Container(
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
    );
  }
}

class _ChatMessage {
  final String text;
  final bool isUser;
  const _ChatMessage(this.text, this.isUser);
}
