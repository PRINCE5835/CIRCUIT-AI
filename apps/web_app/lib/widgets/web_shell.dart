import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:file_picker/file_picker.dart';
import 'package:dio/dio.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class WebShell extends ConsumerStatefulWidget {
  final Widget child;
  const WebShell({super.key, required this.child});

  @override
  ConsumerState<WebShell> createState() => _WebShellState();
}

class _WebShellState extends ConsumerState<WebShell> {
  Future<void> _scanComponent() async {
    try {
      final result = await FilePicker.platform.pickFiles(type: FileType.image);
      if (result == null || result.files.isEmpty) return;

      final file = result.files.first;
      if (file.path == null && file.bytes == null) return;

      if (!mounted) return;
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (_) => const Center(child: CircuitSpinner(size: 48)),
      );

      final formData = FormData.fromMap({
        'file': file.bytes != null
            ? MultipartFile.fromBytes(file.bytes!, filename: file.name)
            : await MultipartFile.fromFile(file.path!, filename: file.name),
      });
      final response = await ApiClient.instance.dio.post(
        ApiEndpoints.aiVisionDetect,
        data: formData,
      );

      if (mounted) Navigator.of(context).pop();
      final resultData = response.data;
      final components = resultData['components'] as List<dynamic>? ?? [resultData];

      if (!mounted) return;
      _showResults(components);
    } catch (e) {
      if (mounted) {
        Navigator.of(context).pop();
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Scan failed: ${e.toString()}')),
        );
      }
    }
  }

  void _showResults(List<dynamic> components) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Detected Components'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: components.map((c) {
            final cMap = c as Map<String, dynamic>;
            final name = cMap['name'] as String? ?? 'Unknown';
            final confidence = cMap['confidence'] as num?;
            return ListTile(
              leading: const Icon(Icons.memory, color: DSColors.circuitCyan),
              title: Text(name),
              subtitle: confidence != null
                  ? Text('${(confidence * 100).toStringAsFixed(0)}% confidence')
                  : null,
              dense: true,
            );
          }).toList(),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('OK')),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isWide = MediaQuery.of(context).size.width >= 900;
    return Scaffold(
      body: Row(
        children: [
          if (isWide) _Sidebar(onScan: _scanComponent),
          Expanded(child: widget.child),
        ],
      ),
      bottomNavigationBar: isWide ? null : _BottomNav(onScan: _scanComponent),
    );
  }
}

class _Sidebar extends ConsumerWidget {
  final VoidCallback onScan;
  const _Sidebar({required this.onScan});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final location = GoRouterState.of(context).uri.path;
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final allItems = [..._navItems, _NavItem('Scan', Icons.qr_code_scanner, '/scan')];

    return Container(
      width: 220,
      decoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkElevated : DSColors.white,
        border: Border(
          right: BorderSide(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
        ),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(vertical: DSDimensions.s20, horizontal: DSDimensions.s16),
            child: Row(
              children: [
                Container(
                  width: 32, height: 32,
                  decoration: BoxDecoration(
                    gradient: DSGradients.primaryGradient,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(Icons.circle_outlined, color: Colors.white, size: 18),
                ),
                const SizedBox(width: 10),
                Text('BreadBoard', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700)),
              ],
            ),
          ),
          const Divider(height: 1),
          const SizedBox(height: 8),
          ...allItems.map((item) {
            if (item.route == '/scan') {
              return _SidebarActionButton(
                icon: item.icon,
                label: item.label,
                onTap: onScan,
              );
            }
            return _NavItemWidget(item: item, isSelected: location == item.route);
          }),
          const Spacer(),
          if (authState.isAuthenticated) ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 14,
                    backgroundColor: DSColors.primary.withValues(alpha: 0.2),
                    child: Text(
                      (user?['display_name'] as String? ?? user?['username'] as String? ?? 'U')[0].toUpperCase(),
                      style: TextStyle(fontSize: 12, color: DSColors.primary, fontWeight: FontWeight.w600),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      user?['display_name'] as String? ?? user?['username'] as String? ?? 'User',
                      style: TextStyle(fontSize: 13, color: isDark ? DSColors.grey300 : DSColors.grey700),
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: InkWell(
                borderRadius: BorderRadius.circular(12),
                onTap: () async {
                  await ref.read(authProvider.notifier).logout();
                  if (context.mounted) context.go(RoutePaths.login);
                },
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      Icon(Icons.logout, size: 18, color: DSColors.grey500),
                      const SizedBox(width: 12),
                      Text('Logout', style: TextStyle(fontSize: 13, color: DSColors.grey500)),
                    ],
                  ),
                ),
              ),
            ),
          ] else ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: _SidebarActionButton(
                icon: Icons.login,
                label: 'Login',
                onTap: () => context.go(RoutePaths.login),
              ),
            ),
          ],
          _ThemeToggle(),
          const SizedBox(height: 8),
        ],
      ),
    );
  }
}

