import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/screens/repair_assistant_screen.dart';
import 'test_helpers.dart';

void main() {
  testWidgets('renders title and description field', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const RepairAssistantScreen()));
    await tester.pump();

    expect(find.text('Describe the Issue'), findsOneWidget);
    expect(find.text('Analyze Issue'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
  });

  testWidgets('shows analyzing state on button press', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const RepairAssistantScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'My LED is not lighting up');
    await tester.tap(find.text('Analyze Issue'));
    await tester.pump();

    expect(find.text('Analyzing...'), findsOneWidget);
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    await tester.pumpAndSettle(const Duration(seconds: 5));
  });

  testWidgets('button disabled while analyzing', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const RepairAssistantScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'Circuit issue');
    await tester.tap(find.text('Analyze Issue'));
    await tester.pump();

    final button = tester.widget<FilledButton>(find.byType(FilledButton));
    expect(button.onPressed, isNull);

    await tester.pumpAndSettle(const Duration(seconds: 5));
  });

  testWidgets('does not analyze with empty input', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const RepairAssistantScreen()));
    await tester.pump();

    await tester.tap(find.text('Analyze Issue'));
    await tester.pump();

    expect(find.text('Analyzing...'), findsNothing);
  });

  testWidgets('returns to idle after analysis completes', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const RepairAssistantScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'Issue description');
    await tester.tap(find.text('Analyze Issue'));
    await tester.pump();

    expect(find.text('Analyzing...'), findsOneWidget);

    await tester.pumpAndSettle(const Duration(seconds: 5));

    expect(find.text('Analyze Issue'), findsOneWidget);
  });
}
