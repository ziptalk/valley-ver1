MAIN_MENU = """
🌟 *메인 메뉴* 🌟

아래 버튼 중 하나를 선택하세요:

• 📚 도움말: 각 기능에 대한 자세한 설명
• 💰 포인트: 현재 포인트 현황 확인
• 📢 광고: 광고 보기 및 포인트 획득
• 🌐 언어: 언어 설정 변경
"""

HELP_MENU = """
📚 *도움말* 📚

각 기능에 대한 설명입니다:

• 💰 *포인트*
  - 현재 보유한 포인트를 확인합니다
  - 개인 채팅에서는 개인 포인트를
  - 그룹 채팅에서는 그룹 포인트를 표시합니다

• 📢 *광고*
  - 광고를 보고 포인트를 획득합니다
  - 하루에 한 번만 포인트를 획득할 수 있습니다
  - 광고는 랜덤으로 선택됩니다

• 🌐 *언어*
  - 한국어/영어 중 선택할 수 있습니다
  - 선택한 언어로 모든 메시지가 표시됩니다

• 📚 *도움말*
  - 이 메뉴를 표시합니다
  - 각 기능에 대한 자세한 설명을 제공합니다
"""

POINTS_MENU = {
    'private': """
💰 *포인트 현황* 💰

현재 보유 포인트: *{point}*
""",
    'group': """
💰 *그룹 포인트 현황* 💰

현재 그룹 포인트: *{point}*
"""
}

AD_MENU = {
    'success': """
{content}
""",
    'no_ad': "📢 현재 표시할 수 있는 광고가 없습니다.",
    'already_viewed': "ℹ️ 오늘은 이미 광고를 보셨습니다. 포인트는 하루에 한 번만 획득할 수 있습니다.",
    'points_earned': "🎉 {points} 포인트를 획득하셨습니다!"
}

LANGUAGE_MENU = """
🌐 *언어 설정* 🌐
Please select your preferred language.
언어를 선택해주세요.
"""

AD_MESSAGES = {
    'ad_error': "❌ 광고 처리 중 오류가 발생했습니다.",
    'ad_fetching_error': "❌ 광고를 불러오는 중 오류가 발생했습니다.",
    'no_ads_error': "📢 현재 표시할 수 있는 광고가 없습니다.",
    'points_error': "❌ 포인트 업데이트 중 오류가 발생했습니다.",
    'view_log_error': "❌ 광고 시청 기록 중 오류가 발생했습니다."
}

POINT_MESSAGES = {
    'points_error': "❌ 포인트 조회 중 오류가 발생했습니다."
}

LANG_MESSAGES = {
    'language_success_ko': "✅ 언어가 한국어로 변경되었습니다.",
    'language_success_en': "✅ Language has been changed to English.",
    'language_error': "❌ 언어 변경 중 오류가 발생했습니다."
}

USER_GROUP_MESSAGES = {
    'user_success_register': "✅ 사용자 등록이 완료되었습니다.",
    'user_already_exists': "ℹ️ 이미 등록된 사용자입니다.",
    'group_success_register': "✅ 그룹 등록이 완료되었습니다.",
    'group_already_exists': "ℹ️ 이미 등록된 그룹입니다.",
    'registration_error': "❌ 등록 중 오류가 발생했습니다. 다시 시도해주세요."
} 