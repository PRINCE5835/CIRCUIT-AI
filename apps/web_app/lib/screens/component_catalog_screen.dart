import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart' hide EmptyState;
import '../widgets/empty_state.dart';

class ComponentCatalogScreen extends ConsumerStatefulWidget {
  const ComponentCatalogScreen({super.key});

  @override
  ConsumerState<ComponentCatalogScreen> createState() => _ComponentCatalogScreenState();
}

class _ComponentCatalogScreenState extends ConsumerState<ComponentCatalogScreen> {
  List<Map<String, dynamic>> _components = [];
  bool _isLoading = true;
  final _searchController = TextEditingController();
  String _query = '';

  @override
  void initState() {
    super.initState();
    _load();
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _load() async {
    setState(() => _isLoading = true);
    try {
      final url = _query.isNotEmpty
          ? '${ApiEndpoints.components}?query=${Uri.encodeComponent(_query)}&limit=100'
          : '${ApiEndpoints.components}?limit=100';
      final resp = await ApiClient.instance.dio.get(url);
      final items = (resp.data['items'] as List?)?.cast<Map<String, dynamic>>() ?? [];
      if (mounted) setState(() => _components = items);
    } catch (_) {}
    if (mounted) setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Component Catalog')),
      body: Column(
        children: [
          Padding(
            padding: EdgeInsets.fromLTRB(isWide ? 48 : 16, 16, isWide ? 48 : 16, 8),
            child: TextField(
              controller: _searchController,
              onSubmitted: (v) {
                _query = v;
                _load();
              },
              style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900),
              decoration: InputDecoration(
                hintText: 'Search components...',
                hintStyle: TextStyle(color: isDark ? DSColors.grey500 : DSColors.grey400),
                prefixIcon: Icon(Icons.search, color: isDark ? DSColors.grey400 : DSColors.grey500),
                suffixIcon: _searchController.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear, size: 18),
                        onPressed: () {
                          _searchController.clear();
                          _query = '';
                          _load();
                        },
                      )
                    : null,
                filled: true,
                fillColor: isDark ? DSColors.surfaceDarkCard : DSColors.grey50,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                  borderSide: BorderSide.none,
                ),
                contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              ),
            ),
          ),
          Expanded(
            child: _isLoading
                ? const Center(child: CircularProgressIndicator(strokeWidth: 2))
                : _components.isEmpty
                    ? const EmptyState(icon: Icons.inventory_2_outlined, title: 'No components found', subtitle: 'Try a different search term')
                    : ListView.builder(
                        padding: EdgeInsets.fromLTRB(isWide ? 48 : 16, 0, isWide ? 48 : 16, 16),
                        itemCount: _components.length,
                        itemBuilder: (context, i) {
                          final c = _components[i];
                          return Card(
                            margin: const EdgeInsets.only(bottom: 8),
                            child: ListTile(
                              leading: Container(
                                width: 44, height: 44,
                                decoration: BoxDecoration(
                                  color: _categoryColor(c['category'] as String? ?? '').withValues(alpha: 0.15),
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                child: Icon(
                                  _categoryIcon(c['category'] as String? ?? ''),
                                  color: _categoryColor(c['category'] as String? ?? ''),
                                  size: 22,
                                ),
                              ),
                              title: Text(c['name'] as String? ?? '', style: const TextStyle(fontWeight: FontWeight.w600)),
                              subtitle: Text([
                                if (c['category'] != null) c['category'],
                                if (c['manufacturer'] != null) c['manufacturer'],
                                if (c['model_number'] != null) c['model_number'],
                              ].join('  ·  '), style: TextStyle(fontSize: 12, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                              trailing: const Icon(Icons.chevron_right, size: 18),
                              onTap: () => _showDetail(c),
                            ),
                          );
                        },
                      ),
          ),
        ],
      ),
    );
  }

  void _showDetail(Map<String, dynamic> c) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
      ),
      builder: (ctx) => DraggableScrollableSheet(
        initialChildSize: 0.6,
        maxChildSize: 0.9,
        expand: false,
        builder: (_, scrollController) => SingleChildScrollView(
          controller: scrollController,
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Container(
                  width: 40, height: 4,
                  decoration: BoxDecoration(
                    color: Colors.grey.shade300,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text(c['name'] as String? ?? '', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
              if (c['manufacturer'] != null) ...[
                const SizedBox(height: 4),
                Text(c['manufacturer'] as String, style: TextStyle(color: Theme.of(context).colorScheme.primary)),
              ],
              const Divider(height: 24),
              _detailRow('Category', c['category'] as String?),
              _detailRow('Subcategory', c['subcategory'] as String?),
              _detailRow('Model Number', c['model_number'] as String?),
              if (c['description'] != null) ...[
                const SizedBox(height: 8),
                Text('Description', style: Theme.of(context).textTheme.titleSmall),
                const SizedBox(height: 4),
                Text(c['description'] as String),
              ],
              if (c['datasheet_url'] != null) ...[
                const SizedBox(height: 16),
                FilledButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.description, size: 18),
                  label: const Text('View Datasheet'),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _detailRow(String label, String? value) {
    if (value == null) return const SizedBox.shrink();
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        children: [
          Text('$label: ', style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13)),
          Expanded(child: Text(value, style: const TextStyle(fontSize: 13))),
        ],
      ),
    );
  }

  Color _categoryColor(String cat) {
    switch (cat.toLowerCase()) {
      case 'resistor': return Colors.brown;
      case 'capacitor': return Colors.orange;
      case 'ic': case 'integrated circuit': return Colors.indigo;
      case 'connector': return Colors.blue;
      case 'sensor': return Colors.teal;
      case 'power': return Colors.green;
      case 'led': case 'opto': return Colors.red;
      default: return DSColors.primary;
    }
  }

  IconData _categoryIcon(String cat) {
    switch (cat.toLowerCase()) {
      case 'resistor': return Icons.timeline;
      case 'capacitor': return Icons.linear_scale;
      case 'ic': case 'integrated circuit': return Icons.memory;
      case 'connector': return Icons.cable;
      case 'sensor': return Icons.sensors;
      case 'power': return Icons.battery_std;
      case 'led': case 'opto': return Icons.circle;
      default: return Icons.inventory_2_outlined;
    }
  }
}
