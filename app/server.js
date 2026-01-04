const http = require("http");

http.createServer((req, res) => {
  res.end("Hello from Docker App");
}).listen(3000, () => {
  console.log("Server running on port 3000");
});

