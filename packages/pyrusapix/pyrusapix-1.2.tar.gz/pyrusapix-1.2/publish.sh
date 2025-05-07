#!/bin/bash

# Если мы внутри venv — выходим из него
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Выход из виртуального окружения..."
    deactivate
fi

# Очистка папки dist
echo "Очистка папки dist..."
rm -rf dist/* || { echo "Ошибка очистки dist"; exit 1; }

# Сборка пакета
echo "Сборка пакета..."
python3 -m build || { echo "Ошибка сборки"; exit 1; }

ENV_TWINE=.env.twine

if [ -f $ENV_TWINE ]; then
    source $ENV_TWINE
fi

# Публикация на PyPI
echo "Публикация на PyPI..."
twine upload --verbose dist/* || { echo "Ошибка публикации"; exit 1; }

echo "Готово!"