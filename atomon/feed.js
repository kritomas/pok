import { readFileSync, writeFileSync } from 'fs';
import { DOMParser, XMLSerializer } from "xmldom";
import { v4 as uuidv4 } from "uuid";

const FEED_LOCATION = "atomon/dist/pok.atom";
const FEED_TEMPLATE_LOCATION = "atomon/atom-template.xml";

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

export function addAutomatedEntry(title, content)
{
	let raw = "" + readFileSync(FEED_TEMPLATE_LOCATION);
	let xml = parser.parseFromString(raw);

	let entry = xml.createElement("entry")

	let titleElement = xml.createElement("title");
	titleElement.textContent = title;
	entry.appendChild(titleElement);

	let author = xml.createElement("author");
	let authorName = xml.createElement("name");
	authorName.textContent = "Pok Atom Feed Monitor";
	author.appendChild(authorName)
	entry.appendChild(author);

	let id = xml.createElement("id");
	id.textContent = "urn:uuid:" + uuidv4();
	entry.appendChild(id);

	let updated = xml.createElement("updated");
	updated.textContent = new Date().toISOString();
	entry.appendChild(updated);

	let contentElement = xml.createElement("content");
	contentElement.setAttribute("type", "text");
	contentElement.textContent = content;
	entry.appendChild(contentElement);

	let feed = xml.getElementsByTagName("feed")[0];
	feed.appendChild(entry);

	writeFileSync(FEED_LOCATION, serializer.serializeToString(xml));
}

try
{
	let xml = readFileSync(FEED_LOCATION);
}
catch
{
	reset();
}