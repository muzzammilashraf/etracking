var server = require('ws').Server;
var mysql = require('mysql');

var con = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "test",
});
con.connect(function(err) {
    if (err) throw err;
    console.log("Database Connected!");
});
var s = new server({ port: 5001 });
console.log("Websocket Server Started");

const change_password = (ws, data) => {
    con.query("UPDATE user_details SET password = '"+ data.new_password +"' WHERE username= '"+ data.username +"' AND password = '"+ data.old_password +"'", function (err, result) {
        let status_data = [];
        if (err) {
            var tmp_status_data = {
                status: 'failed'
            }
        } else {
            var tmp_status_data = {
                status: 'success'
            }
        }
        status_data.push(tmp_status_data);
        var wqe = {
            opcode: 'status',
            data_count: 1,
            data: status_data
        }
        ws.send(JSON.stringify(wqe));
    });
}

const register_client = (ws, id) => {
    con.query("SELECT * FROM records WHERE dev_id = '"+ id +"' ORDER BY id DESC LIMIT 1", function (err, result) {
        if (err) throw err;
        let avl_data = [];
        var tmp_avl_data = {
            dev_id: result[0].dev_id,
            timestamp: result[0].timestamp,
            priority: result[0].priority,
            lng: result[0].lng,
            lat: result[0].lat,
            alt: result[0].alt,
            angle: result[0].angle,
            speed: result[0].speed
        }
        avl_data.push(tmp_avl_data);
        var wqe = {
            opcode: 'avl_data',
            data_count: 1,
            data: avl_data
        }
        ws.send(JSON.stringify(wqe));
    });
}

const notify_client_avl_data = (recv_mesg) => {
    var wqe = {
        opcode: 'avl_data',
        data_count: recv_mesg.data_count,
        data: recv_mesg.data
    }
    s.clients.forEach(client => {
        if(client.id.includes(JSON.parse(recv_mesg.data[0]).dev_id)) {
            client.send(JSON.stringify(wqe));
        }
    })
}

const execute_op = (ws, wqe) => {
    switch(wqe.opcode) {
        case 'register':
            ws.id = [];
            for(let i = 0; i < wqe.data_count; i++) {
                var register = JSON.parse(wqe.data[i]);
                ws.type = register.type;
                ws.id.push(register.id);
                console.log("Client registered with id: " + register.id);
                switch(register.type) {
                    case 'client':
                        register_client(ws, register.id);
                        break;
                }
            }
            break;
        case 'unregister':
            for(let i = 0; i < wqe.data_count; i++) {
                var unregister = JSON.parse(wqe.data[i]);
                ws.id = ws.id.filter(function(item) {
                    return item !== unregister.id
                });
            }
            break;
        case 'change_password':
            for(let i = 0; i < wqe.data_count; i++) {
                var data = JSON.parse(wqe.data[0]);
                change_password(ws, data);
            }
            break;
        case 'avl_data':
            notify_client_avl_data(wqe);
            break;
        case 'echo':
            console.log(wqe.data);
            break;
    }
}

s.on('connection', (ws) => {
    ws.on('message', (message) => {
        var wqe = JSON.parse(message);
        execute_op(ws, wqe);
    });

    ws.on('close', () => {
    });
});