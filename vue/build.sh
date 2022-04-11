#/bin/bash
npm run build
cp ./dist/index.html ../web_monitor/templates/app/index.html
rm ../web_monitor/static/css/app.*.css
rm ../web_monitor/static/js/app.*.js
rm ../web_monitor/static/js/app.*.map
cp -r ./dist/static/css ../web_monitor/static/
cp -r ./dist/static/js ../web_monitor/static/
cp -r ./dist/static/fonts ../web_monitor/static/