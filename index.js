const express = require("express");
const { spawn } = require("child_process");

const app = express();
const port = process.env.PORT || 8080;

let data = require("./data.json");
const minutes = 0.5;

const id = setInterval(() => {
  const python = spawn("python", ["scraper.py"]);
  python.on("close", (code) => {
    //console.log(`Child process close all stdio with code ${code}`);
    data = require("./data.json");
  });
}, minutes * 60 * 1000);

app.get("silesia/hospitals/v1/api", (req, res) => {
  res.json(data);
});

app.listen(port, () =>
  console.log(
    `Checkout API at http://localhost:${port}/silesia/hospitals/v1/api !`
  )
);
