var express = require("express");
const cors = require("cors");

var app = express();
var connection = require("./database");
var data = { 'vehicle': 2, 'dest': 'charholi', 'src': 'kothrud' }
var customer = { 'name': '', 'gender': "", "age": null }
var customer = { 'cust_id': null, 'src': "", "dest": "", 'duartion': "", cost: null, "prov_id": null, 'vehicle': 0 }
var providersData = [];
var providerScores = new Map();
// var finalData = {'providers' : [], 'queryRes' : []}

app.use(cors())
app.use(express.json())

function getProviderNames(result, providersData) {
    if (result.length == 0) return;
    for (let i = 0; i < result.length; i++) {
        for (let j = 0; j < providersData.length; j++) {
            if (result[i]['prov_id'] == providersData[j]['prov_id']) {
                // console.log("abwfkabfk");
                result[i]['rating'] = providersData[j]['ratings'];
                result[i]['provid_name'] = providersData[j]['name'];
            }
        }
    }

    function toSeconds(timeStr) {
        const [hours, minutes, seconds] = timeStr.split(':').map(Number);
        return hours * 3600 + minutes * 60 + seconds;
    }


    // var optimum = result[0];
    // for (let i = 0; i < result.length; i++) {
    //     if((result[i]['cost'] <= optimum['cost'] && result[i]['duration'] <= optimum['duration']) 
    //     || (result[i]['rating'] > optimum['rating'] && result[i]['duration'] <= optimum['duration'])
    //     || (result[i]['rating'] > optimum['rating'] && (result[i]['cost'] <= optimum['cost']))){
    //             optimum = result[i];
    //     }  
    // }

    // console.log("Most optimum is : ")
    // console.log(optimum)


    // providerScores.set(optimum['provid_name'],100);
    // console.log(providerScores)
    for (let i = 0; i < result.length; i++) {
        if (!providerScores.has(result[i]['provid_name'])) {
            var duration = toSeconds(result[i]['duration']);
            var weight = - 0.33 * result[i]['cost'] - 0.33 * duration + 0.33 * result[i]['rating'];
            providerScores.set(result[i]['provid_name'], weight);
        }
    }

    const myArray = Array.from(providerScores);

    // Sort the array based on the values
    myArray.sort(function (a, b) {
        return b[1] - a[1];
    });

    // Create a new Map object from the sorted array
    // console.log(myArray);
    for (let index = 0; index < myArray.length; index++) {
        var score = ((myArray.length - index) / myArray.length) * 100;
        myArray[index][1] = score;
    }

    providerScores = new Map(myArray);
    // console.log(myArray);
    for (let i = 0; i < providersData.length; i++) {
        if (!providerScores.has(providersData[i]['name'])) {
            providerScores.set(providersData[i]['name'], 10);
        }
    }
    // console.log(providerScores);
}



app.post('/getData', async (req, res) => {
    data = req.body
    providerScores = new Map();
    query1 = "select * from rides where vehicle =" + data.vehicle + " and src = '" + data.source + "' and  dest = '" + data.destination + "'";

    connection.query(query1, (err, results) => {
        if (err) throw err;
        getProviderNames(results, providersData);
        console.log(providerScores);
        const myObject = Object.fromEntries(providerScores);
        // res.json(myObject);
        res.send(JSON.stringify(myObject, null, 2));
    })
    // console.log(data.vehicle)
})



app.listen(8000, () => {
    query2 = "select * from providers";
    // query2 = "select * from rides";
    console.log("Listening on port 8000");
    connection.commit(function (err) {
        if (err) throw err;
        console.log("Database connected successfully");
    })
    id = 0;
    connection.query(query2, (err, results) => {
        if (err) throw err;
        providersData = results;
        console.log(results);
    })
})

var id = -1;



app.post('/postCustomerDetails',async (req, res) => {
    details = req.body;
    console.log(details);
    query1 = "insert into rides(cust_id,src,dest,duration,cost,prov_id,vehicle) values('"+details.cust_id+"','"+details.src+"','"+details.dest+"','"+details.duration+"',"+details.cost+","+details.prov_id+","+details.vehicle+"  );"

    connection.query(query1,(err,result) =>{
        if(err) throw err;
    })
})

app.post('/getCustomerData', async (req, res) => {
    customer = req.body
    query1 = "select * from customer where cust_name = '" + customer.name + "' and gender = '" + customer.gender + "' and age = " + customer.age + ";"
    connection.query(query1, (err, result) => {

        // console.log(result);
        if (err) throw err;
        if (result.length != 0) {
            console.log("111111")
            id = result[0]['cust_id']
            console.log(id)
            res.send({ 'id': id })
        }
        else {

            query2 = "insert into customer(cust_name,gender,age) values('" + customer.name + "','" + customer.gender + "'," + customer.age + ");";

            connection.query(query2, async (err, result) => {
                if (err) throw err;
            })

            // query1 = "select * from customer where cust_name = '"+customer.name+"' and gender = '"+customer.gender+"' and age = "+customer.age+";"
            // query3 = "select * from customer where cust_name = 'vgb' and gender = 'MALE' and age = 20;"
            connection.query(query1, (err, result) => {
                console.log("2222222");
                if (err) throw err;
                id = result[0]['cust_id']
                console.log(id)
                res.send({ 'id': id })
            })

        }
        // id = 0;

    })
    // console.log(id);



});



