# First, we need to make sure all dependencies are there. If you are using docker, then the important dependencies are already present on most node images.
FROM node:8

# To run Headful mode, you will need to have a display, which is not present in a server.
# To avoid this, we will use Xvfb, and create a fake display, so the chrome will think there is a display and run properly.
# So we just need to install Xvfb and Puppeteer related dependencies.
RUN apt-get update && apt-get install -yq gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 \
    libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 \
    libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates \
    fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget x11vnc x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps xvfb

# I am going to ignore dumb-init or such for now since it will add complexities to understand what is actually needed here.

# Assuming we are working on /app folder, cd into /app
WORKDIR /srv

# Copy package.json into app folder
COPY package.json /srv

# Install dependencies
RUN npm install

COPY . /srv

# Start server on port 8001
EXPOSE 8001

# I'll also assume you are going to use root user,
# and your script has `--no-sandbox` and `--disable-setuid-sandbox` arguments.
# We run a fake display and run our script.
# Start script on Xvfb
CMD xvfb-run --server-args="-screen 0 1024x768x24" npm start