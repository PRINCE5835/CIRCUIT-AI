import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/widgets/empty_state.dart';

Widget wrapApp(Widget child) {
  return MaterialApp(home: Scaffold(body: child));
}

void main() {
  testWidgets('shows title and icon', (tester) async {
    await tester.pumpWidget(wrapApp(
      const EmptyState(icon: Icons.search, title: 'Nothing here'),
    ));
    expect(find.text('Nothing here'), findsOneWidget);
    expect(find.byIcon(Icons.search), findsOneWidget);
  });

  testWidgets('shows subtitle when provided', (tester) async {
    await tester.pumpWidget(wrapApp(
      const EmptyState(
        icon: Icons.inventory_2_outlined,
        title: 'No items',
        subtitle: 'Try again later',
      ),
    ));
    expect(find.text('No items'), findsOneWidget);
    expect(find.text('Try again later'), findsOneWidget);
  });

  testWidgets('does not show subtitle when null', (tester) async {
    await tester.pumpWidget(wrapApp(
      const EmptyState(icon: Icons.info, title: 'Info'),
    ));
    expect(find.text('Info'), findsOneWidget);
    expect(find.textContaining('Try'), findsNothing);
  });
}
