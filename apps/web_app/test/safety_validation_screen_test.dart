import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/screens/safety_validation_screen.dart';
import 'test_helpers.dart';

void main() {
  testWidgets('renders title and description field', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const SafetyValidationScreen()));
    await tester.pump();

    expect(find.text('Safety Check'), findsOneWidget);
    expect(find.text('Run Safety Check'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
  });

  testWidgets('shows validating state on button press', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const SafetyValidationScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'Circuit with resistor and LED');
    await tester.tap(find.text('Run Safety Check'));
    await tester.pump();

    expect(find.text('Validating...'), findsOneWidget);
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    await tester.pumpAndSettle(const Duration(seconds: 5));
  });

  testWidgets('button disabled while validating', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const SafetyValidationScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'Test circuit');
    await tester.tap(find.text('Run Safety Check'));
    await tester.pump();

    final button = tester.widget<FilledButton>(find.byType(FilledButton));
    expect(button.onPressed, isNull);

    await tester.pumpAndSettle(const Duration(seconds: 5));
  });

  testWidgets('does not validate with empty input', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const SafetyValidationScreen()));
    await tester.pump();

    await tester.tap(find.text('Run Safety Check'));
    await tester.pump();

    expect(find.text('Validating...'), findsNothing);
  });

  testWidgets('returns to idle after validation completes', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const SafetyValidationScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'Circuit description');
    await tester.tap(find.text('Run Safety Check'));
    await tester.pump();

    expect(find.text('Validating...'), findsOneWidget);

    await tester.pumpAndSettle(const Duration(seconds: 5));

    expect(find.text('Run Safety Check'), findsOneWidget);
  });
}
