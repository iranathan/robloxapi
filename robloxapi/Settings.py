import json
import logging

class SettingsSelector:
    def __init__(self, request):
        self._request = request.request

    def __setitem__(self, key, value):
        if key == 'blurb':
            self.blurb(value)
        elif key == 'birthday':
            self.birthday(value)
        elif key == 'gender':
            self.gender(value)
        elif key == 'language':
            self.language(value)
        elif key == 'location':
            self.location(value)
        elif key == 'theme':
            self.theme(value)

    def blurb(self, blurb):
        data = {
            'description': blurb.replace('', '+')
        }
        return self._request(url='https://accountinformation.roblox.com/v1/description', method='POST', data=json.dumps(data))

    def birthday(self, birthjson):
        data = {
            'birthDay': birthjson['day'],
            'birthMonth': birthjson['month'],
            'birthYear': birthjson['year']
        }
        return self._request(url='https://accountinformation.roblox.com/v1/birthdate', method='POST', data=json.dumps(data))

    def gender(self, gender):
        data = {
            'gender': 2
        }
        if gender == 'male': data['gender'] = 2
        if gender == 'female': data['gender'] = 3
        return self._request(url='https://accountinformation.roblox.com/v1/gender', method='POST', data=json.dumps(data))

    def language(self, language):
        url = 'https://locale.roblox.com/v1/locales/supported-locales'
        r = json.loads(self._request(url=url, method='GET'))['supportedLocales']
        selected_lang = None
        for lang in r:
            if lang['name'] == language or lang['nativeName'] == language:
                selected_lang = lang
        if not selected_lang:
            return logging.error(f'Language {language} is not a language or is not supported by roblox.')
        data = {
            'supportedLocaleCode': selected_lang['locale']
        }
        return self._request(url='https://locale.roblox.com/v1/locales/set-user-supported-locale', method='POST', data=json.dumps(data))

    def location(self, country):
        url = 'https://locale.roblox.com/v1/locales/supported-locales'
        r = json.loads(self._request(url=url, method='GET'))['supportedLocales']
        selected_lang = None
        for lang in r:
            if lang['name'] == country or lang['nativeName'] == country:
                selected_lang = lang
        if not selected_lang:
            return logging.error(f'Country {language} is not a country or is not supported by roblox.')
        data = {
            'countryId': selected_lang['id']
        }
        return self._request(url='https://www.roblox.com/account/settings/account-country', method='POST', data=json.dumps(data))

    def theme(self, theme):
        if theme.lower() == 'light': theme = 'Classic'
        elif theme.lower() == 'dark': theme = 'Dark'
        data = {
            'themeType': theme
        }
        return self._request(url='https://accountsettings.roblox.com/v1/themes/user', method='PATCH', data=json.dumps(data))

    def media(self, type, value):
        data = {
            'facebook': '',
            'twitter': '',
            'youtube': '',
            'twitch': '',
            'promotionChannelsVisibilityPrivacy': 'AllUsers'
        }
        if type == 'facebook': data['facebook'] = value
        elif type == 'twitter': data['twitter'] = value
        elif type == 'youtube': data['youtube'] = value
        elif type == 'twitch': data['twitch'] = value
        return self._request('https://accountinformation.roblox.com/v1/promotion-channels', method='POST', data=json.dumps(data))

class Settings:
    def __init__(self, request):
        self.request = request

    def changeSettings(self):
        return SettingsSelector(self.request)

