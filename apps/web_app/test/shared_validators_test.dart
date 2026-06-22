import 'package:flutter_test/flutter_test.dart';
import 'package:breadboard_shared/breadboard_shared.dart';

void main() {
  group('Validators.email', () {
    test('returns error for null', () {
      expect(Validators.email(null), isNotEmpty);
    });

    test('returns error for empty', () {
      expect(Validators.email(''), isNotEmpty);
    });

    test('returns null for valid email', () {
      expect(Validators.email('test@example.com'), isNull);
    });

    test('returns error for invalid email', () {
      expect(Validators.email('not-an-email'), isNotEmpty);
    });

    test('handles subdomain emails', () {
      expect(Validators.email('user@sub.example.co.uk'), isNull);
    });
  });

  group('Validators.password', () {
    test('returns error for null', () {
      expect(Validators.password(null), isNotEmpty);
    });

    test('returns error for too short', () {
      expect(Validators.password('Ab1'), isNotEmpty);
    });

    test('returns error when missing uppercase', () {
      expect(Validators.password('abcdefgh1'), isNotEmpty);
    });

    test('returns error when missing number', () {
      expect(Validators.password('Abcdefgh!'), isNotEmpty);
    });

    test('returns null for valid password', () {
      expect(Validators.password('SecurePass123'), isNull);
    });
  });

  group('Validators.confirmPassword', () {
    test('returns error for null', () {
      expect(Validators.confirmPassword(null, 'pass'), isNotEmpty);
    });

    test('returns error when mismatch', () {
      expect(Validators.confirmPassword('abc', 'xyz'), isNotEmpty);
    });

    test('returns null when match', () {
      expect(Validators.confirmPassword('pass', 'pass'), isNull);
    });
  });

  group('Validators.required', () {
    test('returns error for null', () {
      expect(Validators.required(null), isNotEmpty);
    });

    test('returns error for whitespace only', () {
      expect(Validators.required('   '), isNotEmpty);
    });

    test('returns null for non-empty', () {
      expect(Validators.required('hello'), isNull);
    });
  });

  group('Validators.phone', () {
    test('returns null for null', () {
      expect(Validators.phone(null), isNull);
    });

    test('returns null for valid phone', () {
      expect(Validators.phone('+1234567890'), isNull);
    });

    test('returns error for invalid phone', () {
      expect(Validators.phone('abc'), isNotEmpty);
    });
  });

  group('Validators.number', () {
    test('returns null for null', () {
      expect(Validators.number(null), isNull);
    });

    test('returns null for valid number', () {
      expect(Validators.number('42.5'), isNull);
    });

    test('returns error for non-numeric', () {
      expect(Validators.number('not_a_number'), isNotEmpty);
    });
  });

  group('Validators.positiveNumber', () {
    test('returns error for zero', () {
      expect(Validators.positiveNumber('0'), isNotEmpty);
    });

    test('returns error for negative', () {
      expect(Validators.positiveNumber('-5'), isNotEmpty);
    });

    test('returns null for positive', () {
      expect(Validators.positiveNumber('10'), isNull);
    });
  });

  group('Validators.url', () {
    test('returns null for null', () {
      expect(Validators.url(null), isNull);
    });

    test('returns null for valid http url', () {
      expect(Validators.url('http://example.com'), isNull);
    });

    test('returns null for valid https url', () {
      expect(Validators.url('https://example.com/path'), isNull);
    });

    test('returns error for invalid url', () {
      expect(Validators.url('not-a-url'), isNotEmpty);
    });
  });
}
