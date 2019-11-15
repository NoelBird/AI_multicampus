



## django message 사용하기

django message를 사용하면, 글이 정상적으로 작성되었다는 메시지를 출력할 수 있습니다.

```python
# articles/views.py

...

from django.contrib import messages

...

# in any function using post method
if form.is_valid():
   messages.success(request, '게시물이 성공적으로 작성되었습니다!')

...

```

```html
<!-- articles/templates/articles/detail.html -->
{% if messages %}
  {% for message in messages %}
    <div class="alert alert-success">
        {{message}}
    </div>
  {% endfor %}
{% endif %}
```

세션에 저장을 하기 때문에 message를 context로 넣어주지 않아도 됩니다.

너무 쉬우면, `collaborative Filtering`을 넣으면 좋습니다.

