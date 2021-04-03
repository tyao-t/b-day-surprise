require('dotenv').config()
const express = require("express");
const bodyParser = require("body-parser");
const request = require("request");
const https = require("https");
const cors = require("cors");

var corsOptions = {
  origin: "http://localhost:3000"
};

const mongoose = require('mongoose');
mongoose.connect(process.env.MONGO_CONFIG_URL,
{useNewUrlParser: true, useUnifiedTopology: true});

const Friend = mongoose.model('Friends', { name: String, email: String, bday: String, tag: String});

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));

app.use(express.static("public"))

app.get("/", (req, res) => {
    res.sendFile(__dirname + "/signup.html");
})

app.post("/", (req, res) => {
    const dataShortcut = req.body;
    const name = dataShortcut.name;
    const email = dataShortcut.email;
    const bday = dataShortcut.bday;
    const p = new Friend({name: name, email: email, bday: bday, tag: 's'});
    p.save();
    res.sendFile(__dirname + "/success.html")
});

app.get("/data", (req, res) => {
    Person.find((err, foundPeople) => {
        //console.log(foundCats);
        res.send(foundPeople);
    });
})

app.post("/failure", (req,res) => {
    res.redirect("/");
});

const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log("Server is running on port " + port);
});

// f007cceda3aae0c781f67fa2f14f6713-us4
// 9660118054
