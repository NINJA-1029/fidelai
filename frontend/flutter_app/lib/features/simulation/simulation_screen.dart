import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../core/providers/state_providers.dart';
import '../../core/models/models.dart';

class SimulationScreen extends ConsumerStatefulWidget {
  const SimulationScreen({super.key});

  @override
  ConsumerState<SimulationScreen> createState() => _SimulationScreenState();
}

class _SimulationScreenState extends ConsumerState<SimulationScreen> {
  final TextEditingController _amountController = TextEditingController(text: '12000');
  final NumberFormat _currencyFormat = NumberFormat('#,##0', 'en_IN');

  @override
  void dispose() {
    _amountController.dispose();
    super.dispose();
  }

  void _handleCalculate() {
    final text = _amountController.text.trim();
    final amount = double.tryParse(text) ?? 12000.0;
    ref.read(simulationProvider.notifier).calculateTrajectory(amount);
    FocusScope.of(context).unfocus();
  }

  @override
  Widget build(BuildContext context) {
    final simState = ref.watch(simulationProvider);
    final result = simState.result;

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
                    'WHAT-IF SIMULATION',
                    style: TextStyle(
                      color: AppColors.paper,
                      fontSize: 18,
                      fontWeight: FontWeight.w800,
                      letterSpacing: 2.0,
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
                      'SCENARIO ENGINE',
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

              // 1. Shock Parameter Card
              _buildParameterCard(simState.isLoading),
              const SizedBox(height: 20),

              // Section Header: Impact Projection
              const Text(
                'PROJECTED IMPACT ON TRAJECTORY',
                style: AppTypography.cardHeader,
              ),
              const SizedBox(height: 10),

              // 2. Projected Impact Output Card
              _buildImpactCard(result),
              const SizedBox(height: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildParameterCard(bool isLoading) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'SIMULATE UNEXPECTED EXPENSE',
            style: TextStyle(
              color: AppColors.paper,
              fontSize: 14,
              fontWeight: FontWeight.w700,
              letterSpacing: 0.5,
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Model the deterministic impact of an immediate capital outflow against your 30-day liquidity floor.',
            style: AppTypography.bodySecondary,
          ),
          const SizedBox(height: 16),
          const Text(
            'EXPENSE OUTFLOW AMOUNT (INR)',
            style: TextStyle(
              color: AppColors.ashMist,
              fontSize: 10,
              fontWeight: FontWeight.w700,
              letterSpacing: 0.8,
            ),
          ),
          const SizedBox(height: 6),
          TextField(
            controller: _amountController,
            keyboardType: TextInputType.number,
            style: const TextStyle(
              color: AppColors.paper,
              fontSize: 16,
              fontWeight: FontWeight.w700,
              fontFamily: 'monospace',
            ),
            decoration: const InputDecoration(
              hintText: 'e.g. 12000',
              prefixText: 'INR ',
              prefixStyle: TextStyle(
                color: AppColors.ashMist,
                fontSize: 16,
                fontWeight: FontWeight.w700,
                fontFamily: 'monospace',
              ),
            ),
          ),
          const SizedBox(height: 18),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: isLoading ? null : _handleCalculate,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.paper,
                foregroundColor: AppColors.obsidian,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(75.0),
                ),
                padding: const EdgeInsets.symmetric(vertical: 14),
              ),
              child: Text(
                isLoading ? 'CALCULATING...' : 'CALCULATE TRAJECTORY',
                style: const TextStyle(
                  fontSize: 11,
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

  Widget _buildImpactCard(SimulationResultModel result) {
    final isViolation = result.bufferViolationRisk;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header Row with Status Badge
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text(
                'LIQUIDITY COMPARISON',
                style: TextStyle(
                  color: AppColors.ashMist,
                  fontSize: 11,
                  fontWeight: FontWeight.w700,
                  letterSpacing: 1.0,
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: AppColors.obsidian,
                  borderRadius: BorderRadius.circular(75.0),
                  border: Border.all(
                    color: isViolation ? AppColors.critical : AppColors.positive,
                  ),
                ),
                child: Text(
                  isViolation ? 'BUFFER VIOLATION' : 'BUFFER PRESERVED',
                  style: TextStyle(
                    color: isViolation ? AppColors.critical : AppColors.positive,
                    fontSize: 8,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.8,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Side-by-Side Comparison Metrics
          Row(
            children: [
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.obsidian,
                    border: Border.all(color: AppColors.hairline),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'BASELINE (30-DAY)',
                        style: TextStyle(
                          color: AppColors.ashMist,
                          fontSize: 9,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 0.8,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'INR ${_currencyFormat.format(result.baselineProjectedBalance)}',
                        style: const TextStyle(
                          color: AppColors.paper,
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                          fontFamily: 'monospace',
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.obsidian,
                    border: Border.all(
                      color: isViolation ? AppColors.critical : AppColors.hairline,
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'SIMULATED (POST-SHOCK)',
                        style: TextStyle(
                          color: AppColors.ashMist,
                          fontSize: 9,
                          fontWeight: FontWeight.w700,
                          letterSpacing: 0.8,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        'INR ${_currencyFormat.format(result.simulatedProjectedBalance)}',
                        style: TextStyle(
                          color: isViolation ? AppColors.critical : AppColors.paper,
                          fontSize: 16,
                          fontWeight: FontWeight.w700,
                          fontFamily: 'monospace',
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),

          // Narrative Impact Summary
          Text(
            result.impactSummary,
            style: AppTypography.bodyRegular,
          ),
          const SizedBox(height: 14),

          // Recommendation & Goal Impacts
          if (result.goalImpacts.isNotEmpty) ...[
            const Divider(color: AppColors.hairline, height: 1),
            const SizedBox(height: 14),
            const Text(
              'GOAL CASCADE IMPACT',
              style: TextStyle(
                color: AppColors.ashMist,
                fontSize: 10,
                fontWeight: FontWeight.w700,
                letterSpacing: 0.8,
              ),
            ),
            const SizedBox(height: 8),
            ...result.goalImpacts.map((g) => Padding(
                  padding: const EdgeInsets.only(bottom: 6.0),
                  child: Text(
                    '— ${g.title}: ${g.impact}',
                    style: AppTypography.bodySecondary,
                  ),
                )),
          ],
          const SizedBox(height: 10),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.obsidian,
              border: Border.all(color: AppColors.hairline),
            ),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'ACTION: ',
                  style: TextStyle(
                    color: AppColors.ashMist,
                    fontSize: 10,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 0.8,
                  ),
                ),
                Expanded(
                  child: Text(
                    result.recommendation,
                    style: const TextStyle(
                      color: AppColors.paper,
                      fontSize: 11,
                      fontWeight: FontWeight.w500,
                      height: 1.3,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
