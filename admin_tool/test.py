
dn = "test.com"
ssl_url = "/usr/local/nginx/ssl/dn/"
www_info = str("server {\nlisten 80;\nlisten 443 ssl;\nserver_name m.") + str(dn) + str(";\nssl_certificate ") + str(ssl_url) + str("1_m.") + str(dn) + str("_bundle.crt;\nssl_certificate_key ") + str(ssl_url) + str("2_m.") + str(dn) + str(".key;\ncharset UTF-8;\naccess_log logs/new_access.log access_cookie;\nproxy_http_version 1.1;\nproxy_set_header Host $http_host;\nproxy_set_header Connection "";\nproxy_set_header X-Real-IP $http_x_real_ip;\nproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\nif ($scheme = http ) {return 301 https://$host$request_uri;}\nlocation / {\nroot  /home/waguda/web/cashsmart;\nindex index.html;\ntry_files $uri $uri/ /index.html =404;\nexpires 1d;\nbreak;\n}\nlocation ^~ /old/ {\nroot  /home/waguda/web/cashsmart;\nindex index.html;\ntry_files $uri $uri/ /old/index.html =404;\nbreak;\n}\nlocation ^~ /d/\n{\nproxy_pass http://cash_prod_webserver;\nbreak;\n}\n}")

print(www_info)