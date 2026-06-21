import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:cached_network_image/cached_network_image.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class FeatureCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color? iconColor;
  final Color? accentColor;
  final VoidCallback? onTap;
  final Widget? trailing;

  const FeatureCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
    this.iconColor,
    this.accentColor,
    this.onTap,
    this.trailing,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final col = accentColor ?? DSColors.circuitCyan;

    return Card(
      elevation: 0,
      color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        side: BorderSide(color: col.withValues(alpha: 0.2), width: 1),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        child: Padding(
          padding: const EdgeInsets.all(DSDimensions.cardPadding),
          child: Row(
            children: [
              Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(14),
                  color: col.withValues(alpha: 0.12),
                ),
                child: Icon(icon, color: col, size: 24),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(title, style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600)),
                    const SizedBox(height: 2),
                    Text(subtitle, style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                  ],
                ),
              ),
              if (trailing != null) ...[
                const SizedBox(width: 8),
                trailing!,
              ] else ...[
                Icon(Icons.chevron_right, color: theme.colorScheme.onSurfaceVariant, size: 20),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class MetricCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color? accentColor;
  final String? trend;
  final bool trendUp;

  const MetricCard({
    super.key,
    required this.label,
    required this.value,
    required this.icon,
    this.accentColor,
    this.trend,
    this.trendUp = true,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;
    final col = accentColor ?? DSColors.circuitCyan;

    return Container(
      padding: const EdgeInsets.all(DSDimensions.cardPadding),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
        border: Border.all(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Icon(icon, color: col, size: 20),
              if (trend != null)
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      trendUp ? Icons.trending_up : Icons.trending_down,
                      color: trendUp ? DSColors.safe : DSColors.danger,
                      size: 16,
                    ),
                    const SizedBox(width: 4),
                    Text(trend!, style: TextStyle(
                      fontSize: 12,
                      color: trendUp ? DSColors.safe : DSColors.danger,
                      fontWeight: FontWeight.w600,
                    )),
                  ],
                ),
            ],
          ),
          const SizedBox(height: 12),
          Text(value, style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w700)),
          const SizedBox(height: 4),
          Text(label, style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
        ],
      ),
    );
  }
}

class CircuitCard extends StatelessWidget {
  final String name;
  final String description;
  final String componentCount;
  final bool isVerified;
  final VoidCallback? onTap;

  const CircuitCard({
    super.key,
    required this.name,
    required this.description,
    required this.componentCount,
    this.isVerified = false,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Card(
      elevation: 0,
      color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        side: BorderSide(
          color: isVerified
              ? DSColors.circuitCyan.withValues(alpha: 0.3)
              : (isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
          width: isVerified ? 1.5 : 1,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        child: Padding(
          padding: const EdgeInsets.all(DSDimensions.cardPadding),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 40, height: 40,
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(10),
                      color: DSColors.circuitCyan.withValues(alpha: 0.1),
                    ),
                    child: Icon(Icons.circle_outlined, color: DSColors.circuitCyan, size: 20),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(name, style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
                        Text('$componentCount components', style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
                      ],
                    ),
                  ),
                  if (isVerified)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(6),
                        color: DSColors.safe.withValues(alpha: 0.1),
                      ),
                      child: const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.verified, size: 12, color: DSColors.safe),
                          SizedBox(width: 4),
                          Text('Verified', style: TextStyle(fontSize: 11, color: DSColors.safe, fontWeight: FontWeight.w600)),
                        ],
                      ),
                    ),
                ],
              ),
              const SizedBox(height: 12),
              Text(description, style: theme.textTheme.bodySmall, maxLines: 2, overflow: TextOverflow.ellipsis),
            ],
          ),
        ),
      ),
    );
  }
}

class ComponentCard extends StatelessWidget {
  final String name;
  final String category;
  final String specification;
  final double? price;
  final String? imageUrl;
  final Color categoryColor;
  final VoidCallback? onTap;

  const ComponentCard({
    super.key,
    required this.name,
    required this.category,
    required this.specification,
    this.price,
    this.imageUrl,
    this.categoryColor = DSColors.neonViolet,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Card(
      elevation: 0,
      color: isDark ? DSColors.surfaceDarkCard : DSColors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        side: BorderSide(color: isDark ? DSColors.white.withValues(alpha: 0.06) : DSColors.black.withValues(alpha: 0.06)),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        child: Padding(
          padding: const EdgeInsets.all(DSDimensions.cardPadding),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                width: 48, height: 48,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  color: categoryColor.withValues(alpha: 0.12),
                ),
                child: imageUrl != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(12),
                        child: CachedNetworkImage(
                          imageUrl: imageUrl!,
                          width: 48, height: 48,
                          fit: BoxFit.cover,
                          placeholder: (_, __) => Icon(Icons.memory, color: categoryColor, size: 24),
                          errorWidget: (_, __, ___) => Icon(Icons.memory, color: categoryColor, size: 24),
                        ),
                      )
                    : Icon(Icons.memory, color: categoryColor, size: 24),
              ),
              const SizedBox(height: 12),
              Text(name, style: theme.textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600)),
              const SizedBox(height: 2),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(4),
                  color: categoryColor.withValues(alpha: 0.1),
                ),
                child: Text(category, style: TextStyle(fontSize: 11, color: categoryColor, fontWeight: FontWeight.w500)),
              ),
              const SizedBox(height: 8),
              Text(specification, style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
              if (price != null) ...[
                const Spacer(),
                Text('₹${price!.toStringAsFixed(2)}', style: theme.textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w700, color: DSColors.circuitCyan)),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
