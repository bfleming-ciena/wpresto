
# Latest Ubuntu LTS
FROM ubuntu:14.04

# Install Nginx

# Download and Install Nginx
RUN apt-get install -y nginx apache2-utils

# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf

# Copy configuration files from the current directory
COPY nginx.conf /etc/nginx/
COPY docker-registry /etc/nginx/sites-available/

# Append "daemon off;" to the configuration
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Link the configuration file
RUN ln -s /etc/nginx/sites-available/docker-registry /etc/nginx/sites-enabled/docker-registry

# Users authorized to use the docker registry
RUN htpasswd -c -b /etc/nginx/docker-registry.htpasswd superuser superuser

# Uncomment to use SSL - Copy the SSL certificate and key
#COPY dev-docker-registry.com.crt /etc/ssl/certs/docker-registry
#COPY dev-docker-registry.com.key /etc/ssl/private/docker-registry

# Forward request and error logs to Docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

# Expose ports
EXPOSE 8080

# Set the default command to execute
# when creating a new container
CMD service nginx start

