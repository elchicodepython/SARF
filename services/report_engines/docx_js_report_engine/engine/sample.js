import { createReport } from 'docx-templates';
import fs from 'fs';

const template = fs.readFileSync('templates/sample_template.docx');

async function go(){

	const buffer = await createReport({
	  template,
	  data: {
		  project: {
	      vulns: [
		      {name: "SQLi", description: "SQLI founded in..."},
		      {name: "Invalid", description: "corrupted memory access easly"}
	      ]
		  }
	  },
	});
	fs.writeFileSync('report.docx', buffer)
}


go()
