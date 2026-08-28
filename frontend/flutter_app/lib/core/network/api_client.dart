import 'package:dio/dio.dart';
import '../models/models.dart';

/// ApiClient connects to FastAPI http://localhost:8000/api/v1
/// with full offline mock fallback adhering to shared contracts.
class ApiClient {
  final Dio _dio;
  final String baseUrl;

  ApiClient({
    Dio? dio,
    this.baseUrl = 'http://localhost:8000/api/v1',
  }) : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: baseUrl,
                connectTimeout: const Duration(milliseconds: 2500),
                receiveTimeout: const Duration(milliseconds: 3000),
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json',
                },
              ),
            );

  // --- Fallback Mock Data ---

  static final FinancialStateModel fallbackFinancialState = FinancialStateModel(
    userId: 'user_demo_01',
    generatedAt: DateTime.now().toIso8601String(),
    currentBalance: 30000.0,
    availableCash: 12000.0,
    expectedMonthlyIncome: 65000.0,
    fixedExpenses: 24000.0,
    variableExpenses: 12000.0,
    discretionaryExpenses: 8500.0,
    recurringObligations: 24000.0,
    upcomingObligations: 18000.0,
    savings: 50000.0,
    emergencyFundMonths: 2.1,
    savingsRate: 0.23,
    financialGoals: [
      GoalModel(
        goalId: 'goal_emergency_01',
        userId: 'user_demo_01',
        title: 'Emergency Fund Reserve',
        targetAmount: 72000.0,
        currentAmount: 50000.0,
        targetDate: '2026-12-31',
        monthlyContributionRequired: 5500.0,
        priority: 1,
        status: 'on_track',
      ),
      GoalModel(
        goalId: 'goal_vacation_02',
        userId: 'user_demo_01',
        title: 'Annual Family Vacation',
        targetAmount: 40000.0,
        currentAmount: 15000.0,
        targetDate: '2026-11-30',
        monthlyContributionRequired: 8333.0,
        priority: 3,
        status: 'at_risk',
      ),
    ],
    investmentsTotalValue: 140000.0,
    projectedBalance: 19400.0,
    minimumCashBuffer: 25000.0,
    riskSignals: [
      RiskSignalModel(
        signalId: 'risk_liq_001',
        type: 'liquidity',
        severity: 'medium',
        title: 'Projected Cash Deficit Against Buffer',
        description:
            'Projected month-end balance (INR 19,400) violates your minimum preferred reserve threshold (INR 25,000) by INR 5,600.',
        amountImpact: 5600.0,
        detectedAt: '2026-08-28T10:30:05Z',
        isActive: true,
      ),
    ],
    dataCompleteness: 0.92,
    overallConfidence: 0.94,
  );

  static final List<TransactionModel> fallbackTransactions = [
    TransactionModel(
      transactionId: 'tx_demo_001',
      userId: 'user_demo_01',
      accountId: 'acc_checking_01',
      amount: 65000.0,
      type: 'credit',
      category: 'income',
      description: 'Monthly Salary - Tech Corp',
      timestamp: '2026-08-01T09:00:00Z',
      source: 'bank_api',
      confidence: 1.0,
      isRecurring: true,
    ),
    TransactionModel(
      transactionId: 'tx_demo_002',
      userId: 'user_demo_01',
      accountId: 'acc_checking_01',
      amount: 22000.0,
      type: 'debit',
      category: 'housing',
      description: 'Apartment Monthly Rent',
      timestamp: '2026-08-03T10:15:00Z',
      source: 'bank_api',
      confidence: 1.0,
      isRecurring: true,
    ),
    TransactionModel(
      transactionId: 'tx_demo_003',
      userId: 'user_demo_01',
      accountId: 'acc_checking_01',
      amount: 2000.0,
      type: 'debit',
      category: 'utilities',
      description: 'Electricity & Water Bill',
      timestamp: '2026-08-05T14:30:00Z',
      source: 'bank_api',
      confidence: 1.0,
      isRecurring: true,
    ),
    TransactionModel(
      transactionId: 'tx_demo_004',
      userId: 'user_demo_01',
      accountId: 'acc_checking_01',
      amount: 9000.0,
      type: 'debit',
      category: 'groceries',
      description: 'Supermarket Weekly Provisions',
      timestamp: '2026-08-10T18:45:00Z',
      source: 'receipt',
      confidence: 0.95,
      isRecurring: false,
    ),
    TransactionModel(
      transactionId: 'tx_demo_005',
      userId: 'user_demo_01',
      accountId: 'acc_checking_01',
      amount: 12000.0,
      type: 'debit',
      category: 'unexpected',
      description: 'Urgent Medical Treatment & Diagnostics',
      timestamp: '2026-08-28T10:30:00Z',
      source: 'sms',
      confidence: 0.98,
      isRecurring: false,
    ),
  ];

  static final AgentResponseModel fallbackAgentResponse = AgentResponseModel(
    responseId: 'resp_demo_001',
    userId: 'user_demo_01',
    recommendation: RecommendationItemModel(
      recommendationId: 'rec_demo_001',
      title: 'Preserve Near-Term Liquidity',
      priority: 'high',
      description:
          'An unexpected expense of INR 12,000 has reduced your projected month-end balance to INR 19,400, falling INR 5,600 below your preferred cash buffer of INR 25,000. With an upcoming obligation of INR 18,000 due, we recommend pausing discretionary spending and deferring non-essential goal contributions.',
      impactAmount: 5600.0,
      category: 'liquidity',
    ),
    reason:
        'An unexpected medical transaction of INR 12,000 combined with an upcoming obligation of INR 18,000 will compress liquid reserves below your configured INR 25,000 minimum safety threshold.',
    evidence: [
      EvidenceModel(
        metric: 'current_balance',
        value: 30000.0,
        threshold: 42000.0,
        status: 'confirmed',
        description: 'Liquid bank balance after recent debit',
      ),
      EvidenceModel(
        metric: 'projected_balance',
        value: 19400.0,
        threshold: 25000.0,
        status: 'estimated',
        description: 'Deterministic 30-day forecast considering fixed costs and bills',
      ),
      EvidenceModel(
        metric: 'minimum_cash_buffer',
        value: 25000.0,
        threshold: null,
        status: 'confirmed',
        description: 'User preference target safety buffer',
      ),
      EvidenceModel(
        metric: 'upcoming_obligations',
        value: 18000.0,
        threshold: null,
        status: 'confirmed',
        description: 'Committed pending bills due in current cycle',
      ),
    ],
    confidence: 0.94,
    alternatives: [
      'Temporarily pause the INR 8,333 vacation goal contribution for this billing cycle.',
      'Reduce remaining discretionary dining and shopping allocations by INR 4,000.',
      'Utilize short-term liquid savings to protect primary checking buffer without touching long-term investments.',
    ],
    competingObjectivesConsidered: [
      'Liquidity preservation (Priority 1) vs. Secondary Vacation Goal pacing (Priority 3).',
      'Preserving long-term investment compounding (INR 140,000 portfolio intact) rather than liquidating equity assets.',
    ],
    generatedAt: '2026-08-28T10:30:10Z',
  );

  static final SimulationResultModel fallbackSimulationResult = SimulationResultModel(
    userId: 'user_demo_01',
    scenarioType: 'unexpected_expense',
    baselineProjectedBalance: 31400.0,
    simulatedProjectedBalance: 19400.0,
    bufferViolationRisk: true,
    impactSummary:
        'An immediate outflow of INR 12,000 reduces 30-day projected liquidity from INR 31,400 to INR 19,400, falling below your INR 25,000 safety threshold by INR 5,600.',
    goalImpacts: [
      GoalImpactModel(
        goalId: 'goal_vacation_02',
        title: 'Annual Family Vacation',
        delayMonths: 1,
        impact: 'Requires pausing contribution for 30 days to protect cash reserves',
      ),
    ],
    recommendation:
        'Maintain emergency buffer by deferring discretionary allocations and non-essential savings goals.',
  );

  // --- API Methods with Graceful Fallback ---

  Future<FinancialStateModel> getFinancialState({String userId = 'user_demo_01'}) async {
    try {
      final response = await _dio.get('/financial-state', queryParameters: {'user_id': userId});
      if (response.statusCode == 200 && response.data != null) {
        return FinancialStateModel.fromJson(response.data as Map<String, dynamic>);
      }
    } catch (_) {
      // Graceful offline fallback
    }
    return fallbackFinancialState;
  }

  Future<List<TransactionModel>> getTransactions({String userId = 'user_demo_01'}) async {
    try {
      final response = await _dio.get('/transactions', queryParameters: {'user_id': userId});
      if (response.statusCode == 200 && response.data != null) {
        final list = response.data as List<dynamic>;
        return list.map((e) => TransactionModel.fromJson(e as Map<String, dynamic>)).toList();
      }
    } catch (_) {
      // Graceful offline fallback
    }
    return fallbackTransactions;
  }

  Future<AgentResponseModel> getDecisionAdvice({
    String userId = 'user_demo_01',
    String? query,
  }) async {
    try {
      final response = await _dio.post(
        '/agent/query',
        data: {
          'user_id': userId,
          if (query != null && query.trim().isNotEmpty) 'query': query,
        },
      );
      if (response.statusCode == 200 && response.data != null) {
        return AgentResponseModel.fromJson(response.data as Map<String, dynamic>);
      }
    } catch (_) {
      // Graceful offline fallback
    }
    return fallbackAgentResponse;
  }

  Future<SimulationResultModel> simulateScenario({
    String userId = 'user_demo_01',
    double shockAmount = 12000.0,
    String scenarioType = 'unexpected_expense',
    String description = 'Simulated expense',
  }) async {
    try {
      final response = await _dio.post(
        '/simulate',
        data: {
          'user_id': userId,
          'amount': shockAmount,
          'scenario_type': scenarioType,
          'description': description,
        },
      );
      if (response.statusCode == 200 && response.data != null) {
        return SimulationResultModel.fromJson(response.data as Map<String, dynamic>);
      }
    } catch (_) {
      // Graceful offline fallback with dynamic calculation
    }

    const baseline = 31400.0;
    final simulated = baseline - shockAmount;
    const buffer = 25000.0;
    final isViolation = simulated < buffer;
    final deficit = (buffer - simulated).clamp(0.0, double.infinity);

    return SimulationResultModel(
      userId: userId,
      scenarioType: scenarioType,
      baselineProjectedBalance: baseline,
      simulatedProjectedBalance: simulated,
      bufferViolationRisk: isViolation,
      impactSummary: isViolation
          ? 'An outflow of INR ${shockAmount.toStringAsFixed(0)} reduces 30-day projected liquidity to INR ${simulated.toStringAsFixed(0)}, falling below your INR ${buffer.toStringAsFixed(0)} threshold by INR ${deficit.toStringAsFixed(0)}.'
          : 'An outflow of INR ${shockAmount.toStringAsFixed(0)} reduces 30-day projected liquidity to INR ${simulated.toStringAsFixed(0)}, safely maintaining your minimum buffer.',
      goalImpacts: [
        GoalImpactModel(
          goalId: 'goal_vacation_02',
          title: 'Annual Family Vacation',
          delayMonths: isViolation ? 1 : 0,
          impact: isViolation
              ? 'Requires pausing contribution for 30 days to protect cash reserves'
              : 'Target pacing maintained on track',
        ),
      ],
      recommendation: isViolation
          ? 'Maintain emergency buffer by deferring discretionary allocations and non-essential savings goals.'
          : 'Sufficient buffer margin exists. No immediate intervention required.',
    );
  }
}
