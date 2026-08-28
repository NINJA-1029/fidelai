import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fidel_app/features/simulation/simulation_screen.dart';

void main() {
  group('What-If Simulation Calculator Screen (HW-006) Tests', () {
    testWidgets('Renders SimulationScreen with shock input, calculate button, and impact card',
        (WidgetTester tester) async {
      tester.view.physicalSize = const Size(800, 1200);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);

      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: SimulationScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Screen Header and Engine Badge
      expect(find.text('WHAT-IF SIMULATION'), findsOneWidget);
      expect(find.text('SCENARIO ENGINE'), findsOneWidget);

      // Shock Parameter Card
      expect(find.text('SIMULATE UNEXPECTED EXPENSE'), findsOneWidget);
      expect(find.text('EXPENSE OUTFLOW AMOUNT (INR)'), findsOneWidget);
      expect(find.text('12000'), findsOneWidget);
      expect(find.text('CALCULATE TRAJECTORY'), findsOneWidget);

      // Projected Impact Card & Violation Badge
      expect(find.text('PROJECTED IMPACT ON TRAJECTORY'), findsOneWidget);
      expect(find.text('LIQUIDITY COMPARISON'), findsOneWidget);
      expect(find.text('BUFFER VIOLATION'), findsOneWidget);
      expect(find.text('BASELINE (30-DAY)'), findsOneWidget);
      expect(find.text('INR 31,400'), findsOneWidget);
      expect(find.text('SIMULATED (POST-SHOCK)'), findsOneWidget);
      expect(find.text('INR 19,400'), findsOneWidget);

      // Goal Cascade and Action
      expect(find.text('GOAL CASCADE IMPACT'), findsOneWidget);
      expect(find.text('ACTION: '), findsOneWidget);
    });

    testWidgets('Recalculating with small shock preserves buffer without violation',
        (WidgetTester tester) async {
      tester.view.physicalSize = const Size(800, 1200);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);

      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: SimulationScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Enter small shock amount: 2000
      await tester.enterText(find.byType(TextField), '2000');
      await tester.pumpAndSettle();

      // Tap CALCULATE TRAJECTORY
      await tester.tap(find.text('CALCULATE TRAJECTORY'));
      await tester.pumpAndSettle();

      // Verify BUFFER PRESERVED is rendered
      expect(find.text('BUFFER PRESERVED'), findsOneWidget);
      expect(find.text('INR 29,400'), findsOneWidget);
    });
  });
}
