import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fidel_app/core/network/api_client.dart';
import 'package:fidel_app/core/models/models.dart';
import 'package:fidel_app/core/providers/state_providers.dart';

void main() {
  group('ApiClient & Riverpod State Providers (HW-007) Tests', () {
    late ApiClient client;

    setUp(() {
      client = ApiClient(baseUrl: 'http://localhost:8000/api/v1');
    });

    test('ApiClient initializes with correct base URL and default options', () {
      expect(client.baseUrl, 'http://localhost:8000/api/v1');
    });

    test('getFinancialState returns fallback model gracefully when offline', () async {
      final state = await client.getFinancialState(userId: 'user_demo_01');
      expect(state.userId, 'user_demo_01');
      expect(state.currentBalance, 30000.0);
      expect(state.availableCash, 12000.0);
      expect(state.expectedMonthlyIncome, 65000.0);
      expect(state.fixedExpenses, 24000.0);
      expect(state.variableExpenses, 12000.0);
      expect(state.savings, 50000.0);
      expect(state.emergencyFundMonths, 2.1);
      expect(state.financialGoals.length, 2);
      expect(state.riskSignals.length, 1);
      expect(state.riskSignals.first.type, 'liquidity');
      expect(state.riskSignals.first.severity, 'medium');
      expect(state.dataCompleteness, 0.92);
      expect(state.overallConfidence, 0.94);
    });

    test('getTransactions returns fallback transactions list gracefully when offline', () async {
      final txList = await client.getTransactions(userId: 'user_demo_01');
      expect(txList.length, 5);
      expect(txList[0].transactionId, 'tx_demo_001');
      expect(txList[0].category, 'income');
      expect(txList[0].isCredit, true);
      expect(txList[0].amount, 65000.0);
      expect(txList[1].category, 'housing');
      expect(txList[1].isCredit, false);
      expect(txList[1].amount, 22000.0);
      expect(txList[4].category, 'unexpected');
      expect(txList[4].confidence, 0.98);
    });

    test('getDecisionAdvice returns fallback agent response model gracefully when offline', () async {
      final advice = await client.getDecisionAdvice(
        userId: 'user_demo_01',
        query: 'How to handle unexpected medical expense?',
      );
      expect(advice.responseId, 'resp_demo_001');
      expect(advice.recommendation.title, 'Preserve Near-Term Liquidity');
      expect(advice.recommendation.priority, 'high');
      expect(advice.recommendation.impactAmount, 5600.0);
      expect(advice.evidence.length, 4);
      expect(advice.confidence, 0.94);
      expect(advice.alternatives.length, 3);
      expect(advice.competingObjectivesConsidered.length, 2);
    });

    test('simulateScenario performs deterministic fallback calculation accurately', () async {
      // Scenario with buffer violation
      final simViolation = await client.simulateScenario(
        userId: 'user_demo_01',
        shockAmount: 12000.0,
      );
      expect(simViolation.baselineProjectedBalance, 31400.0);
      expect(simViolation.simulatedProjectedBalance, 19400.0);
      expect(simViolation.bufferViolationRisk, true);
      expect(simViolation.goalImpacts.length, 1);
      expect(simViolation.goalImpacts.first.delayMonths, 1);

      // Scenario with buffer preserved
      final simPreserved = await client.simulateScenario(
        userId: 'user_demo_01',
        shockAmount: 2000.0,
      );
      expect(simPreserved.simulatedProjectedBalance, 29400.0);
      expect(simPreserved.bufferViolationRisk, false);
      expect(simPreserved.goalImpacts.first.delayMonths, 0);
    });

    test('Domain models serialize and deserialize to JSON without precision loss', () {
      final original = ApiClient.fallbackFinancialState;
      final json = original.toJson();
      final reconstructed = FinancialStateModel.fromJson(json);

      expect(reconstructed.userId, original.userId);
      expect(reconstructed.currentBalance, original.currentBalance);
      expect(reconstructed.availableCash, original.availableCash);
      expect(reconstructed.financialGoals.length, original.financialGoals.length);
      expect(reconstructed.riskSignals.length, original.riskSignals.length);
    });

    test('Riverpod State Providers manage state transitions correctly', () async {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      // Verify default state
      expect(container.read(currentUserIdProvider), 'user_demo_01');
      expect(container.read(activeTabProvider), 0);
      expect(container.read(transactionCategoryFilterProvider), 'ALL');
      expect(container.read(transactionSearchQueryProvider), '');

      // Verify filtered transactions default count
      final transactions = container.read(filteredTransactionsProvider);
      expect(transactions.length, 5);

      // Update category filter to GROCERIES
      container.read(transactionCategoryFilterProvider.notifier).state = 'GROCERIES';
      final groceryTx = container.read(filteredTransactionsProvider);
      expect(groceryTx.length, 1);
      expect(groceryTx.first.description, 'Supermarket Weekly Provisions');

      // Update search query to rent
      container.read(transactionCategoryFilterProvider.notifier).state = 'ALL';
      container.read(transactionSearchQueryProvider.notifier).state = 'rent';
      final rentTx = container.read(filteredTransactionsProvider);
      expect(rentTx.length, 1);
      expect(rentTx.first.description, 'Apartment Monthly Rent');
    });
  });
}
