import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import '../../../../core/services/api_service.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
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

  static final _quickActions = [
    _QuickAction(Icons.circle_outlined, 'Generate Circuit', DSColors.circuitCyan, RoutePaths.circuitGeneration),
    _QuickAction(Icons.menu_book_outlined, 'Learn Circuits', DSColors.neonViolet, RoutePaths.circuitLearning),
    _QuickAction(Icons.build_outlined, 'Repair Assistant', DSColors.warmAmber, RoutePaths.repairAssistant),
    _QuickAction(Icons.verified_outlined, 'Verify Layout', DSColors.neonViolet, RoutePaths.breadboardVerification),
    _QuickAction(Icons.monetization_on_outlined, 'Cost Estimate', DSColors.tertiary, RoutePaths.costEstimation),
    _QuickAction(Icons.shield_outlined, 'Safety Check', DSColors.safe, RoutePaths.safetyValidation),
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final l10n = AppLocalizations.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('BreadBoard AI'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings_outlined),
            onPressed: () => context.go(RoutePaths.settings),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DSDimensions.s16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildGreeting(theme, l10n),
            const SizedBox(height: DSDimensions.s24),
            SectionHeader(title: 'Quick Actions'),
            const SizedBox(height: DSDimensions.s12),
            _buildQuickActions(context),
            const SizedBox(height: DSDimensions.s24),
            SectionHeader(title: 'Recent Projects'),
            const SizedBox(height: DSDimensions.s12),
            _buildRecentProjects(theme),
          ],
        ),
      ),
    );
  }

  Widget _buildGreeting(ThemeData theme, AppLocalizations l10n) {
    final hour = DateTime.now().hour;
    final greeting = hour < 12 ? 'Good Morning' : hour < 17 ? 'Good Afternoon' : 'Good Evening';

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(greeting, style: theme.textTheme.headlineMedium),
        const SizedBox(height: DSDimensions.s4),
        Text(
          'What would you like to build today?',
          style: theme.textTheme.bodyLarge?.copyWith(color: theme.colorScheme.onSurface.withValues(alpha: 0.6)),
        ),
      ],
    );
  }

  Widget _buildQuickActions(BuildContext context) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 1.1,
        crossAxisSpacing: DSDimensions.s12,
        mainAxisSpacing: DSDimensions.s12,
      ),
      itemCount: _quickActions.length,
      itemBuilder: (context, index) {
        final action = _quickActions[index];
        return GlowCard(
          child: InkWell(
            onTap: () => context.go(action.route),
            borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
            child: Padding(
              padding: const EdgeInsets.all(DSDimensions.s16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(action.icon, size: 24, color: action.color),
                  const SizedBox(height: DSDimensions.s8),
                  Text(
                    action.label,
                    style: Theme.of(context).textTheme.labelLarge,
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            ),
          ),
        ).animate().fadeIn(duration: 400.ms, delay: (100 * index).ms).slideY(begin: 0.1);
      },
    );
  }

  Widget _buildRecentProjects(ThemeData theme) {
    if (_isLoading) {
      return const Center(child: CircuitSpinner(size: 32));
    }
    if (_projects.isEmpty) {
      return AppCard(
        child: Padding(
          padding: const EdgeInsets.all(DSDimensions.s24),
          child: Center(
            child: Column(
              children: [
                Icon(Icons.history, size: 36, color: theme.colorScheme.onSurface.withValues(alpha: 0.3)),
                const SizedBox(height: DSDimensions.s12),
                Text(
                  'No projects yet',
                  style: theme.textTheme.bodyLarge?.copyWith(
                    color: theme.colorScheme.onSurface.withValues(alpha: 0.5),
                  ),
                ),
                const SizedBox(height: DSDimensions.s4),
                Text(
                  'Start by generating a circuit',
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.colorScheme.onSurface.withValues(alpha: 0.3),
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }
    return Padding(
      padding: const EdgeInsets.only(bottom: DSDimensions.s8),
      child: Column(
        children: _projects.take(3).map((p) {
          final project = p as Map<String, dynamic>;
          return Padding(
            padding: const EdgeInsets.only(bottom: DSDimensions.s8),
            child: AppCard(
              child: ListTile(
                leading: const Icon(Icons.circle_outlined, color: DSColors.primary),
                title: Text(project['title'] as String? ?? 'Untitled'),
                subtitle: Text(project['description'] as String? ?? ''),
                trailing: Chip(label: Text(project['status'] as String? ?? 'draft')),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }
}

class _QuickAction {
  final IconData icon;
  final String label;
  final Color color;
  final String route;
  const _QuickAction(this.icon, this.label, this.color, this.route);
}
