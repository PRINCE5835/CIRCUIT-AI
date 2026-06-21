import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/shared/design_system/colors.dart';
import 'package:breadboard_shared/shared/design_system/gradients.dart';
import 'package:breadboard_shared/shared/widgets/cards/feature_cards.dart';
import 'package:breadboard_shared/shared/widgets/cards/glass_glow_cards.dart';
import 'package:breadboard_shared/shared/widgets/section_header.dart';
import 'package:breadboard_shared/core/router/route_paths.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final isWide = MediaQuery.of(context).size.width >= 900;
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: isWide ? 280 : 200,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Container(
                decoration: BoxDecoration(
                  gradient: isDark
                      ? LinearGradient(colors: [DSColors.surfaceDark, DSColors.surfaceDarkHigh.withValues(alpha: 0.5), DSColors.surfaceDark])
                      : LinearGradient(colors: [DSColors.surfaceLight, DSColors.white, DSColors.surfaceLight]),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    Container(
                      padding: EdgeInsets.symmetric(horizontal: isWide ? 48 : 20, vertical: 24),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('Welcome to BreadBoard AI', style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w700)),
                          const SizedBox(height: 8),
                          Text('Your electronics learning & circuit assistant', style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: isDark ? DSColors.grey300 : DSColors.grey600)),
                          const SizedBox(height: 20),
                          _HeroSearchBar(isDark: isDark),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          SliverPadding(
            padding: EdgeInsets.fromLTRB(isWide ? 48 : 16, 24, isWide ? 48 : 16, 100),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                Text('Quick Actions', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600, color: DSColors.primary)),
                const SizedBox(height: 16),
                _QuickActionsGrid(isWide: isWide, isDark: isDark),
                const SizedBox(height: 32),
                SectionHeader(title: 'Recent Projects', actionLabel: 'View All'),
                const SizedBox(height: 16),
                _RecentProjects(isDark: isDark),
                const SizedBox(height: 32),
                SectionHeader(title: 'Learn Electronics'),
                const SizedBox(height: 16),
                _LearnTopics(isDark: isDark, isWide: isWide),
              ]),
            ),
          ),
        ],
      ),
    );
  }
}

class _HeroSearchBar extends StatelessWidget {
  final bool isDark;
  const _HeroSearchBar({required this.isDark});

  @override
  Widget build(BuildContext context) {
    return Container(
      constraints: const BoxConstraints(maxWidth: 500),
      child: TextField(
        style: TextStyle(color: isDark ? DSColors.white : DSColors.grey900),
        decoration: InputDecoration(
          hintText: 'Ask me anything about electronics...',
          hintStyle: TextStyle(color: isDark ? DSColors.grey400 : DSColors.grey500),
          prefixIcon: Icon(Icons.search, color: DSColors.primary),
          suffixIcon: Container(
            margin: const EdgeInsets.all(4),
            decoration: BoxDecoration(
              gradient: DSGradients.primaryGradient,
              borderRadius: BorderRadius.circular(10),
            ),
            child: IconButton(
              icon: const Icon(Icons.mic, color: Colors.white, size: 20),
              onPressed: () => context.push(RoutePaths.voice),
            ),
          ),
          filled: true,
          fillColor: isDark ? DSColors.surfaceDarkCard : DSColors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide(color: DSColors.primary.withValues(alpha: 0.3)),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide(color: DSColors.primary.withValues(alpha: 0.2)),
          ),
        ),
      ),
    );
  }
}

class _QuickActionsGrid extends StatelessWidget {
  final bool isWide;
  final bool isDark;
  const _QuickActionsGrid({required this.isWide, required this.isDark});

  @override
  Widget build(BuildContext context) {
    final actions = [
      _ActionData('Generate Circuit', Icons.circle_outlined, DSColors.circuitCyan, RoutePaths.circuitGeneration),
      _ActionData('Voice Assistant', Icons.mic, DSColors.neonViolet, RoutePaths.voice),
      _ActionData('Learn Circuits', Icons.menu_book_outlined, DSColors.warmAmber, RoutePaths.circuitLearning),
      _ActionData('Repair Assistant', Icons.build_outlined, DSColors.neonCoral, RoutePaths.repairAssistant),
      _ActionData('Verify Layout', Icons.verified_outlined, DSColors.circuitCyan, RoutePaths.breadboardVerification),
      _ActionData('Shop Components', Icons.store_outlined, DSColors.neonGreen, RoutePaths.marketplace),
    ];
    return Wrap(
      spacing: 12,
      runSpacing: 12,
      children: actions.map((a) {
        return SizedBox(
          width: isWide ? 160 : (MediaQuery.of(context).size.width - 56) / 2,
          child: GlowCard(
            glowColor: a.color,
            onTap: () => context.push(a.route),
            child: Container(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: a.color.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Icon(a.icon, color: a.color, size: 22),
                  ),
                  const SizedBox(height: 12),
                  Text(a.label, style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13, color: isDark ? DSColors.white : DSColors.grey900)),
                ],
              ),
            ),
          ),
        );
      }).toList(),
    );
  }
}

class _RecentProjects extends StatelessWidget {
  final bool isDark;
  const _RecentProjects({required this.isDark});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 160,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: 4,
        itemBuilder: (_, i) {
          final projects = ['LED Blinker', '555 Timer', 'Voltage Divider', 'Motor Driver'];
          return Container(
            width: 200,
            margin: const EdgeInsets.only(right: 12),
            child: GlowCard(
              child: Container(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: DSColors.circuitCyan.withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Icon(Icons.circle_outlined, color: DSColors.circuitCyan, size: 20),
                    ),
                    const Spacer(),
                    Text(projects[i], style: TextStyle(fontWeight: FontWeight.w600, color: isDark ? DSColors.white : DSColors.grey900)),
                    const SizedBox(height: 4),
                    Text('Created 2 days ago', style: TextStyle(fontSize: 12, color: isDark ? DSColors.grey400 : DSColors.grey500)),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}

class _LearnTopics extends StatelessWidget {
  final bool isDark;
  final bool isWide;
  const _LearnTopics({required this.isDark, required this.isWide});

  @override
  Widget build(BuildContext context) {
    final topics = [
      _TopicData("Ohm's Law", 'Voltage, Current, Resistance', Icons.electric_bolt, DSColors.circuitCyan),
      _TopicData('LED Circuits', 'Light up LEDs with resistors', Icons.emoji_objects_outlined, DSColors.neonViolet),
      _TopicData('555 Timer', 'Master the classic timer IC', Icons.timer_outlined, DSColors.warmAmber),
      _TopicData('Transistors', 'Switching & amplification', Icons.memory, DSColors.neonGreen),
    ];
    return Wrap(
      spacing: 12,
      runSpacing: 12,
      children: topics.map((t) => SizedBox(
        width: isWide ? 240 : (MediaQuery.of(context).size.width - 56),
        child: FeatureCard(
          accentColor: t.color,
          title: t.title,
          subtitle: t.subtitle,
          icon: t.icon,
          onTap: () => context.push(RoutePaths.circuitLearning),
        ),
      )).toList(),
    );
  }
}

class _ActionData {
  final String label;
  final IconData icon;
  final Color color;
  final String route;
  const _ActionData(this.label, this.icon, this.color, this.route);
}

class _TopicData {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  const _TopicData(this.title, this.subtitle, this.icon, this.color);
}
