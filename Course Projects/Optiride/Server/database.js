var mysql = require("mysql");

var connection = mysql.createConnection({
    host: "localhost",
    password: "akshay",
    database: "optiride",
    user: "root",
})

module.exports = connection;