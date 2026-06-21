import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';
import '../../design_system/colors.dart';
import '../../design_system/dimensions.dart';

class SkeletonLoader extends StatelessWidget {
  final double width;
  final double height;
  final double borderRadius;

  const SkeletonLoader({
    super.key,
    this.width = double.infinity,
    this.height = 16,
    this.borderRadius = DSDimensions.r8,
  });

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Shimmer.fromColors(
      baseColor: isDark ? const Color(0xFF232B3F) : const Color(0xFFE0E0E0),
      highlightColor: isDark ? const Color(0xFF2A3347) : const Color(0xFFF5F5F5),
      child: Container(
        width: width,
        height: height,
        decoration: BoxDecoration(
          color: isDark ? const Color(0xFF232B3F) : const Color(0xFFE0E0E0),
          borderRadius: BorderRadius.circular(borderRadius),
        ),
      ),
    );
  }
}

class CardSkeleton extends StatelessWidget {
  final bool isDark;

  const CardSkeleton({super.key, this.isDark = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DSDimensions.cardPadding),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(DSDimensions.cardRadius),
        color: isDark ? DSColors.surfaceDarkCard : DSColors.surfaceLightCard,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const SkeletonLoader(width: 44, height: 44, borderRadius: 12),
              const SizedBox(width: 12),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SkeletonLoader(width: 140, height: 16),
                    SizedBox(height: 6),
                    SkeletonLoader(width: 90, height: 12),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const SkeletonLoader(height: 12),
          const SizedBox(height: 8),
          const SkeletonLoader(width: 200, height: 12),
          const SizedBox(height: 16),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: const [
              SkeletonLoader(width: 80, height: 36, borderRadius: 18),
              SkeletonLoader(width: 56, height: 36, borderRadius: 18),
            ],
          ),
        ],
      ),
    );
  }
}

class ListSkeleton extends StatelessWidget {
  final int itemCount;

  const ListSkeleton({super.key, this.itemCount = 5});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: List.generate(
        itemCount,
        (i) => Padding(
          padding: const EdgeInsets.only(bottom: DSDimensions.s12),
          child: Row(
            children: [
              const SkeletonLoader(width: 44, height: 44, borderRadius: 12),
              const SizedBox(width: 12),
              const Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    SkeletonLoader(width: 160, height: 14),
                    SizedBox(height: 6),
                    SkeletonLoader(height: 12),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class CircuitSkeleton extends StatelessWidget {
  const CircuitSkeleton({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const CardSkeleton(),
        const SizedBox(height: DSDimensions.s12),
        const CardSkeleton(),
        const SizedBox(height: DSDimensions.s12),
        const CardSkeleton(),
      ],
    );
  }
}
