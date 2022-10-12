import { createReport } from 'docx-templates';
import fs from 'fs';
import zmq from 'zeromq';
import exec from "child_process";
import conf from './conf.js';


function sendOutputToSarf(reportUuid, reportFile){
	exec(`sarf --ingest --upload-report --filename ${reportFile} --report-id ${reportUuid} `, (error, stdout, stderr) => {
		if (error) {
			console.log(`error: ${error.message}`);
			return;
		}
		if (stderr) {
			console.log(`stderr: ${stderr}`);
			return;
		}
		console.log(`stdout: ${stdout}`);
	});
}

async function generateReport(reportData, output){
	const buffer = await createReport({
	  template,
	  data: reportData
	});
	fs.writeFileSync(output, buffer);
	sendOutputToSarf(output);
}


const sock = zmq.socket('sub');
const template = fs.readFileSync(conf.reportTemplate);

sock.connect('tcp://127.0.0.1:31337');
console.log('Worker connected to port 31337');

sock.subscribe('reports');

sock.on('message', function(msg){
  reportData = JSON.parse(msg);
  generateReport(reportData, `${conf.tmpFolder}/${reportData.uuid}`);
});

