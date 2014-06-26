#!/bin/bash
rm -rf /usr/share/nginx/html/pg/static/0.1;
mkdir -p /usr/share/nginx/html/pg/static/0.1;
cp -R static/* /usr/share/nginx/html/pg/static/0.1;
/data/opt/java/jdk8/bin/java -jar /data/workspace/paymentgw/replacer-1.0.jar /usr/share/nginx/html/pg/static/0.1/js \${pom.version} 0.1
/data/opt/java/jdk8/bin/java -jar /data/workspace/paymentgw/replacer-1.0.jar /usr/share/nginx/html/pg/static/0.1/partials \${pom.version} 0.1
/data/opt/java/jdk8/bin/java -jar /data/workspace/paymentgw/replacer-1.0.jar /usr/share/nginx/html/pg/static/0.1/template \${pom.version} 0.1
chown -R nginx:nginx /usr/share/nginx/html/pg;
chmod -R a+rx /usr/share/nginx/html/pg;
