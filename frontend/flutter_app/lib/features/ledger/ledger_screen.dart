import 'package:flutter/material.dart';
import '../../core/theme/app_theme.dart';
import '../../core/widgets/brutalist_widgets.dart';

class LedgerScreen extends StatelessWidget {
  const LedgerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('FIDEL', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: -1.5)),
        centerTitle: false,
        actions: [
          IconButton(onPressed: () {}, icon: const Icon(Icons.sync, color: AppTheme.paper)),
        ],
        bottom: const PreferredSize(
          preferredSize: Size.fromHeight(1),
          child: BrutalistDivider(),
        ),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Ledger Insights', style: TextStyle(fontFamily: 'Inter', fontSize: 32, fontWeight: FontWeight.bold, color: AppTheme.paper)),
                const SizedBox(height: 24),

                // Search Bar
                const TextField(
                  decoration: InputDecoration(
                    prefixIcon: Icon(Icons.search, size: 18, color: AppTheme.feltGray),
                    hintText: 'SEARCH TRANSACTIONS...',
                    hintStyle: TextStyle(fontFamily: 'JetBrains Mono', fontSize: 14, color: AppTheme.feltGray),
                  ),
                ),
                const SizedBox(height: 16),

                // Filters
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: const [
                      FilterPill(text: 'ALL', isActive: true),
                      SizedBox(width: 8),
                      FilterPill(text: 'SMS'),
                      SizedBox(width: 8),
                      FilterPill(text: 'BANK API'),
                      SizedBox(width: 8),
                      FilterPill(text: 'RECEIPTS'),
                    ],
                  ),
                ),
              ],
            ),
          ),

          // Header
          Container(
            color: AppTheme.inkstone,
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
            child: Row(
              children: const [
                Expanded(flex: 2, child: Text('DATE', style: TextStyle(fontFamily: 'JetBrains Mono', fontSize: 10, color: AppTheme.feltGray))),
                Expanded(flex: 3, child: Text('MERCHANT', style: TextStyle(fontFamily: 'JetBrains Mono', fontSize: 10, color: AppTheme.feltGray))),
                Expanded(flex: 2, child: Text('AMOUNT', style: TextStyle(fontFamily: 'JetBrains Mono', fontSize: 10, color: AppTheme.feltGray), textAlign: TextAlign.right)),
              ],
            ),
          ),

          // Transaction List
          Expanded(
            child: ListView(
              children: const [
                LedgerRow(date: '2023.10.24', merchant: 'Equinox Hudson Yards', category: 'FITNESS', amount: '-$315.00', isConfirmed: true),
                LedgerRow(date: '2023.10.23', merchant: 'Uber Technologies', category: 'TRANSPORT', amount: '-$42.80', isConfirmed: false),
                LedgerRow(date: '2023.10.23', merchant: 'Sweetgreen', category: 'DINING', amount: '-$18.45', isConfirmed: true),
                LedgerRow(date: '2023.10.21', merchant: 'Wire Transfer - Inbound', category: 'INCOME', amount: '+$15,000.00', isConfirmed: true),
                LedgerRow(date: '2023.10.20', merchant: 'Unknown Merchant 883', category: 'UNCATEGORIZED', amount: '-$99.99', isFlag: true),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class FilterPill extends StatelessWidget {
  final String text;
  final bool isActive;

  const FilterPill({super.key, required this.text, this.isActive = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 8),
      decoration: ShapeDecoration(
        color: isActive ? AppTheme.paper : Colors.transparent,
        shape: StadiumBorder(
          side: BorderSide(color: isActive ? AppTheme.paper : AppTheme.feltGray),
        ),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontFamily: 'JetBrains Mono',
          fontSize: 11,
          fontWeight: FontWeight.w600,
          color: isActive ? AppTheme.obsidian : AppTheme.paper,
        ),
      ),
    );
  }
}

class LedgerRow extends StatelessWidget {
  final String date;
  final String merchant;
  final String category;
  final String amount;
  final bool isConfirmed;
  final bool isFlag;

  const LedgerRow({
    super.key,
    required this.date,
    required this.merchant,
    required this.category,
    required this.amount,
    this.isConfirmed = false,
    this.isFlag = false,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
      decoration: const BoxDecoration(
        border: Border(bottom: BorderSide(color: Color(0xFF222222))),
      ),
      child: Row(
        children: [
          Expanded(flex: 2, child: DataText(date, fontSize: 12, color: AppTheme.feltGray)),
          Expanded(
            flex: 3,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(merchant, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
                const SizedBox(height: 4),
                PillBadge(text: category, color: AppTheme.feltGray),
              ],
            ),
          ),
          Expanded(
            flex: 2,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                DataText(amount, fontSize: 14, bold: true, color: amount.startsWith('+') ? AppTheme.success : AppTheme.paper),
                const SizedBox(height: 4),
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Container(
                      width: 6,
                      height: 6,
                      decoration: BoxDecoration(
                        color: isFlag ? AppTheme.error : (isConfirmed ? AppTheme.paper : AppTheme.feltGray),
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: 4),
                    Text(
                      isFlag ? 'FLAG' : (isConfirmed ? 'CONFIRMED' : 'ESTIMATED'),
                      style: TextStyle(fontFamily: 'JetBrains Mono', fontSize: 10, color: isFlag ? AppTheme.error : AppTheme.feltGray),
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
}
