"""
Module for managing all text messages used in the Telegram bot.
"""

# Main menu message
MAIN_MENU = """
🌟 *Valley Bot Menu* 🌟

Please select a menu:

• 📚 Help: Explains the function of each button.
• 💰 Points: Check your current points status.
• 📢 AD: View advertisements. You can earn points by viewing ads.
• 🌐 Language: Change language settings.
"""

# Help message
HELP_MENU = """
📚 *Help* 📚

Here's what each menu does:

• 💰 *Points*
  - Private chat: Check your personal points status.
  - Group chat: Check the group's points status.

• 📢 *AD*
  - Shows the latest active advertisement.
  - You can earn points by viewing ads.
  - Shows a notification if no ads are available.

• 🌐 *Language*
  - Choose between Korean and English.
  - All bot messages will be displayed in the selected language.

• 📚 *Help*
  - Shows this help message.
"""

# Points related messages
POINTS_MENU = {
    'private': """
💰 *Points Status* 💰

Current points: *{point:,}* points
""",
    'group': """
💰 *Group Points Status* 💰

Current group points: *{point:,}* points
"""
}

# Advertisement related messages
AD_MENU = {
    'success': """
{content}
""",
    'no_ad': "📢 No active advertisements available.",
    'already_viewed': "ℹ️ You've already viewed an ad today. Points can only be earned once per day.",
    'points_earned': "🎉 You've earned {points} points!"
}

# Language setting related message
LANGUAGE_MENU = """
🌐 *Language Settings* 🌐

Please select your preferred language.
언어를 선택해주세요.
"""

### Success/Failure messages

AD_MESSAGES = {
    'ad_error': "❌ Error occurred while fetching advertisement.",
    'ad_fetching_error': "❌ Error occurred while fetching advertisements.",
    'no_ads_error': "📢 No active advertisements available.",
    'points_error': "❌ Error occurred while updating points.",
    'view_log_error': "❌ Error occurred while recording advertisement view."
}

POINT_MESSAGES = {
    'points_error': "❌ Error occurred while checking points.",
}

LANG_MESSAGES = {
    'language_success_ko': "✅ 언어가 한국어로 변경되었습니다.",
    'language_success_en': "✅ Language has been changed to English.",
    'language_error': "❌ Error occurred while changing language.",
}

USER_GROUP_MESSAGES = {
    'user_success_register': "✅ User registration completed successfully.",
    'user_already_exists': "ℹ️ This user is already registered.",
    'group_success_register': "✅ Group registration completed successfully.",
    'group_already_exists': "ℹ️ This group is already registered.",
    'registration_error': "❌ An error occurred during registration. Please try again.",
}