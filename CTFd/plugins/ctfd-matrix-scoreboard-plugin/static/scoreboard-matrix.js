function updatescores () {
    $.get(script_root + '/scores', function( data ) {
        const teams = data.standings;
        $('#scoreboard > tbody').empty();
        for (let i = 0; i < teams.length; i++) {
            // 只保留排名、队伍、得分、解题数、最后解题时间
            const row = `
                <tr>
                    <td>${i + 1}</td>
                    <td><a href='/user/${teams[i].id}'>${htmlentities(teams[i].team)}</a></td>
                    <td>${teams[i].score}</td>
                    <td>${teams[i].solve_count}</td>
                    <td>${teams[i].last_solve_time || '-'}</td>
                </tr>
            `;
            $('#scoreboard > tbody').append(row);
        }
    });
}

// 保留定时更新功能
function update() {
    updatescores();
}

// 每5分钟更新一次积分（300000毫秒）
setInterval(update, 300000);