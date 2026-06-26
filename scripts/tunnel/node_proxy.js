const http = require('http');
http.createServer((req, res) => {
    const target = req.url.startsWith('/proxy/') ? req.url.replace('/proxy/', '/') : req.url;
    const opt = { hostname: '127.0.0.1', port: 11434, path: target, method: req.method, headers: {} };
    Object.keys(req.headers).forEach(k => { if (!['host','connection'].includes(k)) opt.headers[k] = req.headers[k]; });
    opt.headers['host'] = '127.0.0.1:11434';
    const p = http.request(opt, pr => { res.writeHead(pr.statusCode, pr.headers); pr.pipe(res); });
    p.on('error', e => { res.writeHead(502); res.end(e.message); });
    req.pipe(p);
}).listen(19994, '0.0.0.0', () => console.log('ok'));
