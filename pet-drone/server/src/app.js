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

console.log(`App listening on ${port}`);

app.use("/", express.static(path.resolve("../../dist")));
app.get("/", (req, res) => {
  res.sendFile(path.resolve("../../dist/index.html"));
});

app.post("/api", function(req, res) {
  console.log(req.body);
  res.send("Got it");
});

const server = app.listen(port);

const io = require("socket.io")(server);

io.on("connection", function(socket) {
  console.log(socket.id);
  socket.emit("news", { hello: "world" });
  socket.on("my other event", function(data) {
    console.log(data);
  });
});
