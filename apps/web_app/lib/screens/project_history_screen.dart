import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class ProjectHistoryScreen extends ConsumerStatefulWidget {
  const ProjectHistoryScreen({super.key});

  @override
  ConsumerState<ProjectHistoryScreen> createState() => _ProjectHistoryScreenState();
}

class _ProjectHistoryScreenState extends ConsumerState<ProjectHistoryScreen> {
  List<dynamic> _projects = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProjects();
  }

  Future<void> _loadProjects() async {
    try {
      final resp = await ApiClient.instance.dio.get(ApiEndpoints.projects);
      final items = resp.data['items'] as List<dynamic>? ?? [];
      if (mounted) setState(() => _projects = items);
    } catch (_) {}
    if (mounted) setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;

    return Scaffold(
      appBar: AppBar(title: const Text('Project History')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(strokeWidth: 2))
          : _projects.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(32),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.folder_open_outlined, size: 80,
                            color: isDark ? DSColors.grey600 : DSColors.grey300),
                        const SizedBox(height: 16),
                        Text('No projects yet',
                            style: Theme.of(context).textTheme.titleLarge?.copyWith(
                              color: isDark ? DSColors.grey400 : DSColors.grey500)),
                        const SizedBox(height: 8),
                        Text('Your circuit projects will appear here',
                            style: TextStyle(color: isDark ? DSColors.grey500 : DSColors.grey400)),
                      ],
                    ),
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _loadProjects,
                  child: ListView.separated(
                    padding: EdgeInsets.all(isWide ? 48 : 16),
                    itemCount: _projects.length,
                    separatorBuilder: (_, __) => const Divider(),
                    itemBuilder: (context, index) {
                      final project = _projects[index] as Map<String, dynamic>;
                      return ListTile(
                        leading: const Icon(Icons.circle_outlined, color: DSColors.primary),
                        title: Text(project['title'] as String? ?? 'Untitled'),
                        subtitle: Text(project['description'] as String? ?? ''),
                        trailing: Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: DSColors.primary.withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text(
                            project['status'] as String? ?? 'draft',
                            style: TextStyle(fontSize: 11, color: DSColors.primary),
                          ),
                        ),
                      );
                    },
                  ),
                ),
    );
  }
}
