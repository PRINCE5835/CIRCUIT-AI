import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import '../../../../core/services/api_service.dart';

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
      final data = await ApiService.getProjects();
      if (mounted) setState(() => _projects = data['items'] as List<dynamic>? ?? []);
    } catch (_) {}
    if (mounted) setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Project History')),
      body: _isLoading
          ? const Center(child: CircuitSpinner(size: 32))
          : _projects.isEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(DSDimensions.s32),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.folder_open_outlined, size: 80,
                            color: theme.colorScheme.onSurface.withValues(alpha: 0.2)),
                        const SizedBox(height: DSDimensions.s16),
                        Text('No projects yet', style: theme.textTheme.titleLarge?.copyWith(
                          color: theme.colorScheme.onSurface.withValues(alpha: 0.5),
                        )),
                        const SizedBox(height: DSDimensions.s8),
                        Text(
                          'Your circuit projects will appear here',
                          style: theme.textTheme.bodyMedium?.copyWith(
                            color: theme.colorScheme.onSurface.withValues(alpha: 0.3),
                          ),
                        ),
                      ],
                    ),
                  ),
                )
              : RefreshIndicator(
                  onRefresh: _loadProjects,
                  child: ListView.separated(
                    padding: const EdgeInsets.all(DSDimensions.s16),
                    itemCount: _projects.length,
                    separatorBuilder: (_, __) => const Divider(),
                    itemBuilder: (context, index) {
                      final project = _projects[index] as Map<String, dynamic>;
                      return ListTile(
                        leading: const Icon(Icons.circle_outlined, color: DSColors.primary),
                        title: Text(project['title'] as String? ?? 'Untitled'),
                        subtitle: Text(project['description'] as String? ?? ''),
                        trailing: Text(project['status'] as String? ?? 'draft'),
                      );
                    },
                  ),
                ),
    );
  }
}
