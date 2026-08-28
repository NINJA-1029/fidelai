import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fidel_app/main.dart';
import 'package:fidel_app/features/transactions/transactions_screen.dart';
import 'package:fidel_app/core/providers/state_providers.dart';

void main() {
  group('Transactions Ledger Screen (HW-004) Tests', () {
    testWidgets('Renders TransactionsScreen with search bar, pills, and initial count',
        (WidgetTester tester) async {
      tester.view.physicalSize = const Size(800, 1200);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);

      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: TransactionsScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Verify Header and Count
      expect(find.text('TRANSACTION LEDGER'), findsOneWidget);
      expect(find.text('COUNT: 5'), findsOneWidget);

      // Verify Search Field
      expect(find.byType(TextField), findsOneWidget);
      expect(find.text('Search by merchant, note, or tag...'), findsOneWidget);

      // Verify Filter Pills
      expect(find.text('ALL'), findsOneWidget);
      expect(find.text('INCOME'), findsWidgets);
      expect(find.text('HOUSING'), findsWidgets);
      expect(find.text('GROCERIES'), findsWidgets);
      expect(find.text('UNEXPECTED'), findsWidgets);

      // Verify initial list of transactions
      expect(find.text('Monthly Salary - Tech Corp'), findsOneWidget);
      expect(find.text('+ INR 65,000.00'), findsOneWidget);
      expect(find.text('Apartment Monthly Rent'), findsOneWidget);
      expect(find.text('- INR 22,000.00'), findsOneWidget);
      expect(find.text('Urgent Medical Treatment & Diagnostics'), findsOneWidget);
      expect(find.text('- INR 12,000.00'), findsOneWidget);
    });

    testWidgets('Filtering by category pill updates ledger count and list instantaneously',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: TransactionsScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Tap on HOUSING pill
      await tester.tap(find.text('HOUSING').first);
      await tester.pumpAndSettle();

      // Verify only housing item is shown
      expect(find.text('COUNT: 1'), findsOneWidget);
      expect(find.text('Apartment Monthly Rent'), findsOneWidget);
      expect(find.text('Monthly Salary - Tech Corp'), findsNothing);
      expect(find.text('Urgent Medical Treatment & Diagnostics'), findsNothing);

      // Tap on UNEXPECTED pill
      await tester.tap(find.text('UNEXPECTED').first);
      await tester.pumpAndSettle();

      expect(find.text('COUNT: 1'), findsOneWidget);
      expect(find.text('Urgent Medical Treatment & Diagnostics'), findsOneWidget);
      expect(find.text('Apartment Monthly Rent'), findsNothing);

      // Tap back to ALL
      await tester.tap(find.text('ALL').first);
      await tester.pumpAndSettle();

      expect(find.text('COUNT: 5'), findsOneWidget);
    });

    testWidgets('Searching updates list and displays empty message when no match is found',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const ProviderScope(
          child: MaterialApp(
            home: TransactionsScreen(),
          ),
        ),
      );
      await tester.pumpAndSettle();

      // Enter search query matching single merchant
      await tester.enterText(find.byType(TextField), 'Tech Corp');
      await tester.pumpAndSettle();

      expect(find.text('COUNT: 1'), findsOneWidget);
      expect(find.text('Monthly Salary - Tech Corp'), findsOneWidget);
      expect(find.text('Apartment Monthly Rent'), findsNothing);

      // Enter search query matching no items
      await tester.enterText(find.byType(TextField), 'NonExistentItemXYZ');
      await tester.pumpAndSettle();

      expect(find.text('COUNT: 0'), findsOneWidget);
      expect(find.text('No transactions match current filters.'), findsOneWidget);

      // Clear search query
      await tester.enterText(find.byType(TextField), '');
      await tester.pumpAndSettle();

      expect(find.text('COUNT: 5'), findsOneWidget);
      expect(find.text('Monthly Salary - Tech Corp'), findsOneWidget);
    });
  });
}
