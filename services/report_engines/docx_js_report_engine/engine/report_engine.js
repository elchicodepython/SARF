import { createReport } from 'docx-templates';
import fs from 'fs';
import zmq from 'zeromq';
import child_process from "child_process";
import conf from './conf.js';


async function sendOutputToSarf(reportUuid, reportFile) {
	console.log("🚀 ~ file: report_engine.js:9 ~ sendOutputToSarf ~ reportUuid:", reportUuid)
	const cmd = `--ingest --upload-report --filename ${reportFile} --report-id ${reportUuid}`;
	console.log("🚀 ~ file: report_engine.js:13 ~ sendOutputToSarf ~ cmd:", cmd);
	try {
		const process = child_process.spawn('sarf', cmd.split(' '));
		process.stdout.on("data", data => console.log(data))
		process.stderr.on("data", data => console.log(data))
	}
	catch (error) {
		console.log("🚀 ~ file: report_engine.js:19 ~ sendOutputToSarf ~ error:", error);
	}
}


async function generateReport(reportData, output){
    console.log(reportData);
	const buffer = await createReport({
	  template,
	  data: reportData
	});
	fs.writeFileSync(output, buffer);
	sendOutputToSarf(reportData.project.uuid, output);
}


const sock = zmq.socket('sub');
const template = fs.readFileSync(conf.reportTemplate);

sock.connect(conf.binding_address);
console.log('Worker connected');

sock.subscribe('reports');

sock.on('message', function(msg){
  const msgTxt = msg.toString();
  console.log(msgTxt);
  const msgBody = msgTxt.substr(msgTxt.indexOf(" ") + 1);
  const reportData = JSON.parse(msgBody);
  generateReport(reportData, `${conf.tmpFolder}/${reportData.project.uuid}.docx`);
});

