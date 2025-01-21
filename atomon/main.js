import express from "express";
import http from "http";

import { conf } from "./config.js"

const PORT = 8080;

const app = express();
const server = http.createServer(app);

app.use(express.static("./atomon/dist"));

server.listen(PORT, () =>
{
	console.log("Pok Atom Feed Monitor listening at " + PORT);
});