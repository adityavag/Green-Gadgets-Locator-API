const express = require('express');
const app = express();
const PORT = 3001;
const cors = require('cors')
const { spawn } = require('child_process');
const nodePickle = require('node-pickle');
const fs = require('fs');



app.use(cors({
    origin: '*',
    credentials: true,
}));


app.use(express.json())
app.post('/', function (req, res) {
    const { lat, long } = req.body;
    console.log(lat, long);
    const process = spawn('python', ["./Map.py"]);
    process.stdout.on('data', (data) => {
        console.log(`${data}`)
    })
    res.send("Hello")
})

app.listen(PORT, () => console.log(`Listening on port ${PORT}!`))