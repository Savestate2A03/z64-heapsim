find . -name '*.z64' -exec sh -c '
  file="$0"
  noext="${file%.*}"
  python ../../notwa-mm/z64dump.py "$file"
  sum=($(sha1sum "$file"))
  mv $sum "$noext"
  python ../../notwa-mm/z64dump.py "$noext"
  mv "$noext.z64" "$noext.dec"
' {} ';'
