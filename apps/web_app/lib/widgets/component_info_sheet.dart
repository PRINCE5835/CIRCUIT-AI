import 'package:flutter/material.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class ComponentInfoSheet extends StatefulWidget {
  final String componentName;
  final bool showDetails;

  const ComponentInfoSheet({
    super.key,
    required this.componentName,
    this.showDetails = false,
  });

  @override
  State<ComponentInfoSheet> createState() => _ComponentInfoSheetState();
}

class _ComponentInfoSheetState extends State<ComponentInfoSheet> {
  Map<String, dynamic>? _data;
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    try {
      final path = widget.showDetails
          ? ApiEndpoints.wikiComponentDetailsPath(widget.componentName)
          : ApiEndpoints.wikiComponentInfoPath(widget.componentName);
      final response = await ApiClient.instance.dio.get(path);
      setState(() {
        _data = response.data;
        _loading = false;
      });
    } catch (e) {
      setState(() {
        _loading = false;
        _error = e.toString();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return DraggableScrollableSheet(
      initialChildSize: 0.6,
      maxChildSize: 0.9,
      minChildSize: 0.4,
      expand: false,
      builder: (context, scrollController) {
        return Container(
          decoration: const BoxDecoration(
            color: Color(0xFF1A1A2E),
            borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
          ),
          child: _buildBody(scrollController),
        );
      },
    );
  }

  Widget _buildBody(ScrollController scrollController) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
              const SizedBox(height: 16),
              Text(_error!, style: const TextStyle(color: Colors.white70)),
              const SizedBox(height: 16),
              ElevatedButton(onPressed: _fetch, child: const Text('Retry')),
            ],
          ),
        ),
      );
    }
    if (_data == null) {
      return const Center(child: Text('No data', style: TextStyle(color: Colors.white54)));
    }

    return ListView(
      controller: scrollController,
      padding: const EdgeInsets.all(20),
      children: [
        _buildHeader(),
        if (_data!.containsKey('thumbnail') && _data!['thumbnail'] != null) ...[
          const SizedBox(height: 16),
          _buildThumbnail(),
        ],
        if (_data!.containsKey('summary') && _data!['summary'] != null) ...[
          const SizedBox(height: 20),
          _buildSectionTitle('Summary'),
          const SizedBox(height: 8),
          Text(_data!['summary'], style: const TextStyle(color: Colors.white70, height: 1.5)),
        ],
        if (_data!.containsKey('url') && _data!['url'] != null) ...[
          const SizedBox(height: 20),
          _buildLinkButton(),
        ],
        if (_data!.containsKey('datasheets') && (_data!['datasheets'] as List).isNotEmpty) ...[
          const SizedBox(height: 20),
          _buildSectionTitle('Datasheets'),
          ...(_data!['datasheets'] as List).map((d) => _buildRelatedItem(d)),
        ],
        if (_data!.containsKey('applications') && (_data!['applications'] as List).isNotEmpty) ...[
          const SizedBox(height: 20),
          _buildSectionTitle('Applications'),
          ...(_data!['applications'] as List).map((a) => _buildRelatedItem(a)),
        ],
        if (_data!.containsKey('alternatives') && (_data!['alternatives'] as List).isNotEmpty) ...[
          const SizedBox(height: 20),
          _buildSectionTitle('Alternatives'),
          ...(_data!['alternatives'] as List).map((a) => _buildRelatedItem(a)),
        ],
        if (_data!.containsKey('related') && (_data!['related'] as List).isNotEmpty) ...[
          const SizedBox(height: 20),
          _buildSectionTitle('Related Components'),
          ...(_data!['related'] as List).map((r) => _buildRelatedItem(r)),
        ],
        const SizedBox(height: 40),
      ],
    );
  }

  Widget _buildHeader() {
    final title = _data!['wikipedia_title'] ?? _data!['name'] ?? '';
    return Text(title, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white));
  }

  Widget _buildThumbnail() {
    final url = _data!['thumbnail'] as String;
    return ClipRRect(
      borderRadius: BorderRadius.circular(12),
      child: Image.network(url, height: 200, width: double.infinity, fit: BoxFit.contain,
          errorBuilder: (_, __, ___) => const SizedBox.shrink()),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600, color: Colors.cyanAccent));
  }

  Widget _buildLinkButton() {
    return OutlinedButton.icon(
      onPressed: () {},
      icon: const Icon(Icons.open_in_new, size: 18),
      label: const Text('View on Wikipedia'),
      style: OutlinedButton.styleFrom(foregroundColor: Colors.cyanAccent, side: const BorderSide(color: Colors.cyanAccent)),
    );
  }

  Widget _buildRelatedItem(dynamic item) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: InkWell(
        onTap: item['url'] != null ? () {} : null,
        child: Row(
          children: [
            const Icon(Icons.chevron_right, color: Colors.cyanAccent, size: 18),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                item['title'] ?? '',
                style: const TextStyle(color: Colors.white70, decoration: TextDecoration.underline, decorationColor: Colors.white38),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
