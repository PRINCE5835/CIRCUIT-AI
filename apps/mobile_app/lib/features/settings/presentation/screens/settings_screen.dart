import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/breadboard_shared.dart';
import '../../../../core/services/api_service.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
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
      await ApiService.updateProfile({'display_name': name});
      await ref.read(authProvider.notifier).fetchProfile();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Name updated')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to update name')),
        );
      }
    }
    if (mounted) setState(() => _isSaving = false);
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
      await ApiService.deleteAccount();
      await ref.read(authProvider.notifier).logout();
      if (mounted) context.go(RoutePaths.splash);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to delete account')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final currentTheme = ref.watch(themeModeProvider);
    final locale = ref.watch(localeProvider);
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final email = user?['email'] as String? ?? '';

    final isDark = currentTheme == ThemeMode.dark ||
        (currentTheme == ThemeMode.system &&
            MediaQuery.of(context).platformBrightness == Brightness.dark);

    if (user != null && _nameController.text.isEmpty) {
      _nameController.text = user['display_name'] as String? ?? user['username'] as String? ?? '';
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        padding: const EdgeInsets.all(DSDimensions.s16),
        children: [
          Text('Profile', style: theme.textTheme.titleSmall?.copyWith(
            color: theme.colorScheme.primary,
          )),
          const SizedBox(height: DSDimensions.s8),
          AppCard(
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.person_outline),
                  title: const Text('Full Name'),
                  subtitle: TextField(
                    controller: _nameController,
                    decoration: const InputDecoration(
                      border: InputBorder.none,
                      isDense: true,
                      hintText: 'Enter your name',
                    ),
                  ),
                  trailing: _isSaving
                      ? const SizedBox(width: 24, height: 24, child: CircularProgressIndicator(strokeWidth: 2))
                      : IconButton(
                          icon: const Icon(Icons.save_outlined),
                          onPressed: _updateName,
                        ),
                ),
                const Divider(height: 1),
                ListTile(
                  leading: const Icon(Icons.email_outlined),
                  title: const Text('Email'),
                  subtitle: Text(email, style: TextStyle(color: theme.colorScheme.onSurface.withValues(alpha: 0.5))),
                ),
              ],
            ),
          ),
          const SizedBox(height: DSDimensions.s24),
          Text('Appearance', style: theme.textTheme.titleSmall?.copyWith(
            color: theme.colorScheme.primary,
          )),
          const SizedBox(height: DSDimensions.s8),
          AppCard(
            child: SwitchListTile(
              title: const Text('Dark Mode'),
              subtitle: const Text('Toggle dark theme'),
              value: isDark,
              onChanged: (_) {
                ref.read(themeModeProvider.notifier).setThemeMode(
                  isDark ? ThemeMode.light : ThemeMode.dark,
                );
              },
            ),
          ),
          AppCard(
            child: ListTile(
              title: const Text('Language'),
              subtitle: Text(_localeName(locale.languageCode)),
              trailing: const Icon(Icons.chevron_right),
              onTap: () => _showLanguagePicker(context, ref),
            ),
          ),
          const SizedBox(height: DSDimensions.s24),
          Text('Support', style: theme.textTheme.titleSmall?.copyWith(
            color: theme.colorScheme.primary,
          )),
          const SizedBox(height: DSDimensions.s8),
          AppCard(
            child: Column(
              children: [
                ListTile(
                  leading: const Icon(Icons.mail_outline),
                  title: const Text('Email'),
                  subtitle: const Text('support@breadboard.ai'),
                ),
                const Divider(height: 1),
                ListTile(
                  leading: const Icon(Icons.phone_outlined),
                  title: const Text('Phone'),
                  subtitle: const Text('+91-1800-123-4567'),
                ),
              ],
            ),
          ),
          const SizedBox(height: DSDimensions.s24),
          Text('Danger Zone', style: theme.textTheme.titleSmall?.copyWith(
            color: DSColors.danger,
          )),
          const SizedBox(height: DSDimensions.s8),
          AppCard(
            child: ListTile(
              leading: const Icon(Icons.delete_forever, color: DSColors.danger),
              title: const Text('Delete Account', style: TextStyle(color: DSColors.danger)),
              subtitle: const Text('Permanently delete your account and data'),
              trailing: const Icon(Icons.chevron_right),
              onTap: _deleteAccount,
            ),
          ),
          const SizedBox(height: DSDimensions.s24),
          Text('About', style: theme.textTheme.titleSmall?.copyWith(
            color: theme.colorScheme.primary,
          )),
          const SizedBox(height: DSDimensions.s8),
          AppCard(
            child: Column(
              children: [
                ListTile(title: const Text('Version'), trailing: const Text('1.0.0')),
                const Divider(height: 1),
                ListTile(title: const Text('Terms of Service'), trailing: const Icon(Icons.chevron_right)),
                const Divider(height: 1),
                ListTile(title: const Text('Privacy Policy'), trailing: const Icon(Icons.chevron_right)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _localeName(String code) {
    switch (code) {
      case 'hi': return 'हिन्दी';
      case 'raj': return 'राजस्थानी';
      default: return 'English';
    }
  }

  void _showLanguagePicker(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(DSDimensions.sheetRadius)),
      ),
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const SizedBox(height: DSDimensions.s8),
            Container(
              width: DSDimensions.sheetHandleWidth,
              height: 4,
              decoration: BoxDecoration(
                color: Colors.grey.shade300,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
            const SizedBox(height: DSDimensions.s16),
            Text('Select Language', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: DSDimensions.s8),
            ListTile(
              leading: const Icon(Icons.check),
              title: const Text('English'),
              onTap: () { ref.read(localeProvider.notifier).setLocale('en'); Navigator.pop(context); },
            ),
            ListTile(
              leading: const Icon(Icons.check),
              title: const Text('हिन्दी'),
              onTap: () { ref.read(localeProvider.notifier).setLocale('hi'); Navigator.pop(context); },
            ),
            ListTile(
              leading: const Icon(Icons.check),
              title: const Text('राजस्थानी'),
              onTap: () { ref.read(localeProvider.notifier).setLocale('raj'); Navigator.pop(context); },
            ),
            const SizedBox(height: DSDimensions.s16),
          ],
        ),
      ),
    );
  }
}
