import { readFileSync, writeFileSync } from 'fs';
import { DOMParser, XMLSerializer } from "xmldom";
import { v4 as uuidv4 } from "uuid";

const FEED_LOCATION = "/var/pok/pok-feedmon/dist/pok.atom";
const FEED_TEMPLATE_LOCATION = "/var/pok/pok-feedmon/atom-template.xml";

const parser = new DOMParser();
const serializer = new XMLSerializer();

export function resetQuiet()
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

	xml.getElementsByTagName("updated")[0].textContent = new Date().toISOString();

	let entry = xml.createElement("entry")

	let titleElement = xml.createElement("title");
	titleElement.textContent = title;
	entry.appendChild(titleElement);

	let author = xml.createElement("author");
	let authorName = xml.createElement("name");
	authorName.textContent = "Pok Automatic Feed Updater";
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

export function reset()
{
	resetQuiet();
	addAutomatedEntry("Feed Reset", "The feed has been wiped.")
}

try
{
	let xml = readFileSync(FEED_LOCATION);
}
catch
{
	resetQuiet();
}