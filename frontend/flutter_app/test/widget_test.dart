import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fidel_app/main.dart';
import 'package:fidel_app/core/theme/app_theme.dart';
import 'package:fidel_app/core/network/api_client.dart';

void main() {
  group('Fidel Mobile Platform App Tests', () {
    testWidgets('Boot FidelApp and verify Overview dashboard renders with metrics',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: FidelApp(),
        ),
      );
      await tester.pumpAndSettle();

      // Verify App Branding
      expect(find.text('FIDEL'), findsOneWidget);
      expect(find.text('LIVE AUTONOMOUS ENGINE'), findsOneWidget);

      // Verify Hero Headline
      expect(find.text('Preserve Liquidity.\nReason Over Tradeoffs.'), findsOneWidget);

      // Verify Metric Cards
      expect(find.text('CURRENT BALANCE'), findsOneWidget);
      expect(find.text('AVAILABLE CASH'), findsOneWidget);
      expect(find.text('30-DAY PROJECTED'), findsOneWidget);
      expect(find.text('EMERGENCY FUND'), findsOneWidget);

      // Verify Strategic Decision Card
      expect(find.text('PRESERVE NEAR-TERM LIQUIDITY'), findsOneWidget);
      expect(find.text('OPEN AI ADVISOR'), findsWidgets);
    });

    testWidgets('Switch tabs via bottom navigation bar without losing state',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: FidelApp(),
        ),
      );
      await tester.pumpAndSettle();

      // Switch to ADVISOR tab
      await tester.tap(find.text('ADVISOR'));
      await tester.pumpAndSettle();
      expect(find.text('AI ADVISOR'), findsOneWidget);
      expect(find.text('DETERMINISTIC EVIDENCE MATRIX'), findsOneWidget);

      // Switch to LEDGER tab
      await tester.tap(find.text('LEDGER'));
      await tester.pumpAndSettle();
      expect(find.text('TRANSACTION LEDGER'), findsOneWidget);
      expect(find.text('COUNT: 5'), findsOneWidget);
      expect(find.text('ALL'), findsOneWidget);
      expect(find.text('INCOME'), findsWidgets);

      // Switch to GOALS tab
      await tester.tap(find.text('GOALS'));
      await tester.pumpAndSettle();
      expect(find.text('GOAL PACING'), findsOneWidget);
      expect(find.text('EMERGENCY FUND RESERVE'), findsOneWidget);
      expect(find.text('ANNUAL FAMILY VACATION'), findsOneWidget);

      // Switch to SIMULATE tab
      await tester.tap(find.text('SIMULATE'));
      await tester.pumpAndSettle();
      expect(find.text('WHAT-IF SIMULATION'), findsOneWidget);
      expect(find.text('CALCULATE TRAJECTORY'), findsOneWidget);
      expect(find.text('BUFFER VIOLATION'), findsOneWidget);
    });

    test('FinancialStateModel deserializes correctly from contract JSON', () {
      final state = ApiClient.fallbackFinancialState;
      expect(state.userId, 'user_demo_01');
      expect(state.currentBalance, 30000.0);
      expect(state.availableCash, 12000.0);
      expect(state.projectedBalance, 19400.0);
      expect(state.financialGoals.length, 2);
    });

    test('AgentResponseModel deserializes correctly from contract JSON', () {
      final advisor = ApiClient.fallbackAgentResponse;
      expect(advisor.recommendation.title, 'Preserve Near-Term Liquidity');
      expect(advisor.evidence.length, 4);
      expect(advisor.alternatives.length, 3);
    });

    test('SimulationResultModel correctly computes buffer violation', () {
      final sim = ApiClient.fallbackSimulationResult;
      expect(sim.bufferViolationRisk, true);
      expect(sim.simulatedProjectedBalance, 19400.0);
    });

    test('Theme geometry adheres to Monopo Saigon strict rules', () {
      final theme = AppTheme.darkTheme;
      expect(theme.cardTheme.shape, isA<RoundedRectangleBorder>());
      final cardShape = theme.cardTheme.shape as RoundedRectangleBorder;
      expect(cardShape.borderRadius, BorderRadius.zero);
    });
  });
}
