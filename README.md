# Derigava Support

Персональная страница добровольной поддержки открытых проектов Derigava.

**Сайт:** https://derigava.github.io/support/  
**Бренд:** https://github.com/Derigava/derigava-brand

## Стек

Чистый HTML + CSS + JavaScript (ES modules); GitHub Pages + Actions. Без backend, базы данных, аналитики и тяжёлых зависимостей.

## Локальный запуск

Требуются Python 3 и Node.js 22+.

```bash
python3 scripts/sync_brand.py
node scripts/check.mjs
python3 -m http.server 5173 --directory site
```

Открой http://localhost:5173/ .

Внимание: брендовые ассеты *не создаются заново*. Скрипт `sync_brand.py` переносит **только нужные** официальные SVG, PNG, три фирменных шрифта и их SIL OFL лицензии из репозитория `Derigava/derigava-brand` с зафиксированного коммита. После выполнения всё работает локально, без внешних шрифтов. В GitHub Actions этот шаг выполняется перед публикацией.

## Где править содержимое

- **Проекты:** `site/data/projects.js`. Объект задаёт название, RU/EN-описания, ссылки и порядок карточек.
- **Способы поддержки:** `site/data/support.js`. Добавить элемент: `{ id: "boosty", label: "Boosty", url: "https://...", enabled: true }`. Можно менять порядок, скрывать `enabled: false`, удалять. Пустой массив показывает честное сообщение без платёжных кнопок.
- **Переводы:** `site/data/i18n.js` (RU / EN).
- **Стили интерфейса:** `site/styles.css`.
- **Токены:** `site/tokens.css` скопированы из `04 Управление и продажи/Командный кит/source/tokens.css` официальной бренд-системы.

После изменения JS запусти `node scripts/check.mjs`. Файлы и конфигурации не содержат секретов. Ссылки платежей только внешние.

## Публикация

GitHub Actions `.github/workflows/pages.yml` при push в `main` запускает проверки, синхронизацию фирменных ассетов, загружает статический `site/` как Pages artifact и публикует через `actions/deploy-pages`.

В настройках репозитория **Settings → Pages → Build and deployment → Source: GitHub Actions**.

Все ссылки и ассеты относительные, публикация работает под путём `/support/`.

## Происхождение и права

Знак, палитра и оформление: © 2026 Дмитрий Горлов, [Derigava visual system](https://github.com/Derigava/derigava-brand) и её [условия](https://github.com/Derigava/derigava-brand/blob/main/LICENSE.md). Это использование владельцем в собственном проекте, а не отдельная лицензия на фирменные материалы.

Шрифты Unbounded, Onest и JetBrains Mono распространяются по SIL Open Font License 1.1; уведомления копируются в `site/assets/fonts/` вместе с ними при сборке.

**Лицензия исходного кода этого сайта пока не назначена.** Это не означает передачу прав на фирменные материалы.
