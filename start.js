const { spawn } = require('child_process');

// Start the Python RESTful API
const pythonProcess = spawn('python', ['./ml/restful_api.py']);

pythonProcess.stdout.on('data', (data) => {
  console.log(`Python API: ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
  console.error(`Python API Error: ${data}`);
});

pythonProcess.on('close', (code) => {
  console.log(`Python API exited with code ${code}`);
  process.exit(code);
});

// Start the Node.js server
const nodeProcess = spawn('node', ['./backend/server.js']);

nodeProcess.stdout.on('data', (data) => {
  console.log(`Node.js Server: ${data}`);
});

nodeProcess.stderr.on('data', (data) => {
  console.error(`Node.js Server Error: ${data}`);
});

nodeProcess.on('close', (code) => {
  console.log(`Node.js Server exited with code ${code}`);
  pythonProcess.kill();
  process.exit(code);
});

process.on('SIGINT', () => {
  pythonProcess.kill();
  nodeProcess.kill();
});
