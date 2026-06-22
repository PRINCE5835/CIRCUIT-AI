import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'camera_dialog.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

final globalSearchProvider = StateProvider<String>((ref) => '');

class WebShell extends ConsumerStatefulWidget {
  final Widget child;
  const WebShell({super.key, required this.child});

  @override
  ConsumerState<WebShell> createState() => _WebShellState();
}

class _WebShellState extends ConsumerState<WebShell> {
  Future<void> _scanComponent() async {
    await showDialog(context: context, builder: (_) => const CameraDialog());
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

class _Sidebar extends ConsumerStatefulWidget {
  final VoidCallback onScan;
  const _Sidebar({required this.onScan});

  @override
  ConsumerState<_Sidebar> createState() => _SidebarState();
}

class _SidebarState extends ConsumerState<_Sidebar> {
  final _searchController = TextEditingController();
  List<Map<String, dynamic>> _searchResults = [];
  bool _showResults = false;

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  Future<void> _onSearch(String query) async {
    if (query.trim().isEmpty) {
      setState(() { _searchResults = []; _showResults = false; });
      return;
    }
    try {
      final results = <Map<String, dynamic>>[];
      try {
        final compResp = await ApiClient.instance.dio.get(
          '${ApiEndpoints.components}?query=${Uri.encodeComponent(query)}&limit=5',
        );
        final items = (compResp.data['items'] as List?)?.cast<Map<String, dynamic>>() ?? [];
        for (final item in items) {
          results.add({
            'type': 'component',
            'label': item['name'] ?? '',
            'subtitle': item['category'] ?? '',
            'route': RoutePaths.componentCatalog,
            'data': item,
          });
        }
      } catch (_) {}
      try {
        final projResp = await ApiClient.instance.dio.get(
          '${ApiEndpoints.projects}?q=${Uri.encodeComponent(query)}&limit=3',
        );
        final items = (projResp.data['items'] as List?)?.cast<Map<String, dynamic>>() ?? [];
        for (final item in items) {
          results.add({
            'type': 'project',
            'label': item['title'] ?? '',
            'subtitle': item['status'] ?? '',
            'route': RoutePaths.projectHistory,
            'data': item,
          });
        }
      } catch (_) {}
      if (mounted) {
        setState(() { _searchResults = results; _showResults = true; });
      }
    } catch (e) {
      if (mounted) setState(() { _searchResults = []; _showResults = false; });
    }
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final location = GoRouterState.of(context).uri.path;
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final allItems = [..._navItems, _NavItem('Scan', Icons.qr_code_scanner, '/scan')];

    return Container(
      width: 240,
      decoration: BoxDecoration(
        color: isDark ? DSColors.surfaceDarkElevated : DSColors.white,
        border: Border(
          right: BorderSide(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
        ),
      ),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 16),
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
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
            child: Semantics(
              label: 'Global search',
              child: TextField(
                controller: _searchController,
                onChanged: _onSearch,
                style: TextStyle(fontSize: 13, color: isDark ? DSColors.white : DSColors.grey900),
                decoration: InputDecoration(
                  hintText: 'Search...',
                  hintStyle: TextStyle(fontSize: 13, color: isDark ? DSColors.grey500 : DSColors.grey400),
                  prefixIcon: Icon(Icons.search, size: 16, color: isDark ? DSColors.grey400 : DSColors.grey500),
                  suffixIcon: _searchController.text.isNotEmpty
                      ? IconButton(
                          icon: const Icon(Icons.clear, size: 16),
                          onPressed: () {
                            _searchController.clear();
                            setState(() { _searchResults = []; _showResults = false; });
                          },
                        )
                      : null,
                  filled: true,
                  fillColor: isDark ? DSColors.surfaceDarkVariant : DSColors.grey50,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: BorderSide.none,
                  ),
                  contentPadding: const EdgeInsets.symmetric(vertical: 8, horizontal: 12),
                  isDense: true,
                ),
              ),
            ),
          ),
          if (_showResults && _searchResults.isNotEmpty)
            Container(
              constraints: const BoxConstraints(maxHeight: 200),
              margin: const EdgeInsets.symmetric(horizontal: 12),
              decoration: BoxDecoration(
                color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
                borderRadius: BorderRadius.circular(8),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.15),
                    blurRadius: 8,
                  ),
                ],
              ),
              child: ListView.builder(
                shrinkWrap: true,
                itemCount: _searchResults.length,
                itemBuilder: (_, i) {
                  final r = _searchResults[i];
                  return ListTile(
                    dense: true,
                    leading: Icon(
                      r['type'] == 'component' ? Icons.inventory_2_outlined : Icons.folder_outlined,
                      size: 16,
                      color: DSColors.primary,
                    ),
                    title: Text(r['label'] as String? ?? '', style: const TextStyle(fontSize: 12)),
                    subtitle: r['subtitle'] != null ? Text(r['subtitle'] as String, style: const TextStyle(fontSize: 10)) : null,
                    onTap: () {
                      _searchController.clear();
                      setState(() { _searchResults = []; _showResults = false; });
                      context.go(r['route'] as String);
                    },
                  );
                },
              ),
            ),
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(vertical: 4),
              children: [
                ...allItems.map((item) {
                  if (item.route == '/scan') {
                    return _SidebarActionButton(
                      icon: item.icon,
                      label: item.label,
                      onTap: widget.onScan,
                    );
                  }
                  return _NavItemWidget(item: item, isSelected: location == item.route);
                }),
              ],
            ),
          ),
          if (authState.isAuthenticated) ...[
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              child: Semantics(
                label: 'User profile',
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
    return Semantics(
      label: label,
      button: true,
      child: InkWell(
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
    return Semantics(
      label: item.label,
      selected: isSelected,
      button: true,
      child: Padding(
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
      _navItems[2], _navItems[11],
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
                  child: Semantics(
                    label: 'Scan component',
                    button: true,
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
                  ),
                );
              }
              final sel = location == item.route;
              return Expanded(
                child: Semantics(
                  label: item.label,
                  selected: sel,
                  button: true,
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
    return Semantics(
      label: 'Toggle theme',
      button: true,
      child: Padding(
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
  _NavItem('Circuit Gen', Icons.circle_outlined, '/circuit-generation'),
  _NavItem('Circuit Learn', Icons.school_outlined, '/circuit-learning'),
  _NavItem('Repair', Icons.build_outlined, '/repair-assistant'),
  _NavItem('Safety', Icons.shield_outlined, '/safety-validation'),
  _NavItem('Cost Estimator', Icons.monetization_on_outlined, '/cost-estimation'),
  _NavItem('Verification', Icons.camera_alt_outlined, '/breadboard-verification'),
  _NavItem('Components', Icons.inventory_2_outlined, '/components'),
  _NavItem('Projects', Icons.folder_outlined, '/project-history'),
  _NavItem('Market', Icons.store_outlined, '/marketplace'),
  _NavItem('Profile', Icons.person_outlined, '/profile'),
  _NavItem('Settings', Icons.settings_outlined, '/settings'),
];
