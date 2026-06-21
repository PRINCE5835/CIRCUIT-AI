import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:breadboard_mobile/app.dart';

void main() {
  testWidgets('App builds successfully', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: BreadBoardApp()));
    await tester.pumpAndSettle(const Duration(seconds: 10));
    expect(find.byType(ProviderScope), findsOneWidget);
  });
}
