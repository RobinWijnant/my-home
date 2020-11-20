### Image

```
sixsq/mjpg-streamer
```

### Ports

```
80:8080
```

### Command

```

'-i' 'input_uvc.so -n -r 1280x720 -f 10' '-o' 'output_http.so -p 80 -w /usr/local/share/mjpg-streamer/www'

```

### Devices

```
/dev/video0
```
