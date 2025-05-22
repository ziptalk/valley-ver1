import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from psycopg2.extras import RealDictCursor
from model.database import DatabaseConnection
from messages.ko_texts import (
    MAIN_MENU as KO_MAIN_MENU,
    HELP_MENU as KO_HELP_MENU,
    POINTS_MENU as KO_POINTS_MENU,
    AD_MENU as KO_AD_MENU,
    LANGUAGE_MENU as KO_LANGUAGE_MENU,
    AD_MESSAGES as KO_AD_MESSAGES,
    POINT_MESSAGES as KO_POINT_MESSAGES,
    CLAIM_VAL_MENU as KO_CLAIM_VAL_MENU,
    LANG_MESSAGES as KO_LANG_MESSAGES,
    USER_GROUP_MESSAGES as KO_USER_GROUP_MESSAGES,
)
from messages.en_texts import (
    MAIN_MENU as EN_MAIN_MENU,
    HELP_MENU as EN_HELP_MENU,
    POINTS_MENU as EN_POINTS_MENU,
    AD_MENU as EN_AD_MENU,
    LANGUAGE_MENU as EN_LANGUAGE_MENU,
    AD_MESSAGES as EN_AD_MESSAGES,
    POINT_MESSAGES as EN_POINT_MESSAGES,
    CLAIM_VAL_MENU as EN_CLAIM_VAL_MENU,
    LANG_MESSAGES as EN_LANG_MESSAGES,
    USER_GROUP_MESSAGES as EN_USER_GROUP_MESSAGES
)

VAL_UNIT = 10

