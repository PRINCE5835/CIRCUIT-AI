import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class ProfileScreen extends ConsumerStatefulWidget {
  const ProfileScreen({super.key});

  @override
  ConsumerState<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends ConsumerState<ProfileScreen> {
  final _nameController = TextEditingController();
  bool _isSaving = false;

  @override
  void initState() {
    super.initState();
    final user = ref.read(authProvider).user;
    if (user != null) {
      _nameController.text = user['display_name'] as String? ?? user['username'] as String? ?? '';
    }
  }

  @override
  void dispose() {
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _updateName() async {
    final name = _nameController.text.trim();
    if (name.isEmpty) return;
    setState(() => _isSaving = true);
    try {
      await ApiClient.instance.dio.patch(ApiEndpoints.profile, data: {'display_name': name});
      await ref.read(authProvider.notifier).fetchProfile();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Name updated'), duration: Duration(seconds: 2)),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to update name'), duration: Duration(seconds: 2)),
        );
      }
    }
    if (mounted) setState(() => _isSaving = false);
  }

  Future<void> _signOut() async {
    await ref.read(authProvider.notifier).logout();
    if (mounted) context.go(RoutePaths.login);
  }

  Future<void> _deleteAccount() async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Delete Account'),
        content: const Text('This action is permanent and irreversible. All your data will be deleted.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
    if (confirmed != true) return;
    try {
      await ApiClient.instance.dio.delete(ApiEndpoints.profile);
      await ref.read(authProvider.notifier).logout();
      if (mounted) context.go(RoutePaths.login);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to delete account'), duration: Duration(seconds: 2)),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;
    final themeMode = ref.watch(themeModeProvider);
    final locale = ref.watch(localeProvider);
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final displayName = user?['display_name'] as String? ?? user?['username'] as String? ?? 'User';
    final email = user?['email'] as String? ?? '';

    if (user != null && _nameController.text.isEmpty) {
      _nameController.text = displayName;
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Profile & Settings')),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(isWide ? 48 : 16),
        child: Center(
          child: Container(
            constraints: const BoxConstraints(maxWidth: 500),
            child: Column(
              children: [
                const SizedBox(height: 20),
                // Avatar
                Container(
                  width: 80, height: 80,
                  decoration: BoxDecoration(
                    gradient: DSGradients.primaryGradient,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(Icons.person, size: 40, color: Colors.white),
                ),
                const SizedBox(height: 16),
                Text(displayName, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w700)),
                const SizedBox(height: 4),
                Text(email, style: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500)),
                const SizedBox(height: 32),
                // ── Edit Name ──
                _SectionHeader(title: 'Profile'),
                _SettingsTile(
                  icon: Icons.person_outline,
                  title: 'Full Name',
                  trailing: SizedBox(
                    width: 200,
                    child: TextField(
                      controller: _nameController,
                      decoration: const InputDecoration(
                        border: OutlineInputBorder(),
                        isDense: true,
                        contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 8),
                      ),
                      style: const TextStyle(fontSize: 14),
                    ),
                  ),
                ),
                Align(
                  alignment: Alignment.centerRight,
                  child: Padding(
                    padding: const EdgeInsets.only(bottom: 16),
                    child: _isSaving
                        ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(strokeWidth: 2))
                        : Semantics(
                            label: 'Save name',
                            button: true,
                            child: FilledButton.icon(
                              onPressed: _updateName,
                              icon: const Icon(Icons.save, size: 18),
                              label: const Text('Save'),
                            ),
                          ),
                  ),
                ),
                // ── Settings ──
                _SectionHeader(title: 'Preferences'),
                _SettingsTile(
                  icon: Icons.light_mode_outlined,
                  title: 'Dark Mode',
                  trailing: Switch(
                    value: themeMode == ThemeMode.dark,
                    onChanged: (_) => ref.read(themeModeProvider.notifier).toggle(),
                    activeTrackColor: DSColors.primary,
                  ),
                ),
                _SettingsTile(
                  icon: Icons.language,
                  title: 'Language',
                  trailing: DropdownButton<String>(
                    value: locale.languageCode,
                    underline: const SizedBox(),
                    items: const [
                      DropdownMenuItem(value: 'en', child: Text('English')),
                      DropdownMenuItem(value: 'hi', child: Text('हिन्दी')),
                    ],
                    onChanged: (v) {
                      if (v != null) ref.read(localeProvider.notifier).setLocale(v);
                    },
                  ),
                ),
                const SizedBox(height: 16),
                // ── Support ──
                _SectionHeader(title: 'Support'),
                _SettingsTile(
                  icon: Icons.mail_outline,
                  title: 'Email',
                  trailing: Text('support@breadboard.ai', style: TextStyle(fontSize: 13, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                ),
                _SettingsTile(
                  icon: Icons.phone_outlined,
                  title: 'Phone',
                  trailing: Text('+91-1800-123-4567', style: TextStyle(fontSize: 13, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                ),
                const SizedBox(height: 16),
                // ── About ──
                _SectionHeader(title: 'About'),
                _SettingsTile(
                  icon: Icons.info_outline,
                  title: 'Version',
                  trailing: Text('0.1.0', style: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500)),
                ),
                const SizedBox(height: 16),
                // ── Danger Zone ──
                _SectionHeader(title: 'Danger Zone', color: DSColors.danger),
                Container(
                  margin: const EdgeInsets.only(bottom: 4),
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: DSColors.danger.withValues(alpha: 0.3)),
                  ),
                  child: ListTile(
                    leading: Icon(Icons.delete_forever, color: DSColors.danger),
                    title: Text('Delete Account', style: TextStyle(color: DSColors.danger, fontWeight: FontWeight.w600)),
                    subtitle: Text('Permanently delete your account and all data', style: TextStyle(fontSize: 12, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                    trailing: TextButton(
                      onPressed: _deleteAccount,
                      child: const Text('Delete', style: TextStyle(color: DSColors.danger)),
                    ),
                  ),
                ),
                const SizedBox(height: 32),
                // ── Sign Out ──
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    onPressed: _signOut,
                    icon: const Icon(Icons.logout),
                    label: const Text('Sign Out'),
                    style: OutlinedButton.styleFrom(
                      foregroundColor: DSColors.danger,
                      side: const BorderSide(color: DSColors.danger),
                      padding: const EdgeInsets.symmetric(vertical: 14),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  ),
                ),
                const SizedBox(height: 32),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _SettingsTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final Widget trailing;
  const _SettingsTile({required this.icon, required this.title, required this.trailing});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
      ),
      child: ListTile(
        leading: Icon(icon, color: DSColors.primary),
        title: Text(title, style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900)),
        trailing: trailing,
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  final String title;
  final Color? color;
  const _SectionHeader({required this.title, this.color});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8, top: 8),
      child: Align(
        alignment: Alignment.centerLeft,
        child: Text(
          title,
          style: TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.w600,
            color: color ?? DSColors.primary,
            letterSpacing: 0.5,
          ),
        ),
      ),
    );
  }
}
