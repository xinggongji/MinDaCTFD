function updatescores() {
    $.get(script_root + '/scores', function(data) {
        var standings = data.standings;
        var tbody = $('#scoreboard > tbody');
        tbody.empty();
        for (var i = 0; i < standings.length; i++) {
            var row = '<tr>' +
                '<td class="text-center">' + (i + 1) + '</td>' +
                '<td><a href="/user/' + standings[i].id + '">' + htmlentities(standings[i].team) + '</a></td>' +
                '<td>' + standings[i].score + '</td>' +
                '<td>' + standings[i].solve_count + '</td>' +
                '<td>' + (standings[i].last_solve_time || '-') + '</td>' +
                '</tr>';
            tbody.append(row);
        }
    });
}

function update() {
    updatescores();
}

setInterval(update, 300000);
