import re
from typing import List, Set
import os


class RussianProfanityFilter:
    def __init__(self):
        self.profanity_words = self.load_profanity_words()

    def load_profanity_words(self) -> Set[str]:
        """Загружает словарь матерных слов"""

        russian_profanity = {
            'блять', 'блядь', 'бля', 'блеать', 'блядина', 'блядский',
            'хуй', 'хуев', 'хуёвый', 'хуйня', 'хуя', 'хуево',
            'пизда', 'пиздец', 'пиздатый', 'пиздос', 'пиздабол',
            'ебал', 'ебать', 'ебаный', 'ебучий', 'ебанутый',
            'сука', 'сучара', 'сучий', 'сучка',
            'мудак', 'мудень', 'мудацкий',
            'долбоеб', 'долбаёб', 'долбоёб',
            'уебан', 'уёбок', 'уебище',
            'залупа', 'залупись', 'залупиться',
            'гандон', 'гондон',
            'шлюха', 'шлюшка',
            'выебок', 'выебываться',
            'трахать', 'трахнуть',
            'вагина', 'влагалище',
            'секс', 'секас',
            'сперма', 'конча',
            'пезда', 'пидор', 'пидорас'
        }

        english_profanity = {
            'fuck', 'fucking', 'fucker', 'motherfucker',
            'shit', 'shitting', 'bullshit',
            'ass', 'asshole', 'smartass',
            'bitch', 'bitches', 'bitching',
            'cunt', 'cunts',
            'dick', 'dicks', 'dickhead',
            'pussy', 'pussies',
            'cock', 'cocks',
            'whore', 'whores',
            'slut', 'sluts',
            'bastard', 'bastards',
            'nigger', 'niggers',
            'retard', 'retarded'
        }

        return russian_profanity | english_profanity

    def contains_profanity(self, text: str) -> bool:
        """Проверяет текст на матерные слова"""
        if not text or not isinstance(text, str):
            return False

        cleaned_text = self.clean_text(text)
        if not cleaned_text:
            return False

        words = set(cleaned_text.split())
        return bool(words & self.profanity_words)

    def clean_text(self, text: str) -> str:
        """Очищает текст для проверки"""
        text = text.lower()

        # Заменяем похожие символы
        replacements = {
            '4': 'а', '0': 'о', '3': 'е', '1': 'и',
            '6': 'б', '5': 'с', '9': 'д', '7': 'т',
            '8': 'в', '$': 'с', '@': 'а', '!': 'и'
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        # Удаляем все кроме букв и пробелов
        text = re.sub(r'[^a-zа-яё\s]', '', text)
        text = re.sub(r'\s+', ' ', text)

        return text.strip()