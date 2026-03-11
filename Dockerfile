FROM kivy/buildozer:stable

WORKDIR /app

COPY . .

RUN buildozer android debug
