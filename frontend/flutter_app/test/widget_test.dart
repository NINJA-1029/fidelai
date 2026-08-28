import 'package:flutter_test/flutter_test.dart';
import 'package:fidel_app/main.dart';

void main() {
  testWidgets('Fidel app boots with Overview header', (WidgetTester tester) async {
    await tester.pumpWidget(const FidelApp());
    expect(find.textContaining('FIDEL'), findsWidgets);
  });
}
