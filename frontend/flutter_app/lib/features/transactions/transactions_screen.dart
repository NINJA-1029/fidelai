import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import '../../core/theme/app_theme.dart';
import '../../core/providers/state_providers.dart';
import '../../core/models/models.dart';

class TransactionsScreen extends ConsumerStatefulWidget {
  const TransactionsScreen({super.key});

  @override
  ConsumerState<TransactionsScreen> createState() => _TransactionsScreenState();
}

class _TransactionsScreenState extends ConsumerState<TransactionsScreen> {
  final TextEditingController _searchController = TextEditingController();
  final NumberFormat _currencyFormat = NumberFormat('#,##0.00', 'en_IN');

  final List<String> _categories = [
    'ALL',
    'INCOME',
    'HOUSING',
    'GROCERIES',
    'UNEXPECTED',
  ];

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final filteredTransactions = ref.watch(filteredTransactionsProvider);
    final selectedCategory = ref.watch(transactionCategoryFilterProvider);

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
                    'TRANSACTION LEDGER',
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
                    child: Text(
                      'COUNT: ${filteredTransactions.length}',
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
            ),

            // Search Field
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
              child: TextField(
                controller: _searchController,
                onChanged: (val) {
                  ref.read(transactionSearchQueryProvider.notifier).state = val;
                },
                style: const TextStyle(color: AppColors.paper, fontSize: 13),
                decoration: const InputDecoration(
                  hintText: 'Search by merchant, note, or tag...',
                  contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                ),
              ),
            ),
            const SizedBox(height: 10),

            // Horizontal Category Filter Pills
            SizedBox(
              height: 36,
              child: ListView.separated(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16),
                itemCount: _categories.length,
                separatorBuilder: (_, __) => const SizedBox(width: 8),
                itemBuilder: (context, index) {
                  final cat = _categories[index];
                  final isSelected = selectedCategory.toUpperCase() == cat;

                  return GestureDetector(
                    onTap: () {
                      ref.read(transactionCategoryFilterProvider.notifier).state = cat;
                    },
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: isSelected ? AppColors.paper : AppColors.inkstone,
                        borderRadius: BorderRadius.circular(75.0),
                        border: Border.all(
                          color: isSelected ? AppColors.paper : AppColors.hairline,
                        ),
                      ),
                      child: Center(
                        child: Text(
                          cat,
                          style: TextStyle(
                            color: isSelected ? AppColors.obsidian : AppColors.ashMist,
                            fontSize: 10,
                            fontWeight: FontWeight.w800,
                            letterSpacing: 0.8,
                          ),
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
            const SizedBox(height: 12),
            const Divider(color: AppColors.hairline, height: 1),

            // Transaction Cards List
            Expanded(
              child: filteredTransactions.isEmpty
                  ? const Center(
                      child: Text(
                        'No transactions match current filters.',
                        style: AppTypography.bodySecondary,
                      ),
                    )
                  : ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: filteredTransactions.length,
                      itemBuilder: (context, index) {
                        final tx = filteredTransactions[index];
                        return _buildTransactionCard(tx);
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTransactionCard(TransactionModel tx) {
    final isCredit = tx.isCredit;
    final sign = isCredit ? '+' : '-';
    final amountColor = isCredit ? AppColors.positive : AppColors.paper;
    final amountFormatted = '$sign INR ${_currencyFormat.format(tx.amount)}';

    String formattedDate = tx.timestamp;
    try {
      final parsed = DateTime.parse(tx.timestamp);
      formattedDate = DateFormat('yyyy-MM-dd HH:mm').format(parsed);
    } catch (_) {}

    return Container(
      margin: const EdgeInsets.only(bottom: 10),
      padding: const EdgeInsets.all(16),
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
              // Category Tag
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                decoration: BoxDecoration(
                  color: AppColors.obsidian,
                  borderRadius: BorderRadius.circular(75.0),
                  border: Border.all(
                    color: tx.category.toLowerCase() == 'unexpected'
                        ? AppColors.critical
                        : AppColors.slatePill,
                  ),
                ),
                child: Text(
                  tx.category.toUpperCase(),
                  style: TextStyle(
                    color: tx.category.toLowerCase() == 'unexpected'
                        ? AppColors.critical
                        : AppColors.ashMist,
                    fontSize: 8,
                    fontWeight: FontWeight.w800,
                    letterSpacing: 0.8,
                  ),
                ),
              ),
              // Timestamp
              Text(
                formattedDate,
                style: const TextStyle(
                  color: AppColors.feltGray,
                  fontSize: 10,
                  fontFamily: 'monospace',
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Text(
                  tx.description,
                  style: const TextStyle(
                    color: AppColors.paper,
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Text(
                amountFormatted,
                style: TextStyle(
                  color: amountColor,
                  fontSize: 14,
                  fontWeight: FontWeight.w700,
                  fontFamily: 'monospace',
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'SOURCE: ${tx.source.toUpperCase()}',
                style: const TextStyle(
                  color: AppColors.feltGray,
                  fontSize: 9,
                  letterSpacing: 0.5,
                ),
              ),
              Text(
                'CONFIDENCE: ${(tx.confidence * 100).toInt()}%',
                style: const TextStyle(
                  color: AppColors.feltGray,
                  fontSize: 9,
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
