import { readFileSync, writeFileSync } from 'fs';
import { DOMParser, XMLSerializer } from "xmldom";
import { v4 as uuidv4 } from "uuid";

const FEED_LOCATION = "atomon/dist/pok.atom";
const FEED_TEMPLATE_LOCATION = "atomon/dist/atom-template.xml";

const parser = new DOMParser();
const serializer = new XMLSerializer();

function reset()
{
	let raw = "" + readFileSync(FEED_TEMPLATE_LOCATION);
	let xml = parser.parseFromString(raw);
	xml.getElementsByTagName("id")[0].textContent = "urn:uuid:" + uuidv4();
	xml.getElementsByTagName("updated")[0].textContent = new Date().toISOString();
	writeFileSync(FEED_LOCATION, serializer.serializeToString(xml));
}

reset();
//xml = readFileSync(CONFIG_LOCATION);