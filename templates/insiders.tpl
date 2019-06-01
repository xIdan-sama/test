<p1><b>{{ title }}</b></p1>
<table border="1px;">
    <tr>
        <td>Инвестор</td>
        <td>Должность</td>
        <td>Дата</td>
        <td>Тип операции</td>
        <td>Тип владения</td>
        <td>Торгуемые акции</td>
        <td>Цена</td>
        <td>Удержанные акции</td>
    </tr>
    {% for elem in data %}
    <tr>
        <td><a href="/{{ title }}/insider/{{ elem.insider.name }}">{{ elem.insider.name }}</a></td>
        <td>{{ elem.insider.relation }}</td>
        <td>{{ elem.date }}</td>
        <td>{{ elem.type }}</td>
        <td>{{ elem.owner_type }}</td>
        <td>{{ elem.traded }}</td>
        <td>{{ elem.price }}</td>
        <td>{{ elem.held }}</td>
    </tr>
    {% endfor %}
</table>