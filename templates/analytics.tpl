<div><p1><b>{{ title }} - Разница цен за даты: {{ kwargs['date_from'] }} - {{ kwargs['date_to'] }}</b></p1></div>

<table border="1px;">
    <tr>
        <td>Цена в начале дня</td>
        <td>Наивысшая цена</td>
        <td>Низшая цена</td>
        <td>Цена в конце дня</td>
    </tr>
    <tr>
        <td>{{ data[0] }}</td>
        <td>{{ data[1] }}</td>
        <td>{{ data[2] }}</td>
        <td>{{ data[3] }}</td>
    </tr>
</table>