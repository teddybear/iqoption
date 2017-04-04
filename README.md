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

Stats by lang:
```
curl -H "Content-Type: application/json" -X POST -d '{"lang":"en-ru"}'  https://evening-stream-58031.herokuapp.com/translate/stats
```
Answer:
```
[
  {
    "lang": "en-ru",
    "requests": 1,
    "text": "Hello",
    "translated": "\u041f\u0440\u0438\u0432\u0435\u0442"
  },
  {
    "lang": "en-ru",
    "requests": 2,
    "text": "The Quick Brown Fox Jumps Over The Lazy Dog",
    "translated": "\u0411\u044b\u0441\u0442\u0440\u0430\u044f \u041a\u043e\u0440\u0438\u0447\u043d\u0435\u0432\u0430\u044f \u041b\u0438\u0441\u0430 \u041f\u0440\u044b\u0433\u0430\u0435\u0442 \u0427\u0435\u0440\u0435\u0437 \u041b\u0435\u043d\u0438\u0432\u0443\u044e \u0421\u043e\u0431\u0430\u043a\u0443"
  }
]

```