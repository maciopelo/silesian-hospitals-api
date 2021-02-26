const express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");

const app = express();
const port = process.env.PORT || 8080;

let _data;
const minutes = 5;

const id = setInterval(() => {
  const python = spawn("python", ["scraper.py"]);
  python.on("close", (code) => {
    console.log(
      `Python script executed with code ${code} | Update done at ${Date()}`
    );
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

app.listen(port, () => console.log(`Website works on port ${port}.`));
