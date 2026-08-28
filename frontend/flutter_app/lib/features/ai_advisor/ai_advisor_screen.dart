import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../core/providers/state_providers.dart';
import '../../core/models/models.dart';

class AiAdvisorScreen extends ConsumerStatefulWidget {
  const AiAdvisorScreen({super.key});

  @override
  ConsumerState<AiAdvisorScreen> createState() => _AiAdvisorScreenState();
}

class _AiAdvisorScreenState extends ConsumerState<AiAdvisorScreen> {
  final TextEditingController _queryController = TextEditingController();
  final NumberFormat _currencyFormat = NumberFormat('#,##0', 'en_IN');

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }

  void _handleSubmitQuery() {
    final text = _queryController.text.trim();
    if (text.isNotEmpty) {
      ref.read(aiAdvisorProvider.notifier).submitQuery(text);
      _queryController.clear();
      FocusScope.of(context).unfocus();
    }
  }

  @override
  Widget build(BuildContext context) {
    final advisorState = ref.watch(aiAdvisorProvider);
    final response = advisorState.response;

    return Scaffold(
      backgroundColor: AppColors.obsidian,
      body: SafeArea(
        child: Column(
          children: [
            // Top App Bar
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'AI ADVISOR',
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
                      'CONFIDENCE: ${(response.confidence * 100).toInt()}%',
                      style: const TextStyle(
                        color: AppColors.positive,
                        fontSize: 9,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 0.8,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const Divider(color: AppColors.hairline, height: 1),

            // Scrollable Content
            Expanded(
              child: advisorState.isLoading
                  ? const Center(
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          CircularProgressIndicator(
                            color: AppColors.paper,
                            strokeWidth: 2,
                          ),
                          SizedBox(height: 16),
                          Text(
                            'REASONING OVER FINANCIAL GRAPH...',
                            style: TextStyle(
                              color: AppColors.ashMist,
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                              letterSpacing: 1.0,
                            ),
                          ),
                        ],
                      ),
                    )
                  : SingleChildScrollView(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.stretch,
                        children: [
                          // 1. Primary Recommendation Card
                          _buildRecommendationCard(response),
                          const SizedBox(height: 20),

                          // Section: 4-Card Evidence Matrix Grid
                          const Text(
                            'DETERMINISTIC EVIDENCE MATRIX',
                            style: AppTypography.cardHeader,
                          ),
                          const SizedBox(height: 10),
                          _buildEvidenceMatrixGrid(response),
                          const SizedBox(height: 20),

                          // Section: Evaluated Tradeoffs
                          const Text(
                            'EVALUATED MULTI-OBJECTIVE TRADEOFFS',
                            style: AppTypography.cardHeader,
                          ),
                          const SizedBox(height: 10),
                          _buildTradeoffsCard(response),
                          const SizedBox(height: 20),

                          // Section: Actionable Alternatives
                          const Text(
                            'ACTIONABLE ALTERNATIVES',
                            style: AppTypography.cardHeader,
                          ),
                          const SizedBox(height: 10),
                          _buildAlternativesList(response),
                          const SizedBox(height: 20),
                        ],
                      ),
                    ),
            ),

            // 5. Bottom Query Input Bar
            _buildBottomQueryBar(advisorState.isLoading),
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendationCard(AgentResponseModel response) {
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
                  response.recommendation.title.toUpperCase(),
                  style: const TextStyle(
                    color: AppColors.paper,
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
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
                    color: response.recommendation.priority == 'high'
                        ? AppColors.critical
                        : AppColors.warning,
                  ),
                ),
                child: Text(
                  '${response.recommendation.priority.toUpperCase()} PRIORITY',
                  style: TextStyle(
                    color: response.recommendation.priority == 'high'
                        ? AppColors.critical
                        : AppColors.warning,
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
            response.recommendation.description,
            style: AppTypography.bodyRegular,
          ),
          const SizedBox(height: 14),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.obsidian,
              border: Border.all(color: AppColors.hairline),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'CORE CAUSAL REASONING',
                  style: TextStyle(
                    color: AppColors.ashMist,
                    fontSize: 9,
                    fontWeight: FontWeight.w700,
                    letterSpacing: 1.0,
                  ),
                ),
                const SizedBox(height: 6),
                Text(
                  response.reason,
                  style: AppTypography.bodySecondary,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEvidenceMatrixGrid(AgentResponseModel response) {
    if (response.evidence.isEmpty) {
      return Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.inkstone,
          border: Border.all(color: AppColors.hairline),
        ),
        child: const Text(
          'No evidence items compiled.',
          style: AppTypography.bodySecondary,
        ),
      );
    }

    final items = response.evidence.take(4).toList();

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
        childAspectRatio: 1.15,
      ),
      itemCount: items.length,
      itemBuilder: (context, index) {
        final ev = items[index];
        final title = ev.metric.replaceAll('_', ' ').toUpperCase();
        final valueStr = 'INR ${_currencyFormat.format(ev.value)}';

        return Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.inkstone,
            border: Border.all(color: AppColors.hairline),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Text(
                      title,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        color: AppColors.ashMist,
                        fontSize: 9,
                        fontWeight: FontWeight.w700,
                        letterSpacing: 0.8,
                      ),
                    ),
                  ),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                    decoration: BoxDecoration(
                      color: AppColors.obsidian,
                      borderRadius: BorderRadius.circular(75.0),
                      border: Border.all(color: AppColors.hairline),
                    ),
                    child: Text(
                      ev.status.toUpperCase(),
                      style: const TextStyle(
                        color: AppColors.paper,
                        fontSize: 7,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                ],
              ),
              Text(
                valueStr,
                style: const TextStyle(
                  color: AppColors.paper,
                  fontSize: 15,
                  fontWeight: FontWeight.w700,
                  fontFamily: 'monospace',
                ),
              ),
              Text(
                ev.description,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: AppColors.feltGray,
                  fontSize: 10,
                  height: 1.2,
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildTradeoffsCard(AgentResponseModel response) {
    final tradeoffs = response.competingObjectivesConsidered;
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: AppColors.inkstone,
        border: Border.all(color: AppColors.hairline),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: tradeoffs.map((t) {
          return Padding(
            padding: const EdgeInsets.only(bottom: 10.0),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Padding(
                  padding: EdgeInsets.only(top: 5.0, right: 10.0),
                  child: Text(
                    '—',
                    style: TextStyle(color: AppColors.ashMist, fontWeight: FontWeight.w700),
                  ),
                ),
                Expanded(
                  child: Text(
                    t,
                    style: AppTypography.bodyRegular,
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ),
    );
  }

  Widget _buildAlternativesList(AgentResponseModel response) {
    final alts = response.alternatives;
    return Column(
      children: alts.map((alt) {
        return Container(
          margin: const EdgeInsets.only(bottom: 10),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: AppColors.inkstone,
            border: Border.all(color: AppColors.hairline),
          ),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(
                child: Text(
                  alt,
                  style: AppTypography.bodyRegular,
                ),
              ),
              const SizedBox(width: 12),
              OutlinedButton(
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      backgroundColor: AppColors.inkstone,
                      content: Text(
                        'Alternative selected: ${alt.substring(0, alt.length > 40 ? 40 : alt.length)}...',
                        style: const TextStyle(color: AppColors.paper),
                      ),
                    ),
                  );
                },
                style: OutlinedButton.styleFrom(
                  foregroundColor: AppColors.paper,
                  side: const BorderSide(color: AppColors.paper, width: 1.0),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(75.0),
                  ),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                ),
                child: const Text(
                  'SELECT',
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 1.0,
                  ),
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildBottomQueryBar(bool isLoading) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: const BoxDecoration(
        color: AppColors.inkstone,
        border: Border(
          top: BorderSide(color: AppColors.hairline, width: 1.0),
        ),
      ),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _queryController,
              enabled: !isLoading,
              textInputAction: TextInputAction.send,
              onSubmitted: (_) => _handleSubmitQuery(),
              style: const TextStyle(color: AppColors.paper, fontSize: 13),
              decoration: const InputDecoration(
                hintText: 'Ask financial advisor (e.g. Can I buy a phone for 20k?)',
                contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              ),
            ),
          ),
          const SizedBox(width: 10),
          ElevatedButton(
            onPressed: isLoading ? null : _handleSubmitQuery,
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.paper,
              foregroundColor: AppColors.obsidian,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(75.0),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
            ),
            child: const Text(
              'ASK',
              style: TextStyle(
                fontSize: 11,
                fontWeight: FontWeight.w800,
                letterSpacing: 1.0,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
