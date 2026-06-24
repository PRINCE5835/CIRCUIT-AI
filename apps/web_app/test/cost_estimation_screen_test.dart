import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_web/screens/cost_estimation_screen.dart';
import 'test_helpers.dart';

void main() {
  testWidgets('renders title and components list field', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const CostEstimationScreen()));
    await tester.pump();

    expect(find.text('Estimate Component Costs'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
    expect(find.text('Estimate Cost'), findsOneWidget);
  });

  testWidgets('shows estimating state on button press', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const CostEstimationScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'LED x10\nResistor x20');
    await tester.tap(find.text('Estimate Cost'));
    await tester.pump();

    expect(find.text('Estimating...'), findsOneWidget);
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    await tester.pumpAndSettle(const Duration(seconds: 5));
  });

  testWidgets('button is disabled while estimating', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const CostEstimationScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'LED x10');
    await tester.tap(find.text('Estimate Cost'));
    await tester.pump();

    final button = tester.widget<FilledButton>(find.byType(FilledButton));
    expect(button.onPressed, isNull);

    await tester.pumpAndSettle(const Duration(seconds: 5));
  });

  testWidgets('does not estimate with empty input', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const CostEstimationScreen()));
    await tester.pump();

    await tester.tap(find.text('Estimate Cost'));
    await tester.pump();

    expect(find.text('Estimating...'), findsNothing);
  });

  testWidgets('returns to idle after estimation completes', (tester) async {
    await tester.pumpWidget(wrapWithProviders(const CostEstimationScreen()));
    await tester.pump();

    await tester.enterText(find.byType(TextField), 'LED x10');
    await tester.tap(find.text('Estimate Cost'));
    await tester.pump();

    expect(find.text('Estimating...'), findsOneWidget);

    await tester.pumpAndSettle(const Duration(seconds: 5));

    expect(find.text('Estimate Cost'), findsOneWidget);
    expect(find.text('Estimating...'), findsNothing);
  });
}
