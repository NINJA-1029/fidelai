import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fidel_app/features/goals/goals_screen.dart';

void main() {
  group('Goals & Pacing Visualizer Screen (HW-005) Tests', () {
    testWidgets('Renders GoalsScreen with header, aggregate banner, and active goal cards',
        (WidgetTester tester) async {
      tester.view.physicalSize = const Size(800, 1200);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);

      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: GoalsScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Top Header & Count Pill
      expect(find.text('GOAL PACING'), findsOneWidget);
      expect(find.text('ACTIVE: 2'), findsOneWidget);

      // Aggregate Monthly Savings Target Banner
      expect(find.text('MONTHLY SAVINGS TARGET'), findsOneWidget);
      expect(find.text('INR 13,833'), findsOneWidget);

      // Section Header
      expect(find.text('TARGET PACING ALLOCATION'), findsOneWidget);

      // First Goal: Emergency Fund Reserve
      expect(find.text('EMERGENCY FUND RESERVE'), findsOneWidget);
      expect(find.text('ON TRACK'), findsOneWidget);
      expect(find.text('INR 50,000 / 72,000'), findsOneWidget);
      expect(find.text('69%'), findsOneWidget);
      expect(find.text('PACING: INR 5,500/MO'), findsOneWidget);
      expect(find.text('TARGET: 2026-12-31'), findsOneWidget);

      // Second Goal: Annual Family Vacation
      expect(find.text('ANNUAL FAMILY VACATION'), findsOneWidget);
      expect(find.text('AT RISK'), findsOneWidget);
      expect(find.text('INR 15,000 / 40,000'), findsOneWidget);
      expect(find.text('38%'), findsOneWidget);
      expect(find.text('PACING: INR 8,333/MO'), findsOneWidget);
      expect(find.text('TARGET: 2026-11-30'), findsOneWidget);

      // Progress Indicators with binary monochrome styling
      expect(find.byType(LinearProgressIndicator), findsNWidgets(2));
    });
  });
}
