import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../core/network/api_client.dart';
import '../../core/providers/state_providers.dart';
import '../../core/models/models.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  static final NumberFormat currencyFormat = NumberFormat('#,##0', 'en_IN');

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final stateAsync = ref.watch(financialStateProvider);
    final advisorState = ref.watch(aiAdvisorProvider);

    return Scaffold(
      backgroundColor: AppColors.obsidian,
      body: SafeArea(
        child: RefreshIndicator(
          color: AppColors.paper,
          backgroundColor: AppColors.inkstone,
          onRefresh: () async {
            ref.invalidate(financialStateProvider);
            ref.read(aiAdvisorProvider.notifier).refresh();
          },
          child: SingleChildScrollView(
            physics: const AlwaysScrollableScrollPhysics(),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
            child: stateAsync.when(
              data: (state) => _buildContent(context, ref, state, advisorState.response),
              loading: () => _buildContent(context, ref, ApiClient.fallbackFinancialState, advisorState.response),
              error: (_, __) => _buildContent(context, ref, ApiClient.fallbackFinancialState, advisorState.response),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildContent(
    BuildContext context,
    WidgetRef ref,
    FinancialStateModel state,
    AgentResponseModel advisor,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Top App Bar Branding
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text(
              'FIDEL',
              style: TextStyle(
                color: AppColors.paper,
                fontSize: 18,
                fontWeight: FontWeight.w800,
                letterSpacing: 3.0,
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: AppColors.inkstone,
                borderRadius: BorderRadius.circular(75.0),
                border: Border.all(color: AppColors.hairline),
              ),
              child: const Text(
                'LIVE AUTONOMOUS ENGINE',
                style: TextStyle(
                  color: AppColors.ashMist,
                  fontSize: 9,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 0.8,
                ),
              ),
            ),
          ],
        ),
        const SizedBox(height: 20),

        // 1. Atmospheric Hero Container
        _buildHeroSection(ref),
        const SizedBox(height: 20),

        // Section Title: Core Liquidity Matrix
        const Text(
          'DETERMINISTIC FINANCIAL STATE',
          style: AppTypography.cardHeader,
        ),
        const SizedBox(height: 10),

        // 2. 2x2 Metric Cards Grid
        _buildMetricGrid(state),
        const SizedBox(height: 20),

        // Section Title: Proactive Intelligence
        const Text(
          'STRATEGIC DECISION GUIDANCE',
          style: AppTypography.cardHeader,
        ),
        const SizedBox(height: 10),

        // 3. Strategic Decision Card
        _buildStrategicDecisionCard(ref, advisor),
        const SizedBox(height: 24),
      ],
    );
  }

  Widget _buildHeroSection(WidgetRef ref) {
    return Container(
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Stack(
        children: [
          // Iridescent Gradient Overlay at 25% opacity
          Positioned.fill(
            child: Opacity(
              opacity: 0.25,
              child: Container(
                decoration: const BoxDecoration(
                  gradient: AppColors.iridescentGradient,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppColors.obsidian,
                    borderRadius: BorderRadius.circular(75.0),
                    border: Border.all(color: AppColors.slatePill),
                  ),
                  child: const Text(
                    'REASONING ENGINE: ACTIVE',
                    style: TextStyle(
                      color: AppColors.paper,
                      fontSize: 9,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 1.0,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                const Text(
                  'Preserve Liquidity.\nReason Over Tradeoffs.',
                  style: AppTypography.heroHeadline,
                ),
                const SizedBox(height: 12),
                const Text(
                  'Autonomous detection identified a liquidity buffer deficit. Structured decision options synthesized below.',
                  style: AppTypography.bodySecondary,
                ),
                const SizedBox(height: 20),
                Row(
                  children: [
                    ElevatedButton(
                      onPressed: () {
                        ref.read(activeTabProvider.notifier).state = 1; // Tab 1: ADVISOR
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.paper,
                        foregroundColor: AppColors.obsidian,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(75.0),
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                      ),
                      child: const Text(
                        'OPEN ADVISOR',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 1.0,
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    OutlinedButton(
                      onPressed: () {
                        ref.read(activeTabProvider.notifier).state = 4; // Tab 4: SIMULATE
                      },
                      style: OutlinedButton.styleFrom(
                        foregroundColor: AppColors.paper,
                        side: const BorderSide(color: AppColors.paper, width: 1.0),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(75.0),
                        ),
                        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                      ),
                      child: const Text(
                        'SIMULATE',
                        style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w800,
                          letterSpacing: 1.0,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMetricGrid(FinancialStateModel state) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                title: 'CURRENT BALANCE',
                value: 'INR ${currencyFormat.format(state.currentBalance)}',
                subtitle: '-12,000 DEBIT',
                subtitleColor: AppColors.critical,
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: _buildMetricCard(
                title: 'AVAILABLE CASH',
                value: 'INR ${currencyFormat.format(state.availableCash)}',
                subtitle: '18,000 DUE 6D',
                subtitleColor: AppColors.warning,
              ),
            ),
          ],
        ),
        const SizedBox(height: 10),
        Row(
          children: [
            Expanded(
              child: _buildMetricCard(
                title: '30-DAY PROJECTED',
                value: 'INR ${currencyFormat.format(state.projectedBalance)}',
                subtitle: 'FLOOR: ${currencyFormat.format(state.minimumCashBuffer)}',
                subtitleColor: state.projectedBalance < state.minimumCashBuffer
                    ? AppColors.critical
                    : AppColors.positive,
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: _buildMetricCard(
                title: 'EMERGENCY FUND',
                value: '${state.emergencyFundMonths} MO',
                subtitle: 'INR ${currencyFormat.format(state.savings)} LIQUID',
                subtitleColor: AppColors.ashMist,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildMetricCard({
    required String title,
    required String value,
    required String subtitle,
    required Color subtitleColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              color: AppColors.ashMist,
              fontSize: 10,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.0,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: AppTypography.metricLarge,
          ),
          const SizedBox(height: 6),
          Text(
            subtitle,
            style: TextStyle(
              color: subtitleColor,
              fontSize: 11,
              fontWeight: FontWeight.w600,
              fontFamily: 'monospace',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStrategicDecisionCard(WidgetRef ref, AgentResponseModel advisor) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  advisor.recommendation.title.toUpperCase(),
                  style: const TextStyle(
                    color: AppColors.paper,
                    fontSize: 15,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 0.5,
                  ),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.obsidian,
                  borderRadius: BorderRadius.circular(75.0),
                  border: Border.all(color: AppColors.critical),
                ),
                child: Text(
                  '${advisor.recommendation.priority.toUpperCase()} PRIORITY',
                  style: const TextStyle(
                    color: AppColors.critical,
                    fontSize: 9,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.8,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          Text(
            advisor.recommendation.description,
            style: AppTypography.bodyRegular,
          ),
          const SizedBox(height: 16),
          const Divider(color: AppColors.hairline, height: 1),
          const SizedBox(height: 16),
          const Text(
            'KEY TRADEOFF EVALUATED',
            style: TextStyle(
              color: AppColors.ashMist,
              fontSize: 10,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.0,
            ),
          ),
          const SizedBox(height: 6),
          Text(
            advisor.competingObjectivesConsidered.isNotEmpty
                ? advisor.competingObjectivesConsidered.first
                : 'Liquidity preservation vs secondary goal allocation.',
            style: AppTypography.bodySecondary,
          ),
          const SizedBox(height: 20),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {
                ref.read(activeTabProvider.notifier).state = 1; // Tab 1: ADVISOR
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.paper,
                foregroundColor: AppColors.obsidian,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(75.0),
                ),
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              child: const Text(
                'OPEN AI ADVISOR',
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w800,
                  letterSpacing: 1.2,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
