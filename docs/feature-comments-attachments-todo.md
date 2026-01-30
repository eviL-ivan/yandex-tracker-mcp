# TODO: Добавление комментариев и вложений

## Статус: ЗАВЕРШЕНО ✅

### Задачи

- [x] **Implement issue_add_comment** (protocol, client, caching, MCP tool, tests)
  - Добавлен метод в протокол `IssueProtocol`
  - Реализован HTTP клиент с POST `/v2/issues/{issue_id}/comments`
  - Добавлен pass-through в caching layer
  - Создан MCP tool с параметрами: issue_id, text, attachment_ids, summonees, is_add_to_followers
  - Написаны тесты для HTTP клиента и MCP tool

- [x] **Implement attachment_upload_temp** (protocol, client, caching, MCP tool, tests)
  - Добавлен метод в протокол `IssueProtocol`
  - Реализован HTTP клиент с multipart/form-data загрузкой
  - Добавлен pass-through в caching layer
  - Создан MCP tool с base64 декодированием (filename, content_base64, mimetype)
  - Написаны тесты для HTTP клиента и MCP tool

- [x] **Update documentation** (README.md, README_ru.md, manifest.json)
  - Добавлены описания `issue_add_comment` в README.md и README_ru.md
  - Добавлены описания `attachment_upload_temp` в README.md и README_ru.md
  - Обновлён manifest.json с новыми инструментами
  - Обновлён CLAUDE.md с актуальным количеством инструментов (9 write tools)

- [x] **Run final verification** (task command)
  - Все 472 теста пройдены
  - ruff format - OK
  - ruff lint - OK
  - mypy type checking - OK

## Финальный результат

- **Тесты**: 472 passed
- **Форматирование**: OK
- **Линтинг**: OK
- **Типизация**: OK
