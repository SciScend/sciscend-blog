---
title: 'Примерна статия: как изглежда една публикация'
description: 'Тестова чернова, която показва оформлението на блога — заглавия, код, таблица и цитат. Не се публикува.'
pubDate: 2026-09-22
lang: bg
tags: [meta]
draft: true
---

Това е **тестова чернова**. Вижда се само в `npm run dev` и никога не влиза в production build.

## Заглавие второ ниво

Обикновен текст с [линк](https://sciscend.com/blog/) и `inline code`.

```python
from collections import Counter

def top_tags(posts):
    return Counter(t for p in posts for t in p["tags"]).most_common(5)
```

| Модел | Български текст | Цена |
|---|---|---|
| A | добре | ниска |
| B | отлично | висока |

> Цитат: мнението е това, което никой друг не може да напише вместо теб.

### Заглавие трето ниво

- първа точка
- втора точка
