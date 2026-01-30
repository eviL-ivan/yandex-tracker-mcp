# План: Добавление комментариев и вложений в Yandex Tracker MCP

## Цель
Добавить два новых инструмента:
1. **`issue_add_comment`** - добавление комментариев к задачам
2. **`attachment_upload_temp`** - загрузка временных файлов для прикрепления к задачам

## Файлы для изменения

### 1. Протокол: `mcp_tracker/tracker/proto/issues.py`

Добавить методы в `IssueProtocol`:

```python
async def issue_add_comment(
    self,
    issue_id: str,
    text: str,
    *,
    attachment_ids: list[str] | None = None,
    summonees: list[str] | None = None,
    is_add_to_followers: bool = True,
    auth: YandexAuth | None = None,
) -> IssueComment: ...

async def attachment_upload_temp(
    self,
    filename: str,
    content: bytes,
    *,
    mimetype: str | None = None,
    auth: YandexAuth | None = None,
) -> IssueAttachment: ...
```

### 2. Клиент: `mcp_tracker/tracker/custom/client.py`

Реализовать HTTP методы:
- `issue_add_comment`: POST `/v2/issues/{issue_id}/comments` (JSON body)
- `attachment_upload_temp`: POST `/v2/attachments` (multipart/form-data)

### 3. Кэширование: `mcp_tracker/tracker/caching/client.py`

Добавить pass-through методы (write-операции не кэшируются).

### 4. MCP Tools: `mcp_tracker/mcp/tools/issue_write.py`

Добавить инструменты:
- `issue_add_comment` - с параметрами: issue_id, text, attachment_ids, summonees, is_add_to_followers
- `attachment_upload_temp` - с параметрами: filename, content_base64, mimetype

**Важно**: Файлы передаются как base64-строки (MCP не поддерживает бинарные данные).

### 5. Тесты

| Тест | Файл |
|------|------|
| HTTP клиент комментарии | `tests/tracker/custom/issues/test_issue_comments.py` (новый класс) |
| HTTP клиент вложения | `tests/tracker/custom/issues/test_issue_attachments.py` (новый класс) |
| MCP tools | `tests/mcp/tools/test_issue_write_tools.py` (новые классы) |
| Регистрация | `tests/mcp/server/test_server_creation.py` (обновить WRITE_TOOL_NAMES) |

### 6. Документация

- `README.md` - добавить описание новых инструментов
- `README_ru.md` - русская версия
- `manifest.json` - обновить список инструментов

## Yandex Tracker API

### Создание комментария
```
POST /v2/issues/{issueId}/comments
Content-Type: application/json

{
  "text": "Текст комментария",
  "attachmentIds": ["id1", "id2"],
  "summonees": ["user_login"]
}
?isAddToFollowers=true
```

### Загрузка временного файла
```
POST /v2/attachments?filename=file.txt
Content-Type: multipart/form-data

[binary file data]
```

Возвращает attachment ID для использования в issue_create, issue_update, issue_add_comment.

## Порядок реализации

1. Протокол (`proto/issues.py`)
2. Клиент (`custom/client.py`)
3. Кэширование (`caching/client.py`)
4. MCP tools (`tools/issue_write.py`)
5. Тесты HTTP клиента
6. Тесты MCP tools
7. Документация

## Верификация

```bash
task              # Все проверки (format, lint, type, tests)
task test         # Только тесты
uv run mcp-tracker # Запуск сервера для ручной проверки
```

Проверить через MCP клиент:
1. Загрузить файл через `attachment_upload_temp` - получить ID
2. Создать комментарий через `issue_add_comment` с attachment_ids
3. Проверить комментарий через `issue_get_comments`
