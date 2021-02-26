const express = require("express");
const { spawn } = require("child_process");

const app = express();
const port = process.env.PORT || 8080;

let data = require("./data.json");
const minutes = 0.5;

const id = setInterval(() => {
  const python = spawn("python", ["scraper.py"]);
  console.log(" i should have exec script");
  python.on("close", (code) => {
    console.log(`Child process close all stdio with code ${code}`);
    data = require("./data.json");
  });
}, minutes * 60 * 1000);

app.get("/", (req, res) => {
  res.json(data);
});

app.listen(port, () => console.log(`Works!`));