class ButtonHandlers:
    """
    Handles all button interactions and command responses for the Telegram bot.
    This class manages user interactions including registration, points checking,
    advertisement viewing, and language settings.
    """

    def __init__(self):
        """Initialize the ButtonHandlers with a database connection."""
        self.db = DatabaseConnection()
        self.texts = {
            'ko': {
                'MAIN_MENU': KO_MAIN_MENU,
                'HELP_MENU': KO_HELP_MENU,
                'POINTS_MENU': KO_POINTS_MENU,
                'AD_MENU': KO_AD_MENU,
                'LANGUAGE_MENU': KO_LANGUAGE_MENU,
                'AD_MESSAGES': KO_AD_MESSAGES,
                'POINT_MESSAGES': KO_POINT_MESSAGES,
                'LANG_MESSAGES': KO_LANG_MESSAGES,
                'USER_GROUP_MESSAGES': KO_USER_GROUP_MESSAGES
            },
            'en': {
                'MAIN_MENU': EN_MAIN_MENU,
                'HELP_MENU': EN_HELP_MENU,
                'POINTS_MENU': EN_POINTS_MENU,
                'AD_MENU': EN_AD_MENU,
                'LANGUAGE_MENU': EN_LANGUAGE_MENU,
                'AD_MESSAGES': EN_AD_MESSAGES,
                'POINT_MESSAGES': EN_POINT_MESSAGES,
                'LANG_MESSAGES': EN_LANG_MESSAGES,
                'USER_GROUP_MESSAGES': EN_USER_GROUP_MESSAGES
            }
        }
        # 채팅별 언어 설정을 저장하는 딕셔너리
        self.language_cache = {}

    def get_chat_key(self, chat_type: str, chat_id: int) -> str:
        """
        Creates a unique identifier for a chat.
        
        Args:
            chat_type (str): Type of chat ('private' or 'group')
            chat_id (int): ID of the chat
            
        Returns:
            str: Unique chat identifier
        """
        return f"{chat_type}_{chat_id}"

    async def set_language(self, chat_type: str, chat_id: int, language: str):
        """
        Updates the language setting for a chat in both database and cache.
        
        Args:
            chat_type (str): Type of chat ('private' or 'group')
            chat_id (int): ID of the chat
            language (str): Language code ('ko' or 'en')
        """
        try:
            with self.db.get_cursor() as cur:
                if chat_type == 'private':
                    cur.execute("""
                        UPDATE users 
                        SET language = %s 
                        WHERE user_id = %s
                    """, (language, chat_id))
                else:
                    cur.execute("""
                        UPDATE groups 
                        SET language = %s 
                        WHERE group_id = %s
                    """, (language, chat_id))
                
                # Update cache
                chat_key = self.get_chat_key(chat_type, chat_id)
                self.language_cache[chat_key] = language
        except Exception as e:
            logging.error(f"Error in set_language: {e}")

    def get_text(self, chat_type: str, chat_id: int, text_type: str) -> str:
        """
        Gets the appropriate text based on cached language setting.
        If not in cache, retrieves from database and updates cache.
        
        Args:
            chat_type (str): Type of chat ('private' or 'group')
            chat_id (int): ID of the chat
            text_type (str): Type of text to retrieve
            
        Returns:
            str: Text in the appropriate language
        """
        chat_key = self.get_chat_key(chat_type, chat_id)
        
        # Try to get language from cache first
        lang = self.language_cache.get(chat_key)
        
        # If not in cache, get from database and update cache
        if lang is None:
            try:
                with self.db.get_cursor() as cur:
                    if chat_type == 'private':
                        cur.execute("""
                            SELECT language 
                            FROM users 
                            WHERE user_id = %s
                        """, (chat_id,))
                    else:
                        cur.execute("""
                            SELECT language 
                            FROM groups 
                            WHERE group_id = %s
                        """, (chat_id,))
                    
                    result = cur.fetchone()
                    lang = result['language'] if result else 'ko'  # Default to Korean if not found
                    
                    # Update cache
                    self.language_cache[chat_key] = lang
            except Exception as e:
                logging.error(f"Error in get_text: {e}")
                lang = 'ko'  # Default to Korean on error
                self.language_cache[chat_key] = lang
        
        return self.texts[lang][text_type]

    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /start command for both private chats and group chats.
        
        This handler:
        1. Registers new users/groups in the database
        2. Initializes points for new users/groups
        3. Sends appropriate welcome messages
        4. Shows the settings menu automatically
        
        Args:
            update (Update): The update object containing the message information
            context (ContextTypes.DEFAULT_TYPE): The context object for the current update
        """
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        chat_type = update.effective_chat.type
        
        try:
            with self.db.get_cursor(cursor_factory=RealDictCursor) as cur:
                if chat_type == 'private':
                    username = update.effective_user.username or f"user_{user_id}"
                    
                    cur.execute("""
                        SELECT user_id, language FROM users WHERE user_id = %s
                    """, (user_id,))
                    
                    result = cur.fetchone()
                    if not result:
                        cur.execute("""
                            INSERT INTO users (user_id, username, language)
                            VALUES (%s, %s, 'ko')
                        """, (user_id, username))
                        
                        cur.execute("""
                            INSERT INTO points (owner_type, owner_id, point)
                            VALUES ('user', %s, 0)
                        """, (user_id,))
                        
                        await self.set_language(chat_type, user_id, 'ko')
                        messages = self.get_text(chat_type, user_id, 'USER_GROUP_MESSAGES')
                        message = messages['user_success_register']
                    else:
                        await self.set_language(chat_type, user_id, result['language'])
                        messages = self.get_text(chat_type, user_id, 'USER_GROUP_MESSAGES')
                        message = messages['user_already_exists']
                        
                else:
                    group_name = update.effective_chat.title or f"group_{chat_id}"
                    
                    cur.execute("""
                        SELECT group_id, language FROM groups WHERE group_id = %s
                    """, (chat_id,))
                    
                    result = cur.fetchone()
                    if not result:
                        cur.execute("""
                            INSERT INTO groups (group_id, group_name, language)
                            VALUES (%s, %s, 'ko')
                        """, (chat_id, group_name))
                        
                        cur.execute("""
                            INSERT INTO points (owner_type, owner_id, point)
                            VALUES ('group', %s, 0)
                        """, (chat_id,))
                        
                        await self.set_language(chat_type, chat_id, 'ko')
                        messages = self.get_text(chat_type, chat_id, 'USER_GROUP_MESSAGES')
                        message = messages['group_success_register']
                    else:
                        await self.set_language(chat_type, chat_id, result['language'])
                        messages = self.get_text(chat_type, chat_id, 'USER_GROUP_MESSAGES')
                        message = messages['group_already_exists']
                
                await context.bot.send_message(chat_id=chat_id, text=message)
                
                # Show help menu after registration or if already registered
                keyboard = [
                    [
                        InlineKeyboardButton("📢 AD", callback_data="menu_ad"),
                        InlineKeyboardButton("💰 Points", callback_data="menu_points")
                    ],
                    [
                        InlineKeyboardButton("📚 Help", callback_data="menu_help"),
                        InlineKeyboardButton("🌐 Language", callback_data="menu_language")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                main_menu = self.get_text(chat_type, chat_id, 'MAIN_MENU')
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=main_menu,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logging.error(f"Error in start_handler: {e}", exc_info=True)
            messages = self.get_text(chat_type, chat_id, 'USER_GROUP_MESSAGES')
            error_message = messages['registration_error']
            await context.bot.send_message(chat_id=chat_id, text=error_message)

    async def points_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /points command to display current points status.
        
        This handler:
        1. Checks if the chat is private or group
        2. Retrieves points from the database
        3. Displays the points in the appropriate format
        
        Args:
            update (Update): The update object containing the message information
            context (ContextTypes.DEFAULT_TYPE): The context object for the current update
        """
        chat_type = update.effective_chat.type
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
        try:
            with self.db.get_cursor(cursor_factory=RealDictCursor) as cur:
                if chat_type == 'private':
                    cur.execute("""
                        SELECT p.point 
                        FROM points p 
                        WHERE p.owner_type = 'user' AND p.owner_id = %s
                    """, (user_id,))
                    result = cur.fetchone()
                    point = result['point'] if result else 0
                    val = round(point / VAL_UNIT, 2)
                    
                    points_menu = self.get_text(chat_type, user_id, 'POINTS_MENU')
                    message = points_menu['private'].format(point=point, val=val)
                else:
                    cur.execute("""
                        SELECT p.point 
                        FROM points p 
                        WHERE p.owner_type = 'group' AND p.owner_id = %s
                    """, (chat_id,))
                    result = cur.fetchone()
                    point = result['point'] if result else 0
                    val = round(point / VAL_UNIT, 2)
                    
                    points_menu = self.get_text(chat_type, chat_id, 'POINTS_MENU')
                    message = points_menu['group'].format(point=point, val=val)
            
            keyboard = [
                [InlineKeyboardButton("Claim $Val", callback_data=f"claim_val_{point}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode='Markdown')
            
        except Exception as e:
            logging.error(f"Error in points_handler: {e}")
            error_message = self.get_text(chat_type, chat_id, 'POINT_MESSAGES')['points_error']
            await context.bot.send_message(chat_id=chat_id, text=error_message)

    async def ads_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /ads command to display the latest active advertisement.
        
        This handler:
        1. Queries the database for the most recent active advertisement
        2. Displays the advertisement content if available
        3. Shows a notification if no active advertisements exist
        
        Args:
            update (Update): The update object containing the message information
            context (ContextTypes.DEFAULT_TYPE): The context object for the current update
        """
        try:
            chat_id = update.effective_chat.id
            chat_type = update.effective_chat.type
            with self.db.get_cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT content, url
                    FROM ads 
                    WHERE is_active = TRUE 
                    ORDER BY created_at DESC 
                    LIMIT 1
                """)
                result = cur.fetchone()
                
                
                if result:
                    keyboard = [
                        [
                            InlineKeyboardButton("광고 보러가기", url=result['url'])
                        ]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await context.bot.send_message(
                        chat_id=chat_id,
                        text=result['content'],
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
                else:
                    no_ads_error = await self.get_text(chat_type, chat_id, 'AD_MESSAGES')['no_ads_error']
                    await context.bot.send_message(chat_id=chat_id, text=no_ads_error, parse_mode='Markdown')
        except Exception as e:
            logging.error(f"Error in ads_handler: {e}")
            ad_fetching_error = await self.get_text(chat_type, chat_id, 'AD_MESSAGES')['ad_fetching_error']
            await context.bot.send_message(chat_id=chat_id, text=ad_fetching_error, parse_mode='Markdown')

    async def claim_val_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        chat_type = update.effective_chat.type
        chat_id = update.effective_chat.id

        _, points = query.data.split('_')
        points = int(points)
        
        try:
            if points < 10:  # 최소 10 포인트 필요
                isSuccess = False
                
            val_amount = points / 10
            
            # DB에서 포인트 차감 및 Val 지급 처리
            # isSuccess = await self.db.claim_val(user_id, points, val_amount)
            
            if isSuccess:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=self.get_text(chat_type, chat_id, 'CLAIM_VAL_MENU')['success'].format(val=val_amount),
                    reply_markup=query.message.reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(
                    chat_id=chat_id,
                    text=self.get_text(chat_type, chat_id, 'CLAIM_VAL_MENU')['failed'],
                    reply_markup=query.message.reply_markup,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logging.error(f"Error in claim_val_callback: {e}")
            await query.edit_message_text(
                text="❌ Claim failed: An error occurred",
                reply_markup=query.message.reply_markup
            )

    async def menu_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /help command by displaying the main menu with interactive buttons.
        
        This handler creates a keyboard with four main options:
        - Help: Shows detailed information about each feature
        - Points: Displays current points status
        - AD: Shows available advertisements
        - Language: Allows language preference changes
        
        Args:
            update (Update): The update object containing the message information
            context (ContextTypes.DEFAULT_TYPE): The context object for the current update
        """
        chat_type = update.effective_chat.type
        chat_id = update.effective_chat.id
        
        keyboard = [
            [
                InlineKeyboardButton("📢 AD", callback_data="menu_ad"),
                InlineKeyboardButton("💰 Points", callback_data="menu_points")
            ],
            [
                InlineKeyboardButton("📚 Help", callback_data="menu_help"),
                InlineKeyboardButton("🌐 Language", callback_data="menu_language")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        main_menu = self.get_text(chat_type, chat_id, 'MAIN_MENU')
        await context.bot.send_message(
            chat_id=chat_id,
            text=main_menu,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    async def language_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles the /language command by showing the language selection menu.
        """
        chat_id = update.effective_chat.id
        chat_type = update.effective_chat.type

        keyboard = [
            [
                InlineKeyboardButton("🇰🇷 한국어", callback_data="lang_ko"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        language_menu = self.get_text(chat_type, chat_id, 'LANGUAGE_MENU')
        await context.bot.send_message(
            chat_id=chat_id,
            text=language_menu,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
    async def help_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_type = update.effective_chat.type
        chat_id = update.effective_chat.id
        
        help_menu = self.get_text(chat_type, chat_id, 'HELP_MENU')
        await context.bot.send_message(
            chat_id=chat_id,
            text=help_menu, 
            parse_mode='Markdown'
        )

    async def menu_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles all menu button callbacks from the main menu.
        
        This handler processes different actions based on the callback data:
        - help: Displays detailed help information
        - points: Shows current points status for user or group
        - ad: Displays the latest active advertisement and awards points if eligible
        - language: Shows language selection options
        
        Args:
            update (Update): The update object containing the callback query
            context (ContextTypes.DEFAULT_TYPE): The context object for the current update
        """
        query = update.callback_query
        await query.answer()
        
        action = query.data.split('_')[1]
        chat_type = update.effective_chat.type
        chat_id = update.effective_chat.id
        
        if action == 'help':
            help_menu = self.get_text(chat_type, chat_id, 'HELP_MENU')
            await context.bot.send_message(
                chat_id=chat_id,
                text=help_menu, 
                parse_mode='Markdown'
            )
            
        elif action == 'points':
            try:
                with self.db.get_cursor(cursor_factory=RealDictCursor) as cur:
                    if chat_type == 'private':
                        cur.execute("""
                            SELECT p.point 
                            FROM points p 
                            WHERE p.owner_type = 'user' AND p.owner_id = %s
                        """, (chat_id,))
                        result = cur.fetchone()
                        point = result['point'] if result else 0
                        val = round(point / VAL_UNIT, 2)
                        points_menu = self.get_text(chat_type, chat_id, 'POINTS_MENU')
                        message = points_menu['private'].format(point=point,val=val)
                    else:
                        cur.execute("""
                            SELECT p.point 
                            FROM points p 
                            WHERE p.owner_type = 'group' AND p.owner_id = %s
                        """, (chat_id,))
                        result = cur.fetchone()
                        point = result['point'] if result else 0
                        val = round(point / VAL_UNIT, 2)
                        points_menu = self.get_text(chat_type, chat_id, 'POINTS_MENU')
                        message = points_menu['group'].format(point=point, val=val)
                        
                await context.bot.send_message(
                    chat_id=chat_id, text=message, parse_mode='Markdown'
                )
                
            except Exception as e:
                logging.error(f"Error in points callback: {e}")
                error_message = self.get_text(chat_type, chat_id, 'POINT_MESSAGES')['points_error']
                await context.bot.send_message(chat_id=chat_id, text=error_message)
                
        elif action == 'ad':
            try:
                with self.db.get_cursor(cursor_factory=RealDictCursor) as cur:
                    owner_type = 'user' if chat_type == 'private' else 'group'
                    logging.info(f"Processing ad action - chat_type: {chat_type}, chat_id: {chat_id}")
                    
                    # Check if user/group has already viewed an ad today
                    cur.execute("""
                        SELECT id 
                        FROM ad_view_logs 
                        WHERE owner_type = %s 
                        AND owner_id = %s 
                        AND DATE(viewed_at) = CURRENT_DATE
                    """, (owner_type, chat_id))
                    
                    has_viewed_today = cur.fetchone() is not None
                    logging.info(f"Has viewed today: {has_viewed_today}")
                    
                    # Get a random active advertisement
                    cur.execute("""
                        SELECT id, content 
                        FROM ads 
                        WHERE is_active = TRUE 
                        ORDER BY RANDOM() 
                        LIMIT 1
                    """)
                    result = cur.fetchone()
                    logging.info(f"Ad result: {result}")
                    
                    if result:
                        ad_menu = self.get_text(chat_type, chat_id, 'AD_MENU')
                        logging.info(f"Ad menu: {ad_menu}")
                        
                        if not has_viewed_today:
                            # Award points (10 points per view)
                            points_to_award = 10
                            
                            # Update points
                            cur.execute("""
                                UPDATE points 
                                SET point = point + %s 
                                WHERE owner_type = %s AND owner_id = %s
                                RETURNING point
                            """, (points_to_award, owner_type, chat_id))
                            
                            updated_points = cur.fetchone()['point']
                            logging.info(f"Updated points: {updated_points}")
                            
                            # Log the ad view
                            cur.execute("""
                                INSERT INTO ad_view_logs (owner_type, owner_id, ad_id, points_earned)
                                VALUES (%s, %s, %s, %s)
                            """, (owner_type, chat_id, result['id'], points_to_award))
                            
                        else:
                            # Get current points
                            cur.execute("""
                                SELECT point 
                                FROM points 
                                WHERE owner_type = %s AND owner_id = %s
                            """, (owner_type, chat_id))
                            current_points = cur.fetchone()['point']
                            logging.info(f"Current points: {current_points}")
                            
                        message = ad_menu['success'].format(
                            content=result['content']
                        )
                        await context.bot.send_message(
                            chat_id=chat_id, text=message, parse_mode='Markdown'
                        )
                    else:
                        ad_menu = self.get_text(chat_type, chat_id, 'AD_MENU')
                        await context.bot.send_message(
                            chat_id=chat_id, text=ad_menu['no_ad'], parse_mode='Markdown'
                        )
                        
            except Exception as e:
                logging.error(f"Error in ad callback: {e}", exc_info=True)
                error_message = self.get_text(chat_type, chat_id, 'AD_MESSAGES')['ad_error']
                await context.bot.send_message(
                    chat_id=chat_id, text=error_message, parse_mode='Markdown'
                )
                
        elif action == 'language':
            keyboard = [
                [
                    InlineKeyboardButton("🇰🇷 한국어", callback_data="lang_ko"),
                    InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            language_menu = self.get_text(chat_type, chat_id, 'LANGUAGE_MENU')
            await context.bot.send_message(
                chat_id=chat_id, text=language_menu, reply_markup=reply_markup, parse_mode='Markdown'
            )

    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Handles language selection callbacks.
        
        This handler:
        1. Updates the user's/group's language preference in the database
        2. Sends a confirmation message in the selected language
        
        Args:
            update (Update): The update object containing the callback query
            context (ContextTypes.DEFAULT_TYPE): The context object for the current update
        """
        query = update.callback_query
        await query.answer()
        
        selected_lang = query.data.split('_')[1]
        chat_type = update.effective_chat.type
        chat_id = update.effective_chat.id
        
        try:
            with self.db.get_cursor() as cur:
                if chat_type == 'private':
                    cur.execute("""
                        UPDATE users 
                        SET language = %s 
                        WHERE user_id = %s
                    """, (selected_lang, chat_id))
                else:
                    cur.execute("""
                        UPDATE groups 
                        SET language = %s 
                        WHERE group_id = %s
                    """, (selected_lang, chat_id))
                
                # 언어 설정 업데이트
                await self.set_language(chat_type, chat_id, selected_lang)
                
            lang_messages = self.get_text(chat_type, chat_id, 'LANG_MESSAGES')
            lang_message = lang_messages['language_success_ko'] if selected_lang == 'ko' else lang_messages['language_success_en']
            await context.bot.send_message(
                chat_id=chat_id, text=lang_message, parse_mode='Markdown'
            )
            
        except Exception as e:
            logging.error(f"Error in language_callback: {e}")
            error_message = self.get_text(chat_type, chat_id, 'LANG_MESSAGES')['language_error']
            await context.bot.send_message(
                chat_id=chat_id, text=error_message, parse_mode='Markdown'
            )