import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

class ForgotPasswordScreen extends ConsumerStatefulWidget {
  const ForgotPasswordScreen({super.key});

  @override
  ConsumerState<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends ConsumerState<ForgotPasswordScreen> {
  final _emailController = TextEditingController();
  bool _sent = false;

  @override
  void dispose() {
    _emailController.dispose();
    super.dispose();
  }

  void _onSubmit() {
    setState(() => _sent = true);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Forgot Password')),
      body: Padding(
        padding: const EdgeInsets.all(DSDimensions.s24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const SizedBox(height: DSDimensions.s32),
            Icon(Icons.lock_reset, size: 80, color: DSColors.primary),
            const SizedBox(height: DSDimensions.s24),
            Text(
              'Reset your password',
              style: theme.textTheme.headlineSmall,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s8),
            Text(
              'Enter your email and we\'ll send you instructions',
              style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurface.withValues(alpha: 0.6)),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: DSDimensions.s32),
            if (!_sent) ...[
              AppTextField(
                label: 'Email',
                controller: _emailController,
                keyboardType: TextInputType.emailAddress,
                validator: Validators.email,
              ),
              const SizedBox(height: DSDimensions.s24),
              AppButton(
                label: 'Send Reset Link',
                isFullWidth: true,
                onPressed: _onSubmit,
              ),
            ] else ...[
              const Icon(Icons.check_circle, size: 64, color: DSColors.safe),
              const SizedBox(height: DSDimensions.s16),
              Text(
                'Check your email',
                style: theme.textTheme.titleLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: DSDimensions.s24),
              AppButton(
                label: 'Back to Login',
                isFullWidth: true,
                onPressed: () => context.go(RoutePaths.login),
              ),
            ],
            const SizedBox(height: DSDimensions.s16),
            TextButton(
              onPressed: () => context.go(RoutePaths.login),
              child: const Text('Back to Login'),
            ),
          ],
        ),
      ),
    );
  }
}
