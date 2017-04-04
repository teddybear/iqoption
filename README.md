# iqoption Yandex Translate API
[![Build Status](https://travis-ci.org/teddybear/iqoption.svg?branch=master)](https://travis-ci.org/teddybear/iqoption)

Translate:

```
curl -H "Content-Type: application/json" -X POST -d '{"text":"Hello","lang":"en-ru"}'  https://evening-stream-58031.herokuapp.com/translate
```
Answer:
```
{
  "lang": "en-ru",
  "translated": [
    "\u041f\u0440\u0438\u0432\u0435\u0442"
  ]
}
```

Stats:
```
curl -H "Content-Type: application/json" -X POST -d '{"text":"Hello","lang":"en-ru"}'  https://evening-stream-58031.herokuapp.com/translate/stats
```
Answer:
```
[
  {
    "lang": "en-ru",
    "requests": 1,
    "text": "Hello",
    "translated": "\u041f\u0440\u0438\u0432\u0435\u0442"
  }
]
```