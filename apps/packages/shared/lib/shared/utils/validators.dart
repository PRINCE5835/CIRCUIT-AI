class Validators {
  Validators._();

  static String? email(String? value) {
    if (value == null || value.isEmpty) return 'Email is required';
    final regex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!regex.hasMatch(value)) return 'Enter a valid email address';
    return null;
  }

  static String? password(String? value) {
    if (value == null || value.isEmpty) return 'Password is required';
    if (value.length < 8) return 'Password must be at least 8 characters';
    if (!value.contains(RegExp(r'[A-Z]'))) return 'Password must contain an uppercase letter';
    if (!value.contains(RegExp(r'[0-9]'))) return 'Password must contain a number';
    return null;
  }

  static String? confirmPassword(String? value, String password) {
    if (value == null || value.isEmpty) return 'Please confirm your password';
    if (value != password) return 'Passwords do not match';
    return null;
  }

  static String? required(String? value) {
    if (value == null || value.trim().isEmpty) return 'This field is required';
    return null;
  }

  static String? phone(String? value) {
    if (value == null || value.isEmpty) return null;
    final regex = RegExp(r'^\+?[\d\s-]{10,15}$');
    if (!regex.hasMatch(value)) return 'Enter a valid phone number';
    return null;
  }

  static String? number(String? value) {
    if (value == null || value.isEmpty) return null;
    if (double.tryParse(value) == null) return 'Enter a valid number';
    return null;
  }

  static String? positiveNumber(String? value) {
    if (value == null || value.isEmpty) return null;
    final num = double.tryParse(value);
    if (num == null) return 'Enter a valid number';
    if (num <= 0) return 'Number must be positive';
    return null;
  }

  static String? url(String? value) {
    if (value == null || value.isEmpty) return null;
    final regex = RegExp(r'^https?:\/\/.+');
    if (!regex.hasMatch(value)) return 'Enter a valid URL';
    return null;
  }
}
