import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme/app_theme.dart';
import 'core/providers/state_providers.dart';
import 'features/dashboard/dashboard_screen.dart';
import 'features/ai_advisor/ai_advisor_screen.dart';
import 'features/transactions/transactions_screen.dart';
import 'features/goals/goals_screen.dart';
import 'features/simulation/simulation_screen.dart';

void main() {
  runApp(
    const ProviderScope(
      child: FidelApp(),
    ),
  );
}

class FidelApp extends StatelessWidget {
  const FidelApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fidel AI Financial Management',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.darkTheme,
      home: const MainShell(),
    );
  }
}

class MainShell extends ConsumerWidget {
  const MainShell({super.key});

  static const List<String> tabLabels = [
    'OVERVIEW',
    'ADVISOR',
    'LEDGER',
    'GOALS',
    'SIMULATE',
  ];

  static const List<Widget> screens = [
    DashboardScreen(),
    AiAdvisorScreen(),
    TransactionsScreen(),
    GoalsScreen(),
    SimulationScreen(),
  ];

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final activeIndex = ref.watch(activeTabProvider);

    return Scaffold(
      backgroundColor: AppColors.obsidian,
      body: IndexedStack(
        index: activeIndex,
        children: screens,
      ),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AppColors.inkstone,
          border: Border(
            top: BorderSide(color: AppColors.hairline, width: 1.0),
          ),
        ),
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
        child: SafeArea(
          top: false,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: List.generate(tabLabels.length, (index) {
              final isSelected = activeIndex == index;
              return Expanded(
                child: InkWell(
                  onTap: () {
                    ref.read(activeTabProvider.notifier).state = index;
                  },
                  splashColor: Colors.transparent,
                  highlightColor: Colors.transparent,
                  child: Container(
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    decoration: BoxDecoration(
                      border: Border(
                        bottom: BorderSide(
                          color: isSelected ? AppColors.paper : Colors.transparent,
                          width: 2.0,
                        ),
                      ),
                    ),
                    child: Center(
                      child: Text(
                        tabLabels[index],
                        style: TextStyle(
                          color: isSelected ? AppColors.paper : AppColors.feltGray,
                          fontSize: 10,
                          fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                          letterSpacing: 1.0,
                        ),
                      ),
                    ),
                  ),
                ),
              );
            }),
          ),
        ),
      ),
    );
  }
}
