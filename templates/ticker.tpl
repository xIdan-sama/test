<p1><b>{{ title }}</b></p1> <a href="/{{ title }}/insider" style="padding-left:550px;">/%TICKER%/insider</a>
<table border="1px;">
    <tr>
        <td>Дата</td>
        <td>Цена в начале дня</td>
        <td>Наивысшая цена</td>
        <td>Низшая цена</td>
        <td>Цена в конце дня</td>
        <td>Кол-во</td>
    </tr>
    {% for elem in data %}
    <tr>
        <td>{{ elem.date }}</td>
        <td>{{ elem.open }}</td>
        <td>{{ elem.high }}</td>
        <td>{{ elem.low }}</td>
        <td>{{ elem.close }}</td>
        <td>{{ elem.volume }}</td>
    </tr>
    {% endfor %}
</table>