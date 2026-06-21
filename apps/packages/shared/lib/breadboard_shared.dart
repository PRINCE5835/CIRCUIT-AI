/// BreadBoard AI - Shared Design System & Core Library.
///
/// Contains the electronic-themed design tokens, reusable widgets,
/// routing, localization, networking, and core infrastructure
/// shared across all BreadBoard apps (mobile, web, admin, teacher).
library breadboard_shared;

export 'core/router/route_names.dart';
export 'core/router/route_paths.dart';
export 'core/theme/app_theme.dart';
export 'core/theme/theme_provider.dart';
export 'core/localization/app_localizations.dart';
export 'core/localization/locale_provider.dart';
export 'core/di/providers.dart';
export 'core/di/auth_providers.dart';
export 'core/animations/animation_constants.dart';
export 'core/network/api_client.dart';
export 'core/network/api_endpoints.dart';
export 'core/security/auth_storage.dart';
export 'core/cache/local_storage.dart';
export 'core/errors/app_exceptions.dart';
export 'shared/design_system/colors.dart';
export 'shared/design_system/dimensions.dart';
export 'shared/design_system/typography.dart';
export 'shared/design_system/decorations.dart';
export 'shared/design_system/gradients.dart';
export 'shared/design_system/shadows.dart';

// Config & Utils
export 'core/config/app_config.dart';
export 'shared/utils/validators.dart';

// Utility Extensions
export 'core/extensions/context_extensions.dart';

// Shared Widgets
export 'shared/widgets/app_button.dart';
export 'shared/widgets/app_card.dart';
export 'shared/widgets/app_text_field.dart';
export 'shared/widgets/app_scaffold.dart';
export 'shared/widgets/error_display.dart';
export 'shared/widgets/loading_overlay.dart';
export 'shared/widgets/shimmer_loading.dart';
export 'shared/widgets/section_header.dart';
export 'shared/widgets/responsive_layout.dart';
export 'shared/widgets/buttons/neo_button.dart';
export 'shared/widgets/buttons/icon_button.dart';
export 'shared/widgets/buttons/segmented_button.dart';
export 'shared/widgets/cards/glass_glow_cards.dart';
export 'shared/widgets/cards/feature_cards.dart';
export 'shared/widgets/feedback/app_dialog.dart';
export 'shared/widgets/feedback/app_bottom_sheet.dart';
export 'shared/widgets/feedback/toast.dart';
export 'shared/widgets/inputs/neo_text_field.dart';
export 'shared/widgets/inputs/app_search_bar.dart';
export 'shared/widgets/inputs/app_components.dart';
export 'shared/widgets/layout/layout_widgets.dart';
export 'shared/widgets/loading/circuit_spinner.dart';
export 'shared/widgets/loading/skeleton_loader.dart';
export 'shared/widgets/states/state_widgets.dart';
