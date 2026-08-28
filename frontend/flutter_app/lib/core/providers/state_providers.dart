import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/models.dart';
import '../network/api_client.dart';

// --- Core Singletons ---

final apiClientProvider = Provider<ApiClient>((ref) {
  return ApiClient();
});

final currentUserIdProvider = StateProvider<String>((ref) {
  return 'user_demo_01';
});

final activeTabProvider = StateProvider<int>((ref) {
  return 0;
});

// --- Financial State Provider ---

final financialStateProvider = FutureProvider<FinancialStateModel>((ref) async {
  final client = ref.watch(apiClientProvider);
  final userId = ref.watch(currentUserIdProvider);
  return client.getFinancialState(userId: userId);
});

// --- Transactions Providers & Filtering ---

final rawTransactionsProvider = FutureProvider<List<TransactionModel>>((ref) async {
  final client = ref.watch(apiClientProvider);
  final userId = ref.watch(currentUserIdProvider);
  return client.getTransactions(userId: userId);
});

final transactionCategoryFilterProvider = StateProvider<String>((ref) {
  return 'ALL';
});

final transactionSearchQueryProvider = StateProvider<String>((ref) {
  return '';
});

final filteredTransactionsProvider = Provider<List<TransactionModel>>((ref) {
  final asyncTx = ref.watch(rawTransactionsProvider);
  final transactions = asyncTx.when(
    data: (data) => data.isNotEmpty ? data : ApiClient.fallbackTransactions,
    loading: () => ApiClient.fallbackTransactions,
    error: (_, __) => ApiClient.fallbackTransactions,
  );
  final category = ref.watch(transactionCategoryFilterProvider).toUpperCase();
  final query = ref.watch(transactionSearchQueryProvider).trim().toLowerCase();

  return transactions.where((tx) {
    // Category match
    if (category != 'ALL' && tx.category.toUpperCase() != category) {
      return false;
    }
    // Search query match
    if (query.isNotEmpty) {
      final descMatch = tx.description.toLowerCase().contains(query);
      final catMatch = tx.category.toLowerCase().contains(query);
      final sourceMatch = tx.source.toLowerCase().contains(query);
      if (!descMatch && !catMatch && !sourceMatch) {
        return false;
      }
    }
    return true;
  }).toList();
});

// --- AI Advisor State ---

class AiAdvisorState {
  final AgentResponseModel response;
  final bool isLoading;
  final String? error;
  final String currentQuery;

  AiAdvisorState({
    required this.response,
    this.isLoading = false,
    this.error,
    this.currentQuery = '',
  });

  AiAdvisorState copyWith({
    AgentResponseModel? response,
    bool? isLoading,
    String? error,
    String? currentQuery,
  }) {
    return AiAdvisorState(
      response: response ?? this.response,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      currentQuery: currentQuery ?? this.currentQuery,
    );
  }
}

class AiAdvisorNotifier extends StateNotifier<AiAdvisorState> {
  final ApiClient _client;
  final String _userId;

  AiAdvisorNotifier(this._client, this._userId)
      : super(AiAdvisorState(response: ApiClient.fallbackAgentResponse));

  Future<void> submitQuery(String query) async {
    if (query.trim().isEmpty) return;
    state = state.copyWith(isLoading: true, currentQuery: query, error: null);
    try {
      final result = await _client.getDecisionAdvice(userId: _userId, query: query);
      state = state.copyWith(response: result, isLoading: false);
    } catch (e) {
      state = state.copyWith(isLoading: false, error: e.toString());
    }
  }

  void refresh() async {
    state = state.copyWith(isLoading: true, error: null);
    final result = await _client.getDecisionAdvice(userId: _userId);
    state = state.copyWith(response: result, isLoading: false);
  }
}

final aiAdvisorProvider = StateNotifierProvider<AiAdvisorNotifier, AiAdvisorState>((ref) {
  final client = ref.watch(apiClientProvider);
  final userId = ref.watch(currentUserIdProvider);
  return AiAdvisorNotifier(client, userId);
});

// --- Simulation State ---

class SimulationState {
  final double shockAmount;
  final SimulationResultModel result;
  final bool isLoading;

  SimulationState({
    required this.shockAmount,
    required this.result,
    this.isLoading = false,
  });

  SimulationState copyWith({
    double? shockAmount,
    SimulationResultModel? result,
    bool? isLoading,
  }) {
    return SimulationState(
      shockAmount: shockAmount ?? this.shockAmount,
      result: result ?? this.result,
      isLoading: isLoading ?? this.isLoading,
    );
  }
}

class SimulationNotifier extends StateNotifier<SimulationState> {
  final ApiClient _client;
  final String _userId;

  SimulationNotifier(this._client, this._userId)
      : super(
          SimulationState(
            shockAmount: 12000.0,
            result: ApiClient.fallbackSimulationResult,
          ),
        );

  Future<void> calculateTrajectory(double amount) async {
    state = state.copyWith(shockAmount: amount, isLoading: true);
    final result = await _client.simulateScenario(
      userId: _userId,
      shockAmount: amount,
    );
    state = state.copyWith(result: result, isLoading: false);
  }
}

final simulationProvider = StateNotifierProvider<SimulationNotifier, SimulationState>((ref) {
  final client = ref.watch(apiClientProvider);
  final userId = ref.watch(currentUserIdProvider);
  return SimulationNotifier(client, userId);
});