class _SidebarActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;
  const _SidebarActionButton({required this.icon, required this.label, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return InkWell(
      borderRadius: BorderRadius.circular(12),
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            Icon(icon, size: 18, color: isDark ? DSColors.grey400 : DSColors.grey600),
            const SizedBox(width: 12),
            Text(label, style: TextStyle(fontSize: 13, color: isDark ? DSColors.grey400 : DSColors.grey600)),
          ],
        ),
      ),
    );
  }
}

class _NavItemWidget extends StatelessWidget {
  final _NavItem item;
  final bool isSelected;
  const _NavItemWidget({required this.item, required this.isSelected});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
      child: Material(
        color: isSelected
            ? DSColors.primary.withValues(alpha: 0.12)
            : Colors.transparent,
        borderRadius: BorderRadius.circular(12),
        child: InkWell(
          borderRadius: BorderRadius.circular(12),
          onTap: () => context.go(item.route),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
            child: Row(
              children: [
                Icon(item.icon, size: 20, color: isSelected ? DSColors.primary : (isDark ? DSColors.grey300 : DSColors.grey600)),
                const SizedBox(width: 12),
                Text(item.label, style: TextStyle(
                  fontSize: 14,
                  fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                  color: isSelected ? DSColors.primary : (isDark ? DSColors.grey300 : DSColors.grey600),
                )),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _BottomNav extends StatelessWidget {
  final VoidCallback onScan;
  const _BottomNav({required this.onScan});

  @override
  Widget build(BuildContext context) {
    final location = GoRouterState.of(context).uri.path;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final allItems = [
      _navItems[0], _navItems[1],
      _NavItem('Scan', Icons.qr_code_scanner, '/scan'),
      _navItems[2], _navItems[3],
    ];
    return Container(
      decoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkElevated : DSColors.white,
        border: Border(top: BorderSide(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06))),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 4),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: allItems.map((item) {
              if (item.route == '/scan') {
                return Expanded(
                  child: InkWell(
                    onTap: onScan,
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 6),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 44, height: 44,
                            decoration: BoxDecoration(
                              gradient: DSGradients.primaryGradient,
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.qr_code_scanner, color: Colors.white, size: 22),
                          ),
                          const SizedBox(height: 2),
                          Text('Scan', style: TextStyle(fontSize: 10, fontWeight: FontWeight.w600, color: DSColors.primary)),
                        ],
                      ),
                    ),
                  ),
                );
              }
              final sel = location == item.route;
              return Expanded(
                child: InkWell(
                  onTap: () => context.go(item.route),
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 6),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(item.icon, size: 22, color: sel ? DSColors.primary : (isDark ? DSColors.grey400 : DSColors.grey500)),
                        const SizedBox(height: 2),
                        Text(item.label, style: TextStyle(fontSize: 10, fontWeight: sel ? FontWeight.w600 : FontWeight.w400, color: sel ? DSColors.primary : (isDark ? DSColors.grey400 : DSColors.grey500))),
                      ],
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}

class _ThemeToggle extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8),
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () => ref.read(themeModeProvider.notifier).toggle(),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Row(
            children: [
              Icon(isDark ? Icons.light_mode_outlined : Icons.dark_mode_outlined, size: 20),
              const SizedBox(width: 12),
              Text(isDark ? 'Light Mode' : 'Dark Mode', style: const TextStyle(fontSize: 14)),
            ],
          ),
        ),
      ),
    );
  }
}

class _NavItem {
  final String label;
  final IconData icon;
  final String route;
  const _NavItem(this.label, this.icon, this.route);
}

final List<_NavItem> _navItems = const [
  _NavItem('Home', Icons.dashboard_outlined, '/home'),
  _NavItem('Voice AI', Icons.mic_outlined, '/voice'),
  _NavItem('Circuit', Icons.circle_outlined, '/circuit-generation'),
  _NavItem('Market', Icons.store_outlined, '/marketplace'),
  _NavItem('Profile', Icons.person_outlined, '/profile'),
];
