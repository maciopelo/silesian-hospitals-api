const express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");

const app = express();
const port = process.env.PORT || 8080;

let _data;
const minutes = 0.5;

const id = setInterval(() => {
  const python = spawn("python", ["scraper.py"]);
  console.log(" i should have exec script");
  python.on("close", (code) => {
    console.log(`Child process close all stdio with code ${code}`);
    fs.readFile("./data.json", "utf8", (err, data) => {
      if (err) {
        console.error(err);
        return;
      }
      _data = JSON.parse(data);
    });
  });
}, minutes * 60 * 1000);

app.get("/", (req, res) => {
  res.json(_data);
});

app.listen(port, () => console.log(`Works!`));
