const express = require("express");
const path = require("path");
const bodyParser = require("body-parser");
const cors = require("cors");

const port = 23333;
const app = express();

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);
app.use(cors());
app.use(express.urlencoded());
app.use(express.json());

const server = app.listen(port);
console.log(`App listening on ${port}`);

const io = require("socket.io")(server);

app.use("/", express.static(path.resolve("../../dist")));

app.get("/", (req, res) => {
  res.sendFile(path.resolve("../../dist/index.html"));
});

const clients = [];
io.on("connection", function(socket) {
  console.log(socket.id);
  clients.push(socket.id);
});

app.post("/api", function(req, res) {
  console.log(req.body);
  clients.forEach(c => {
    io.to(c).emit("UPDATE", { data: req.body });
  });
  res.send("Got it");
});
