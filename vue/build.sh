#/bin/bash
npm run build
cp ./dist/index.html /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/templates/app/index.html
rm /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/static/css/app.*.css
rm /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/static/js/app.*.js
rm /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/static/js/app.*.map
cp -r ./dist/static/css /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/static/
cp -r ./dist/static/js /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/static/
cp -r ./dist/static/fonts /Users/xiaoc/code/xiaoc/WebMonitor/web_monitor/static/