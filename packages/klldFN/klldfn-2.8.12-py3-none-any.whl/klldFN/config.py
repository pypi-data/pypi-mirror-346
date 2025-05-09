"""Configuration utilities for klldFN"""
import json

class configuration:
    """Interact With The Bot Configuration("config.json")"""
    @staticmethod
    def read():
        """Read The Configuration File"""
        with open("config.json") as config_file:
            config = json.load(config_file)
            return config

class translations:
    """Interact With The Bot Configuration("translations.json")"""
    @staticmethod
    def read():
        """Read The Configuration File"""
        with open("translations/translations.json", encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config

class translations_system:
    """Interact With The Bot Configuration("translations-system.json")"""
    @staticmethod
    def read():
        """Read The Configuration File"""
        with open("translations/translations-system.json", encoding='utf-8') as config_file:
            config = json.load(config_file)
            return config

# Initialize language setting
get_Language = configuration.read()["Control"]["Language"]