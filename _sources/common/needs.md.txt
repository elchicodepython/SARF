# Detected needs

When I was working as an ethical hacker I began to notice a series of needs in
my day to day that this platform tries to solve.

## Need for custom vulnerability templates

I used to get frustrated spending a lot of time styling reports instead of
using my knowledge to improve their content.

In my first attempt at automating reports I started a repository with
vulnerability descriptions written by me. When I had to write a new
vulnerability, I started from the template that I already had written. Then I
modified it to adjust the CVSS, to add the real impact on my client's business
and add the evidence on how to exploit it. This allowed me to significantly
increase the time I had to audit by reducing the time I spent generating the
report.

## Need for report templates and automatic report generation

As different clients had different report formats and particularities to
remember this wasn't enough. The problem wasn't that I had to remember
everything about each client. The problem was that we wanted all the members of
the team to remember it and even if it was well noted and documented, human
errors were common.

The data was correct but the formatting was often wrong and the style of a
report is one of the most most valued parts by customers.

This led me to want to generate automatic reports with specific styles based
on each client.

If vulnerabilities were stored in a structured way in some kind of data store
associated with a report... A tool could use this data to generate a
client-specific styled report.

That's why I thought it would be very interesting to be able to have multiple
reporting engines with templates. A report engine could generate reports in a
specific format like docx.

The templates could be made by business people without the need to write code
directly in the report engine template language. For the docx report engine
templates could be written in word.

## Need for security assesment traceability

I would often conduct an audit on an asset that a co-worker had previously
audited a long time ago. Sometimes I was not convinced by some reported
vulnerabilities and I considered that they could be a false positive. If the
evidence in the past document wasn't enough to determine whether or not the
vulnerability actually existed I was often in a bind. If I replicated the steps
of the previous auditor and found no evidence of the vulnerability, it could be
that the vulnerability had been corrected, but it could also be that it had
never existed. In the worst case, it could be that something not evidenced was
causing the vulnerability to not be replicated and we did not know if it had
been corrected.

This made me strongly desire to be able to have traceability of everything
that was done in a report.

I wanted to have the outputs of all the tools. Not just what was added to the
report. I wanted the reporter thoughts.

- When was an action performed?
- Who performed it?
- What was the result?
- Any kind of special thoughts about it?

In summary: What has been done, when, by who and how.
Wanted a detailed journal of the security assesment.

A "security assesment changelog".

This would also be very useful for continuing a security assessment that a
co-worker had started.

During the audit process I saved all this data in a cherrytree that I
consulted while generating the report. This allowed me to avoid trying the same
action multiple times generating as little noise as possible.
This was helpful with my reports as I was very disciplined about documenting
everything. However, it added time and it was not something that we all did.

Sometimes I dreamed of a tool that would allow me to achieve all the actions I
did in the cherrytree with less effort. I dreamed of being able to see all the
actions that had been done during an audit. Both mine and those of my
co-workers.

## Need for tools interconnection

Ethical hacking tools are very varied.

When starting an audit one could launch an nmap and based on the results that
this tool throws decide what to do.

Example:
nmap discovers a web service on port 8080 where a wordpress is hosted.

In case it in within the scope, an auditor will perform a series of actions
such as running wpscan in search of vulnerabilities, listing directories with
dirbuster, etc.

I have seen many ethical hacking teams develop similar tools to try to
improve processes over and over again. Generally an ethical hacker is very good
at penetration testing but not at coding so these projects end up with a lot of
spaghetti code and end up taking more time than they should.

I dream of a pipeline of ethical hacking tools. A pipeline where any ethical
hacker or developer can connect to decide to take an action based on the
outputs of another tool. A pipeline that allows all the specific software
developed in each team to be interconnected.

How do I propose to achieve this interconnection between such diverse
applications? Through messages.

When executing a tool its output will be saved in a data backend and a message
will be sent notifying whoever is listening that a particular tool has been
executed. Other tools will be able to subscribe and process the information
that is of interest to them. Once this information is received, they will be
able to perform actions such as notify users, launch other tools based on the
output of previous ones, process the results and anything else you can imagine.

Everything would be logged and associated with a specific report. All this
additional information would be very useful for future audits.

> New needs will be added here as they get written -
