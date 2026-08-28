import 'package:dio/dio.dart';
import '../models/models.dart';

class ApiClient {
  final Dio _dio;
  static const String baseUrl = 'http://localhost:8000/api/v1';

  ApiClient()
      : _dio = Dio(BaseOptions(
          baseUrl: baseUrl,
          connectTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 10),
        ));

  Future<FinancialStateModel> getFinancialState({required String userId}) async {
    try {
      final response = await _dio.get('/financial-state', queryParameters: {'user_id': userId});
      return FinancialStateModel.fromJson(response.data);
    } catch (e) {
      return fallbackFinancialState;
    }
  }

  Future<List<TransactionModel>> getTransactions({required String userId}) async {
    try {
      final response = await _dio.get('/transactions', queryParameters: {'user_id': userId});
      final List data = response.data;
      return data.map((e) => TransactionModel.fromJson(e)).toList();
    } catch (e) {
      return fallbackTransactions;
    }
  }

  Future<AgentResponseModel> getDecisionAdvice({required String userId, String? query}) async {
    try {
      final response = await _dio.post('/agent/analyze', data: {
        'user_id': userId,
        if (query != null) 'user_query': query,
      });
      return AgentResponseModel.fromJson(response.data);
    } catch (e) {
      return fallbackAgentResponse;
    }
  }

  Future<SimulationResultModel> simulateScenario({
    required String userId,
    required double shockAmount,
    String scenarioType = 'unexpected_expense',
  }) async {
    try {
      final response = await _dio.post('/simulation', data: {
        'user_id': userId,
        'amount': shockAmount,
        'scenario_type': scenarioType,
      });
      return SimulationResultModel.fromJson(response.data);
    } catch (e) {
      return fallbackSimulationResult;
    }
  }

  // --- Mock Fallback Data (Deterministic Fixtures) ---

  static final FinancialStateModel fallbackFinancialState = FinancialStateModel(
    userId: 'user_demo_01',
    generatedAt: DateTime.now().toIso8601String(),
    currentBalance: 30000.0,
    availableCash: 12450.0,
    expectedMonthlyIncome: 65000.0,
    fixedExpenses: 28000.0,
    variableExpenses: 12000.0,
    discretionaryExpenses: 8000.0,
    recurringObligations: 18000.0,
    upcomingObligations: 18050.0,
    savings: 50000.0,
    emergencyFundMonths: 2.1,
    savingsRate: 0.15,
    investmentsTotalValue: 125000.0,
    projectedBalance: 19400.0,
    minimumCashBuffer: 25000.0,
    financialGoals: [
      GoalModel(
        goalId: 'goal_01',
        userId: 'user_demo_01',
        title: 'Emergency Reserve Fund',
        targetAmount: 72000.0,
        currentAmount: 45000.0,
        targetDate: '2024-10-31',
        monthlyContributionRequired: 5500.0,
        priority: 1,
        status: 'on_track',
      ),
      GoalModel(
        goalId: 'goal_02',
        userId: 'user_demo_01',
        title: 'Family Vacation',
        targetAmount: 40000.0,
        currentAmount: 12000.0,
        targetDate: '2024-12-15',
        monthlyContributionRequired: 8333.0,
        priority: 3,
        status: 'behind',
      ),
    ],
    riskSignals: [
      RiskSignalModel(
        signalId: 'sig_01',
        type: 'liquidity',
        severity: 'high',
        title: 'Liquidity Buffer Deficit',
        description: 'Projected balance falls below the minimum safety threshold.',
        amountImpact: 5600.0,
        detectedAt: DateTime.now().toIso8601String(),
        isActive: true,
      ),
    ],
    dataCompleteness: 0.95,
    overallConfidence: 0.94,
  );

  static final List<TransactionModel> fallbackTransactions = [
    TransactionModel(
      transactionId: 'tx_01',
      userId: 'user_demo_01',
      accountId: 'acc_main',
      amount: 12000.0,
      type: 'debit',
      category: 'unexpected',
      description: 'Medical Expense - Hospital',
      timestamp: DateTime.now().subtract(const Duration(days: 1)).toIso8601String(),
      source: 'sms',
      confidence: 0.98,
    ),
    TransactionModel(
      transactionId: 'tx_02',
      userId: 'user_demo_01',
      accountId: 'acc_main',
      amount: 65000.0,
      type: 'credit',
      category: 'income',
      description: 'Monthly Salary Credit',
      timestamp: DateTime.now().subtract(const Duration(days: 5)).toIso8601String(),
      source: 'bank_api',
      confidence: 1.0,
    ),
  ];

  static final AgentResponseModel fallbackAgentResponse = AgentResponseModel(
    responseId: 'resp_01',
    userId: 'user_demo_01',
    recommendation: RecommendationItemModel(
      recommendationId: 'rec_01',
      title: 'Preserve Near-Term Liquidity',
      priority: 'high',
      description: 'Pause vacation goal funding and reduce discretionary dining to recover INR 5,600.',
      impactAmount: 5600.0,
      category: 'liquidity',
    ),
    reason: 'Expenditure velocity exceeds projected inflow by 1.2x. Maintaining current allocation poses a liquidity threat.',
    evidence: [
      EvidenceModel(metric: 'liquid_balance', value: 12450.0, status: 'confirmed', description: 'Current available cash'),
      EvidenceModel(metric: 'pending_bills', value: 18050.0, status: 'confirmed', description: 'Due in next 30 days'),
    ],
    confidence: 0.94,
    alternatives: [
      'Pause Vacation Goal Funding (Recovers INR 4,000)',
      'Trim Dining Budget (Recovers INR 1,600)',
    ],
    competingObjectivesConsidered: [
      'Liquidity preservation vs. Secondary goal allocation',
      'Immediate obligation coverage vs. Investment yield',
    ],
    generatedAt: DateTime.now().toIso8601String(),
  );

  static final SimulationResultModel fallbackSimulationResult = SimulationResultModel(
    userId: 'user_demo_01',
    scenarioType: 'unexpected_expense',
    baselineProjectedBalance: 19400.0,
    simulatedProjectedBalance: 7400.0,
    bufferViolationRisk: true,
    impactSummary: 'An additional INR 12,000 expense will result in a critical breach of your safety buffer.',
    recommendation: 'Immediate reduction in discretionary spend is required to avoid buffer violation.',
    goalImpacts: [
      GoalImpactModel(goalId: 'goal_02', title: 'Family Vacation', delayMonths: 2, impact: 'Delayed by 60 days'),
    ],
  );
}
