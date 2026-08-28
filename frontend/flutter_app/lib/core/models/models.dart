// Financial Domain Models conforming strictly to shared contracts

class GoalModel {
  final String goalId;
  final String userId;
  final String title;
  final double targetAmount;
  final double currentAmount;
  final String currency;
  final String targetDate;
  final double monthlyContributionRequired;
  final int priority;
  final String status;

  GoalModel({
    required this.goalId,
    required this.userId,
    required this.title,
    required this.targetAmount,
    required this.currentAmount,
    this.currency = 'INR',
    required this.targetDate,
    required this.monthlyContributionRequired,
    required this.priority,
    required this.status,
  });

  double get progress => targetAmount > 0 ? (currentAmount / targetAmount).clamp(0.0, 1.0) : 0.0;
  int get progressPercent => (progress * 100).round();

  factory GoalModel.fromJson(Map<String, dynamic> json) {
    return GoalModel(
      goalId: json['goal_id'] as String? ?? '',
      userId: json['user_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      targetAmount: (json['target_amount'] as num?)?.toDouble() ?? 0.0,
      currentAmount: (json['current_amount'] as num?)?.toDouble() ?? 0.0,
      currency: json['currency'] as String? ?? 'INR',
      targetDate: json['target_date'] as String? ?? '',
      monthlyContributionRequired: (json['monthly_contribution_required'] as num?)?.toDouble() ?? 0.0,
      priority: json['priority'] as int? ?? 1,
      status: json['status'] as String? ?? 'on_track',
    );
  }

  Map<String, dynamic> toJson() => {
    'goal_id': goalId,
    'user_id': userId,
    'title': title,
    'target_amount': targetAmount,
    'current_amount': currentAmount,
    'currency': currency,
    'target_date': targetDate,
    'monthly_contribution_required': monthlyContributionRequired,
    'priority': priority,
    'status': status,
  };
}

class RiskSignalModel {
  final String signalId;
  final String type;
  final String severity;
  final String title;
  final String description;
  final double amountImpact;
  final String detectedAt;
  final bool isActive;

  RiskSignalModel({
    required this.signalId,
    required this.type,
    required this.severity,
    required this.title,
    required this.description,
    required this.amountImpact,
    required this.detectedAt,
    required this.isActive,
  });

  factory RiskSignalModel.fromJson(Map<String, dynamic> json) {
    return RiskSignalModel(
      signalId: json['signal_id'] as String? ?? '',
      type: json['type'] as String? ?? '',
      severity: json['severity'] as String? ?? 'medium',
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      amountImpact: (json['amount_impact'] as num?)?.toDouble() ?? 0.0,
      detectedAt: json['detected_at'] as String? ?? '',
      isActive: json['is_active'] as bool? ?? true,
    );
  }

  Map<String, dynamic> toJson() => {
    'signal_id': signalId,
    'type': type,
    'severity': severity,
    'title': title,
    'description': description,
    'amount_impact': amountImpact,
    'detected_at': detectedAt,
    'is_active': isActive,
  };
}

class FinancialStateModel {
  final String userId;
  final String generatedAt;
  final double currentBalance;
  final double availableCash;
  final double expectedMonthlyIncome;
  final double fixedExpenses;
  final double variableExpenses;
  final double discretionaryExpenses;
  final double recurringObligations;
  final double upcomingObligations;
  final double savings;
  final double emergencyFundMonths;
  final double savingsRate;
  final List<GoalModel> financialGoals;
  final double investmentsTotalValue;
  final double projectedBalance;
  final double minimumCashBuffer;
  final List<RiskSignalModel> riskSignals;
  final double dataCompleteness;
  final double overallConfidence;

  FinancialStateModel({
    required this.userId,
    required this.generatedAt,
    required this.currentBalance,
    required this.availableCash,
    required this.expectedMonthlyIncome,
    required this.fixedExpenses,
    required this.variableExpenses,
    required this.discretionaryExpenses,
    required this.recurringObligations,
    required this.upcomingObligations,
    required this.savings,
    required this.emergencyFundMonths,
    required this.savingsRate,
    required this.financialGoals,
    required this.investmentsTotalValue,
    required this.projectedBalance,
    required this.minimumCashBuffer,
    required this.riskSignals,
    required this.dataCompleteness,
    required this.overallConfidence,
  });

