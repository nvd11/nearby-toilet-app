old_stat=$(stat -c %Y output.mp4 2>/dev/null)
for i in {1..12}; do
  new_stat=$(stat -c %Y output.mp4 2>/dev/null)
  if [ "$old_stat" != "$new_stat" ]; then
    echo "Video changed!"
    exit 0
  fi
  sleep 5
done
echo "Timeout"
