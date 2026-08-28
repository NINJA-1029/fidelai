import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class RigidContainer extends StatelessWidget {
  final Widget child;
  final Color? color;
  final EdgeInsets? padding;
  final double? height;
  final double? width;
  final Border? border;

  const RigidContainer({
    super.key,
    required this.child,
    this.color,
    this.padding,
    this.height,
    this.width,
    this.border,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      height: height,
      padding: padding,
      decoration: BoxDecoration(
        color: color ?? AppTheme.inkstone,
        border: border ?? Border.all(color: const Color(0xFF222222), width: 1),
      ),
      child: child,
    );
  }
}

class PillBadge extends StatelessWidget {
  final String text;
  final Color? color;
  final Color? textColor;
  final IconData? icon;

  const PillBadge({
    super.key,
    required this.text,
    this.color,
    this.textColor,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
      decoration: ShapeDecoration(
        color: color?.withOpacity(0.1),
        shape: StadiumBorder(
          side: BorderSide(color: color ?? AppTheme.paper, width: 1),
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            Icon(icon, size: 12, color: color ?? AppTheme.paper),
            const SizedBox(width: 4),
          ],
          Text(
            text.toUpperCase(),
            style: Theme.of(context).textTheme.labelLarge?.copyWith(
                  color: color ?? AppTheme.paper,
                  fontSize: 10,
                ),
          ),
        ],
      ),
    );
  }
}

class DataText extends StatelessWidget {
  final String text;
  final double fontSize;
  final Color? color;
  final bool bold;

  const DataText(
    this.text, {
    super.key,
    this.fontSize = 14,
    this.color,
    this.bold = false,
  });

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      style: TextStyle(
        fontFamily: 'JetBrains Mono',
        fontSize: fontSize,
        fontWeight: bold ? FontWeight.w600 : FontWeight.w500,
        color: color ?? AppTheme.paper,
      ),
    );
  }
}

class BrutalistDivider extends StatelessWidget {
  const BrutalistDivider({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 1,
      color: const Color(0xFF222222),
    );
  }
}
