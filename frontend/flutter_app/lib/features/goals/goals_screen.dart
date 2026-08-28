import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../core/network/api_client.dart';
import '../../core/providers/state_providers.dart';
import '../../core/models/models.dart';

class GoalsScreen extends ConsumerWidget {
  const GoalsScreen({super.key});

  static final NumberFormat _currencyFormat = NumberFormat('#,##0', 'en_IN');

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final stateAsync = ref.watch(financialStateProvider);
    final state = stateAsync.value ?? ApiClient.fallbackFinancialState;
    final goals = state.financialGoals;

    return Scaffold(
      backgroundColor: AppColors.obsidian,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Top App Bar Branding
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'GOAL PACING',
                    style: TextStyle(
                      color: AppColors.paper,
                      fontSize: 18,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 2.5,
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.inkstone,
                      borderRadius: BorderRadius.circular(75.0),
                      border: Border.all(color: AppColors.hairline),
                    ),
                    child: Text(
                      'ACTIVE: ${goals.length}',
                      style: const TextStyle(
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

              // Overview Banner Card
              Container(
                padding: const EdgeInsets.all(18),
                decoration: BoxDecoration(
                  color: AppColors.inkstone,
                  border: Border.all(color: AppColors.hairline),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'MONTHLY SAVINGS TARGET',
                      style: AppTypography.cardHeader,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'INR ${_currencyFormat.format(goals.fold<double>(0.0, (acc, g) => acc + g.monthlyContributionRequired))}',
                      style: AppTypography.metricLarge,
                    ),
                    const SizedBox(height: 6),
                    const Text(
                      'Aggregated monthly capital required to meet all deterministic goal horizons.',
                      style: AppTypography.bodySecondary,
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Section Header: Active Goals
              const Text(
                'TARGET PACING ALLOCATION',
                style: AppTypography.cardHeader,
              ),
              const SizedBox(height: 10),

              // Goals List
              ...goals.map((goal) => _buildGoalCard(goal)),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildGoalCard(GoalModel goal) {
    final isOnTrack = goal.status.toLowerCase() == 'on_track';
    final progress = goal.progress;
    final percent = goal.progressPercent;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Title and Status Badge
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  goal.title.toUpperCase(),
                  style: const TextStyle(
                    color: AppColors.paper,
                    fontSize: 14,
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
                  border: Border.all(
                    color: isOnTrack ? AppColors.positive : AppColors.warning,
                  ),
                ),
                child: Text(
                  goal.status.replaceAll('_', ' ').toUpperCase(),
                  style: TextStyle(
                    color: isOnTrack ? AppColors.positive : AppColors.warning,
                    fontSize: 8,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.8,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),

          // Amounts and Percent
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'ACCUMULATED / TARGET',
                    style: TextStyle(
                      color: AppColors.ashMist,
                      fontSize: 9,
                      fontWeight: FontWeight.w700,
                      letterSpacing: 0.8,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'INR ${_currencyFormat.format(goal.currentAmount)} / ${_currencyFormat.format(goal.targetAmount)}',
                    style: const TextStyle(
                      color: AppColors.paper,
                      fontSize: 15,
                      fontWeight: FontWeight.w700,
                      fontFamily: 'monospace',
                    ),
                  ),
                ],
              ),
              Text(
                '$percent%',
                style: const TextStyle(
                  color: AppColors.paper,
                  fontSize: 18,
                  fontWeight: FontWeight.w800,
                  fontFamily: 'monospace',
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Binary Monochrome LinearProgressIndicator (0px radius)
          ClipRRect(
            borderRadius: BorderRadius.zero,
            child: LinearProgressIndicator(
              value: progress,
              minHeight: 6,
              backgroundColor: AppColors.obsidian,
              valueColor: const AlwaysStoppedAnimation<Color>(AppColors.paper),
            ),
          ),
          const SizedBox(height: 14),

          // Monthly Pacing Requirement and Deadline
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'PACING: INR ${_currencyFormat.format(goal.monthlyContributionRequired)}/MO',
                style: const TextStyle(
                  color: AppColors.ashMist,
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                  fontFamily: 'monospace',
                ),
              ),
              Text(
                'TARGET: ${goal.targetDate}',
                style: const TextStyle(
                  color: AppColors.feltGray,
                  fontSize: 10,
                  fontFamily: 'monospace',
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
