# Link Manager Plugin Base

Этот пакет содержит базовый класс LinkManagerPlugin, который облегчает создание плагинов для приложения Link Manager. Также он необходим для использования плагинов

## Использование

Чтобы создать плагин, просто унаследуйте свой класс плагина от LinkManagerPlugin и реализуйте методы plugin_info() и run().

Вот пример:

from plugin_base import LinkManagerPlugin

class MyAwesomePlugin(LinkManagerPlugin):
    @staticmethod
    def plugin_info():
        return {
            'name': 'Мой Крутой Плагин',
            'version': '1.0',
            'description': 'Этот плагин делает что-то потрясающее.',
            'author': 'Разработчик'
        }

    def run(self, url_links, action, key, url=None, **kwargs):
        if action == 'open':
            print(f"Мой Крутой Плагин: Ссылка {url} была открыта.")

if __name__ == '__main__':
    print(MyAwesomePlugin.plugin_info())