  factory FinancialStateModel.fromJson(Map<String, dynamic> json) {
    return FinancialStateModel(
      userId: json['user_id'] as String? ?? '',
      generatedAt: json['generated_at'] as String? ?? '',
      currentBalance: (json['current_balance'] as num?)?.toDouble() ?? 0.0,
      availableCash: (json['available_cash'] as num?)?.toDouble() ?? 0.0,
      expectedMonthlyIncome: (json['expected_monthly_income'] as num?)?.toDouble() ?? 0.0,
      fixedExpenses: (json['fixed_expenses'] as num?)?.toDouble() ?? 0.0,
      variableExpenses: (json['variable_expenses'] as num?)?.toDouble() ?? 0.0,
      discretionaryExpenses: (json['discretionary_expenses'] as num?)?.toDouble() ?? 0.0,
      recurringObligations: (json['recurring_obligations'] as num?)?.toDouble() ?? 0.0,
      upcomingObligations: (json['upcoming_obligations'] as num?)?.toDouble() ?? 0.0,
      savings: (json['savings'] as num?)?.toDouble() ?? 0.0,
      emergencyFundMonths: (json['emergency_fund_months'] as num?)?.toDouble() ?? 0.0,
      savingsRate: (json['savings_rate'] as num?)?.toDouble() ?? 0.0,
      financialGoals: (json['financial_goals'] as List<dynamic>?)
              ?.map((e) => GoalModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      investmentsTotalValue: (json['investments_total_value'] as num?)?.toDouble() ?? 0.0,
      projectedBalance: (json['projected_balance'] as num?)?.toDouble() ?? 0.0,
      minimumCashBuffer: (json['minimum_cash_buffer'] as num?)?.toDouble() ?? 0.0,
      riskSignals: (json['risk_signals'] as List<dynamic>?)
              ?.map((e) => RiskSignalModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      dataCompleteness: (json['data_completeness'] as num?)?.toDouble() ?? 1.0,
      overallConfidence: (json['overall_confidence'] as num?)?.toDouble() ?? 1.0,
    );
  }

  Map<String, dynamic> toJson() => {
    'user_id': userId,
    'generated_at': generatedAt,
    'current_balance': currentBalance,
    'available_cash': availableCash,
    'expected_monthly_income': expectedMonthlyIncome,
    'fixed_expenses': fixedExpenses,
    'variable_expenses': variableExpenses,
    'discretionary_expenses': discretionaryExpenses,
    'recurring_obligations': recurringObligations,
    'upcoming_obligations': upcomingObligations,
    'savings': savings,
    'emergency_fund_months': emergencyFundMonths,
    'savings_rate': savingsRate,
    'financial_goals': financialGoals.map((e) => e.toJson()).toList(),
    'investments_total_value': investmentsTotalValue,
    'projected_balance': projectedBalance,
    'minimum_cash_buffer': minimumCashBuffer,
    'risk_signals': riskSignals.map((e) => e.toJson()).toList(),
    'data_completeness': dataCompleteness,
    'overall_confidence': overallConfidence,
  };
}

class TransactionModel {
  final String transactionId;
  final String userId;
  final String accountId;
  final double amount;
  final String currency;
  final String type; // debit or credit
  final String category;
  final String description;
  final String timestamp;
  final String source;
  final double confidence;
  final bool isRecurring;

  TransactionModel({
    required this.transactionId,
    required this.userId,
    required this.accountId,
    required this.amount,
    this.currency = 'INR',
    required this.type,
    required this.category,
    required this.description,
    required this.timestamp,
    this.source = 'manual',
    this.confidence = 1.0,
    this.isRecurring = false,
  });

  bool get isCredit => type.toLowerCase() == 'credit';

  factory TransactionModel.fromJson(Map<String, dynamic> json) {
    return TransactionModel(
      transactionId: json['transaction_id'] as String? ?? '',
      userId: json['user_id'] as String? ?? '',
      accountId: json['account_id'] as String? ?? '',
      amount: (json['amount'] as num?)?.toDouble() ?? 0.0,
      currency: json['currency'] as String? ?? 'INR',
      type: json['type'] as String? ?? 'debit',
      category: json['category'] as String? ?? 'other',
      description: json['description'] as String? ?? '',
      timestamp: json['timestamp'] as String? ?? '',
      source: json['source'] as String? ?? 'manual',
      confidence: (json['confidence'] as num?)?.toDouble() ?? 1.0,
      isRecurring: json['is_recurring'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() => {
    'transaction_id': transactionId,
    'user_id': userId,
    'account_id': accountId,
    'amount': amount,
    'currency': currency,
    'type': type,
    'category': category,
    'description': description,
    'timestamp': timestamp,
    'source': source,
    'confidence': confidence,
    'is_recurring': isRecurring,
  };
}

class EvidenceModel {
  final String metric;
  final double value;
  final double? threshold;
  final String status;
  final String description;

  EvidenceModel({
    required this.metric,
    required this.value,
    this.threshold,
    required this.status,
    required this.description,
  });

  factory EvidenceModel.fromJson(Map<String, dynamic> json) {
    return EvidenceModel(
      metric: json['metric'] as String? ?? '',
      value: (json['value'] as num?)?.toDouble() ?? 0.0,
      threshold: (json['threshold'] as num?)?.toDouble(),
      status: json['status'] as String? ?? 'confirmed',
      description: json['description'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'metric': metric,
    'value': value,
    'threshold': threshold,
    'status': status,
    'description': description,
  };
}

class RecommendationItemModel {
  final String recommendationId;
  final String title;
  final String priority;
  final String description;
  final double impactAmount;
  final String category;

  RecommendationItemModel({
    required this.recommendationId,
    required this.title,
    required this.priority,
    required this.description,
    required this.impactAmount,
    required this.category,
  });

  factory RecommendationItemModel.fromJson(Map<String, dynamic> json) {
    return RecommendationItemModel(
      recommendationId: json['recommendation_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      priority: json['priority'] as String? ?? 'medium',
      description: json['description'] as String? ?? '',
      impactAmount: (json['impact_amount'] as num?)?.toDouble() ?? 0.0,
      category: json['category'] as String? ?? 'liquidity',
    );
  }

  Map<String, dynamic> toJson() => {
    'recommendation_id': recommendationId,
    'title': title,
    'priority': priority,
    'description': description,
    'impact_amount': impactAmount,
    'category': category,
  };
}

class AgentResponseModel {
  final String responseId;
  final String userId;
  final RecommendationItemModel recommendation;
  final String reason;
  final List<EvidenceModel> evidence;
  final double confidence;
  final List<String> alternatives;
  final List<String> competingObjectivesConsidered;
  final String generatedAt;

  AgentResponseModel({
    required this.responseId,
    required this.userId,
    required this.recommendation,
    required this.reason,
    required this.evidence,
    required this.confidence,
    required this.alternatives,
    required this.competingObjectivesConsidered,
    required this.generatedAt,
  });

  factory AgentResponseModel.fromJson(Map<String, dynamic> json) {
    return AgentResponseModel(
      responseId: json['response_id'] as String? ?? '',
      userId: json['user_id'] as String? ?? '',
      recommendation: RecommendationItemModel.fromJson(
        json['recommendation'] as Map<String, dynamic>? ?? {},
      ),
      reason: json['reason'] as String? ?? '',
      evidence: (json['evidence'] as List<dynamic>?)
              ?.map((e) => EvidenceModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      confidence: (json['confidence'] as num?)?.toDouble() ?? 0.95,
      alternatives: (json['alternatives'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      competingObjectivesConsidered: (json['competing_objectives_considered'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
      generatedAt: json['generated_at'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'response_id': responseId,
    'user_id': userId,
    'recommendation': recommendation.toJson(),
    'reason': reason,
    'evidence': evidence.map((e) => e.toJson()).toList(),
    'confidence': confidence,
    'alternatives': alternatives,
    'competing_objectives_considered': competingObjectivesConsidered,
    'generated_at': generatedAt,
  };
}

class GoalImpactModel {
  final String goalId;
  final String title;
  final int delayMonths;
  final String impact;

  GoalImpactModel({
    required this.goalId,
    required this.title,
    required this.delayMonths,
    required this.impact,
  });

  factory GoalImpactModel.fromJson(Map<String, dynamic> json) {
    return GoalImpactModel(
      goalId: json['goal_id'] as String? ?? '',
      title: json['title'] as String? ?? '',
      delayMonths: json['delay_months'] as int? ?? 0,
      impact: json['impact'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'goal_id': goalId,
    'title': title,
    'delay_months': delayMonths,
    'impact': impact,
  };
}

class SimulationResultModel {
  final String userId;
  final String scenarioType;
  final double baselineProjectedBalance;
  final double simulatedProjectedBalance;
  final bool bufferViolationRisk;
  final String impactSummary;
  final List<GoalImpactModel> goalImpacts;
  final String recommendation;

  SimulationResultModel({
    required this.userId,
    required this.scenarioType,
    required this.baselineProjectedBalance,
    required this.simulatedProjectedBalance,
    required this.bufferViolationRisk,
    required this.impactSummary,
    required this.goalImpacts,
    required this.recommendation,
  });

  factory SimulationResultModel.fromJson(Map<String, dynamic> json) {
    return SimulationResultModel(
      userId: json['user_id'] as String? ?? '',
      scenarioType: json['scenario_type'] as String? ?? 'unexpected_expense',
      baselineProjectedBalance: (json['baseline_projected_balance'] as num?)?.toDouble() ?? 0.0,
      simulatedProjectedBalance: (json['simulated_projected_balance'] as num?)?.toDouble() ?? 0.0,
      bufferViolationRisk: json['buffer_violation_risk'] as bool? ?? false,
      impactSummary: json['impact_summary'] as String? ?? '',
      goalImpacts: (json['goal_impacts'] as List<dynamic>?)
              ?.map((e) => GoalImpactModel.fromJson(e as Map<String, dynamic>))
              .toList() ??
          [],
      recommendation: json['recommendation'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    'user_id': userId,
    'scenario_type': scenarioType,
    'baseline_projected_balance': baselineProjectedBalance,
    'simulated_projected_balance': simulatedProjectedBalance,
    'buffer_violation_risk': bufferViolationRisk,
    'impact_summary': impactSummary,
    'goal_impacts': goalImpacts.map((e) => e.toJson()).toList(),
    'recommendation': recommendation,
  };
}
