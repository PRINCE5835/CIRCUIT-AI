import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class OnboardingScreen extends ConsumerStatefulWidget {
  const OnboardingScreen({super.key});

  @override
  ConsumerState<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends ConsumerState<OnboardingScreen> {
  final _pageController = PageController();
  int _currentPage = 0;

  final _pages = const [
    _OnboardingPageData(
      icon: Icons.circle_outlined,
      title: 'Design Circuits',
      description: 'Create electronic circuits using natural voice commands. Just describe what you want to build.',
    ),
    _OnboardingPageData(
      icon: Icons.troubleshoot_outlined,
      title: 'Learn & Repair',
      description: 'Understand how circuits work with interactive tutorials and get step-by-step repair guidance.',
    ),
    _OnboardingPageData(
      icon: Icons.verified_outlined,
      title: 'Verify & Share',
      description: 'Validate your breadboard layout with AI-powered camera verification and share with the community.',
    ),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _onNext() {
    if (_currentPage < _pages.length - 1) {
      _pageController.nextPage(duration: 300.ms, curve: Curves.easeInOut);
    } else {
      _complete();
    }
  }

  void _complete() {
    ref.read(authStateProvider.notifier).state = true;
    context.go(RoutePaths.login);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Column(
          children: [
            Align(
              alignment: Alignment.topRight,
              child: TextButton(
                onPressed: _complete,
                child: Text(AppLocalizations.of(context).skip),
              ),
            ),
            Expanded(
              child: PageView.builder(
                controller: _pageController,
                onPageChanged: (i) => setState(() => _currentPage = i),
                itemCount: _pages.length,
                itemBuilder: (context, index) {
                  final page = _pages[index];
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: DSDimensions.s32),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(page.icon, size: 120, color: DSColors.primary)
                            .animate()
                            .fadeIn(duration: 500.ms)
                            .scale(delay: 200.ms),
                        const SizedBox(height: DSDimensions.s40),
                        Text(
                          page.title,
                          style: theme.textTheme.headlineMedium,
                          textAlign: TextAlign.center,
                        ).animate().fadeIn(duration: 500.ms, delay: 300.ms).slideY(begin: 0.2),
                        const SizedBox(height: DSDimensions.s16),
                        Text(
                          page.description,
                          style: theme.textTheme.bodyLarge?.copyWith(
                            color: theme.colorScheme.onSurface.withValues(alpha: 0.7),
                          ),
                          textAlign: TextAlign.center,
                        ).animate().fadeIn(duration: 500.ms, delay: 500.ms).slideY(begin: 0.2),
                      ],
                    ),
                  );
                },
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(_pages.length, (i) => _PageIndicator(isActive: i == _currentPage)),
            ),
            const SizedBox(height: DSDimensions.s32),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: DSDimensions.s24),
              child: AppButton(
                label: _currentPage == _pages.length - 1
                    ? AppLocalizations.of(context).getStarted
                    : AppLocalizations.of(context).next,
                isFullWidth: true,
                onPressed: _onNext,
              ),
            ),
            const SizedBox(height: DSDimensions.s48),
          ],
        ),
      ),
    );
  }
}

class _OnboardingPageData {
  final IconData icon;
  final String title;
  final String description;
  const _OnboardingPageData({
    required this.icon,
    required this.title,
    required this.description,
  });
}

class _PageIndicator extends StatelessWidget {
  final bool isActive;
  const _PageIndicator({required this.isActive});

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: 300.ms,
      margin: const EdgeInsets.symmetric(horizontal: 4),
      width: isActive ? 24 : 8,
      height: 8,
      decoration: BoxDecoration(
        color: isActive ? DSColors.primary : DSColors.grey300,
        borderRadius: BorderRadius.circular(4),
      ),
    );
  }
}
