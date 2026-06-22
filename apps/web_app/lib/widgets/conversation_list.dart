import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class ConversationList extends ConsumerStatefulWidget {
  final AsyncValue<List<Map<String, dynamic>>> conversations;
  final int? selectedId;
  final ValueChanged<int> onSelect;
  final VoidCallback onNewChat;
  final ValueChanged<String> onSearch;

  const ConversationList({
    super.key,
    required this.conversations,
    this.selectedId,
    required this.onSelect,
    required this.onNewChat,
    required this.onSearch,
  });

  @override
  ConsumerState<ConversationList> createState() => _ConversationListState();
}

class _ConversationListState extends ConsumerState<ConversationList> {
  final _searchController = TextEditingController();
  bool _showSearch = false;
  String _searchQuery = '';

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged(String value) {
    _searchQuery = value;
    widget.onSearch(value);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkElevated : DSColors.grey50,
        border: Border(
          right: BorderSide(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
        ),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.fromLTRB(12, 12, 12, 0),
            child: Column(
              children: [
                Row(
                  children: [
                    Icon(Icons.history, size: 20, color: isDark ? DSColors.grey300 : DSColors.grey700),
                    const SizedBox(width: 8),
                    Text('History', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w600, color: isDark ? DSColors.grey100 : DSColors.grey900)),
                    const Spacer(),
                    IconButton(
                      icon: Icon(
                        _showSearch ? Icons.search_off : Icons.search,
                        size: 20,
                        color: isDark ? DSColors.grey300 : DSColors.grey700,
                      ),
                      onPressed: () {
                        setState(() {
                          _showSearch = !_showSearch;
                          if (!_showSearch) {
                            _searchController.clear();
                            _onSearchChanged('');
                          }
                        });
                      },
                      visualDensity: VisualDensity.compact,
                      tooltip: _showSearch ? 'Close search' : 'Search conversations',
                    ),
                    Container(
                      decoration: BoxDecoration(
                        gradient: DSGradients.primaryGradient,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Material(
                        color: Colors.transparent,
                        child: InkWell(
                          borderRadius: BorderRadius.circular(8),
                          onTap: widget.onNewChat,
                          child: const Padding(
                            padding: EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Icon(Icons.add, size: 16, color: Colors.white),
                                SizedBox(width: 4),
                                Text('New', style: TextStyle(fontSize: 12, color: Colors.white, fontWeight: FontWeight.w600)),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                if (_showSearch) ...[
                  const SizedBox(height: 8),
                  TextField(
                    controller: _searchController,
                    autofocus: true,
                    onChanged: _onSearchChanged,
                    style: TextStyle(fontSize: 13, color: isDark ? DSColors.white : DSColors.grey900),
                    decoration: InputDecoration(
                      hintText: 'Search conversations...',
                      hintStyle: TextStyle(fontSize: 13, color: isDark ? DSColors.grey500 : DSColors.grey400),
                      prefixIcon: Icon(Icons.search, size: 16, color: isDark ? DSColors.grey400 : DSColors.grey500),
                      suffixIcon: _searchQuery.isNotEmpty
                          ? IconButton(
                              icon: Icon(Icons.clear, size: 16),
                              onPressed: () {
                                _searchController.clear();
                                _onSearchChanged('');
                              },
                            )
                          : null,
                      filled: true,
                      fillColor: isDark ? DSColors.surfaceDarkVariant : DSColors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                        borderSide: BorderSide.none,
                      ),
                      contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
                      isDense: true,
                    ),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: 8),
          const Divider(height: 1),
          Expanded(
            child: widget.conversations.when(
              loading: () => const Center(child: CircularProgressIndicator(strokeWidth: 2)),
              error: (e, _) => Center(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.cloud_off, color: isDark ? DSColors.grey400 : DSColors.grey500),
                      const SizedBox(height: 8),
                      Text('Could not load history', style: TextStyle(fontSize: 12, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                    ],
                  ),
                ),
              ),
              data: (items) {
                if (items.isEmpty) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Text(
                        _searchQuery.isNotEmpty ? 'No matching conversations' : 'No conversations yet',
                        style: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500),
                      ),
                    ),
                  );
                }
                return ListView.separated(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  itemCount: items.length,
                  separatorBuilder: (_, __) => const Divider(height: 1, indent: 16, endIndent: 16),
                  itemBuilder: (_, i) {
                    final c = items[i];
                    final id = c['id'] as int;
                    final title = c['title'] as String? ?? 'Chat';
                    final msgCount = c['message_count'] as int? ?? 0;
                    final updated = c['updated_at'] as String? ?? '';
                    final selected = id == widget.selectedId;

                    return Container(
                      color: selected ? DSColors.primary.withValues(alpha: 0.08) : null,
                      child: ListTile(
                        dense: true,
                        leading: Icon(
                          Icons.chat_outlined,
                          size: 20,
                          color: selected ? DSColors.primary : (isDark ? DSColors.grey400 : DSColors.grey500),
                        ),
                        title: _searchQuery.isNotEmpty
                            ? _highlightedTitle(title, _searchQuery, isDark, selected)
                            : Text(
                                title,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                                style: TextStyle(
                                  fontSize: 13,
                                  fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
                                  color: selected ? DSColors.primary : (isDark ? DSColors.grey100 : DSColors.grey900),
                                ),
                              ),
                        subtitle: Row(
                          children: [
                            Text('$msgCount msgs', style: TextStyle(fontSize: 11, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                            if (updated.length >= 10) ...[
                              const SizedBox(width: 8),
                              Text(updated.substring(0, 10), style: TextStyle(fontSize: 11, color: isDark ? DSColors.grey500 : DSColors.grey400)),
                            ],
                          ],
                        ),
                        onTap: () => widget.onSelect(id),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _highlightedTitle(String title, String query, bool isDark, bool selected) {
    final lowerTitle = title.toLowerCase();
    final lowerQuery = query.toLowerCase();
    final idx = lowerTitle.indexOf(lowerQuery);
    if (idx == -1) {
      return Text(
        title,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
        style: TextStyle(
          fontSize: 13,
          fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
          color: selected ? DSColors.primary : (isDark ? DSColors.grey100 : DSColors.grey900),
        ),
      );
    }

    return RichText(
      maxLines: 1,
      overflow: TextOverflow.ellipsis,
      text: TextSpan(
        style: TextStyle(
          fontSize: 13,
          fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
          color: selected ? DSColors.primary : (isDark ? DSColors.grey100 : DSColors.grey900),
        ),
        children: [
          TextSpan(text: title.substring(0, idx)),
          TextSpan(
            text: title.substring(idx, idx + query.length),
            style: TextStyle(
              backgroundColor: DSColors.primary.withValues(alpha: 0.2),
              fontWeight: FontWeight.w700,
            ),
          ),
          TextSpan(text: title.substring(idx + query.length)),
        ],
      ),
    );
  }
}
