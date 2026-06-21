import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

import '../../../../core/services/api_service.dart';

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  Map<String, dynamic>? _user;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    try {
      final user = await ApiService.getProfile();
      if (mounted) setState(() => _user = user);
    } catch (_) {}
    if (mounted) setState(() => _isLoading = false);
  }

  Future<void> _logout() async {
    await ref.read(authProvider.notifier).logout();
    if (!mounted) return;
    context.go(RoutePaths.splash);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final displayName = _user?['display_name'] as String? ?? _user?['username'] as String? ?? 'User';
    final email = _user?['email'] as String? ?? '';

    return Scaffold(
      appBar: AppBar(title: const Text('Profile')),
      body: _isLoading
          ? const Center(child: CircuitSpinner(size: 32))
          : ListView(
              padding: const EdgeInsets.all(DSDimensions.s16),
              children: [
                Center(
                  child: Column(
                    children: [
                      CircleAvatar(
                        radius: 48,
                        backgroundColor: DSColors.primary.withValues(alpha: 0.15),
                        child: const Icon(Icons.person, size: 48, color: DSColors.primary),
                      ),
                      const SizedBox(height: DSDimensions.s12),
                      Text(displayName, style: theme.textTheme.titleLarge),
                      const SizedBox(height: DSDimensions.s4),
                      Text(email, style: theme.textTheme.bodySmall?.copyWith(
                        color: theme.colorScheme.onSurface.withValues(alpha: 0.5),
                      )),
                    ],
                  ),
                ),
                const SizedBox(height: DSDimensions.s32),
                _buildMenuItem(theme, Icons.history, 'Project History', () => context.go(RoutePaths.projectHistory)),
                _buildMenuItem(theme, Icons.settings_outlined, 'Settings', () => context.go(RoutePaths.settings)),
                const Divider(height: DSDimensions.s32),
                _buildMenuItem(theme, Icons.logout, 'Logout', _logout, color: DSColors.danger),
              ],
            ),
    );
  }

  Widget _buildMenuItem(ThemeData theme, IconData icon, String label, VoidCallback onTap, {Color? color}) {
    return ListTile(
      leading: Icon(icon, color: color ?? theme.colorScheme.onSurface),
      title: Text(label, style: TextStyle(color: color)),
      trailing: const Icon(Icons.chevron_right),
      onTap: onTap,
    );
  }
}
