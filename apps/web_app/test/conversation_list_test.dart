import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:breadboard_web/widgets/conversation_list.dart';

Widget wrapApp(Widget child) {
  return ProviderScope(
    child: MaterialApp(
      home: Scaffold(
        body: SizedBox(width: 400, height: 600, child: child),
      ),
    ),
  );
}

void main() {
  group('ConversationList', () {
    testWidgets('shows loading state', (tester) async {
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: const AsyncValue.loading(),
          selectedId: null,
          onSelect: (_) {},
          onNewChat: () {},
          onSearch: (_) {},
        ),
      ));
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows empty state when no conversations', (tester) async {
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: const AsyncValue.data([]),
          selectedId: null,
          onSelect: (_) {},
          onNewChat: () {},
          onSearch: (_) {},
        ),
      ));
      expect(find.text('History'), findsOneWidget);
      expect(find.text('No conversations yet'), findsOneWidget);
    });

    testWidgets('shows list of conversations', (tester) async {
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: AsyncValue.data([
            {'id': 1, 'title': 'Chat One', 'message_count': 3, 'updated_at': '2024-01-15T10:00:00Z'},
            {'id': 2, 'title': 'Chat Two', 'message_count': 5, 'updated_at': '2024-01-16T12:00:00Z'},
          ]),
          selectedId: null,
          onSelect: (_) {},
          onNewChat: () {},
          onSearch: (_) {},
        ),
      ));
      expect(find.text('Chat One'), findsOneWidget);
      expect(find.text('Chat Two'), findsOneWidget);
      expect(find.text('3 msgs'), findsOneWidget);
      expect(find.text('5 msgs'), findsOneWidget);
    });

    testWidgets('highlights selected conversation', (tester) async {
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: AsyncValue.data([
            {'id': 1, 'title': 'Selected', 'message_count': 2, 'updated_at': '2024-01-15T10:00:00Z'},
            {'id': 2, 'title': 'Other', 'message_count': 0, 'updated_at': ''},
          ]),
          selectedId: 1,
          onSelect: (_) {},
          onNewChat: () {},
          onSearch: (_) {},
        ),
      ));
      expect(find.text('Selected'), findsOneWidget);
      expect(find.text('Other'), findsOneWidget);
    });

    testWidgets('calls onSelect when tapping a conversation', (tester) async {
      int? selectedId;
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: AsyncValue.data([
            {'id': 42, 'title': 'Tap Me', 'message_count': 1, 'updated_at': ''},
          ]),
          selectedId: null,
          onSelect: (id) => selectedId = id,
          onNewChat: () {},
          onSearch: (_) {},
        ),
      ));
      await tester.tap(find.text('Tap Me'));
      expect(selectedId, 42);
    });

    testWidgets('calls onNewChat when tapping New button', (tester) async {
      bool newChatClicked = false;
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: const AsyncValue.data([]),
          selectedId: null,
          onSelect: (_) {},
          onNewChat: () => newChatClicked = true,
          onSearch: (_) {},
        ),
      ));
      await tester.tap(find.text('New'));
      expect(newChatClicked, isTrue);
    });

    testWidgets('shows search field when search icon toggled', (tester) async {
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: const AsyncValue.data([]),
          selectedId: null,
          onSelect: (_) {},
          onNewChat: () {},
          onSearch: (_) {},
        ),
      ));
      // Initially no search field
      expect(find.byType(TextField), findsNothing);
      // Tap search icon
      await tester.tap(find.byIcon(Icons.search));
      await tester.pump();
      // Now search field should appear
      expect(find.byType(TextField), findsOneWidget);
    });

    testWidgets('search filters conversations via onSearch', (tester) async {
      String? searchQuery;
      await tester.pumpWidget(wrapApp(
        ConversationList(
          conversations: const AsyncValue.data([]),
          selectedId: null,
          onSelect: (_) {},
          onNewChat: () {},
          onSearch: (q) => searchQuery = q,
        ),
      ));
      await tester.tap(find.byIcon(Icons.search));
      await tester.pump();
      await tester.enterText(find.byType(TextField), 'arduino');
      expect(searchQuery, 'arduino');
    });
  });
}
