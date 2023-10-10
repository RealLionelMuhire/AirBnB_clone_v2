#!/usr/bin/env bash
# This is to setup web static 
# 1. Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    apt-get update
    apt-get -y install nginx
fi

# 2. Create the necessary directories if they don't exist
directories=("/data" "/data/web_static" "/data/web_static/releases" "/data/web_static/shared" "/data/web_static/releases/test")
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
    fi
done

# 3. Create a fake HTML file for testing
echo -e '<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>' > /data/web_static/releases/test/index.html

# 4. Create or update the symbolic link
rm -f /data/web_static/current
ln -s /data/web_static/releases/test /data/web_static/current

# 5. Give ownership to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data

# 6. Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
config_text=$(cat <<EOF
server {
    listen 80 default_server;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current;
    }
    location / {
        add_header X-Served-By \$host;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Served-By \$host;
        proxy_set_header X-Served-By-Nginx \$host;
        proxy_pass http://127.0.0.1:5000;
    }
}
EOF
)

echo "$config_text" > "$config_file"

# 7. Restart Nginx
service nginx restart

exit 0

